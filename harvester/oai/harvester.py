#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

import os
import shutil
import time
import traceback
import uuid
from enum import Enum
from zipfile import BadZipFile, ZipFile

from lxml import etree
from sickle import Sickle

import harvester.utils as utils
from harvester.oai.formaters import DubliCoreElements, JournalPublishing

from threading import Thread
from concurrent.futures import ThreadPoolExecutor, as_completed


XMLParser = etree.XMLParser(
    remove_blank_text=True, recover=True, resolve_entities=False
    )


class OaiHarvesterFileNames(Enum):
    IDENTIFY = "identify.xml"
    FORMATS = "metadata_formats.xml"
    SETS = "sets.xml"
    ITEM_IDENTIFIER = "id.xml"


def fetch_url(url, d):
    OaiFetcher.fetch_url(url, d)


def fetch_list(l, d):
    file1 = open(l, 'r')
    lines = file1.readlines()
    for line in lines:
        OaiFetcher.fetch_url(line, d)


def fetch_list_async(l, d):
    # file1 = open(l, 'r')
    # lines = file1.readlines()
    lines = ['https://revistas.reduc.edu.cu/index.php/agrisost/oai',
             'http://www.alcance.uh.cu/index.php/RCIC/oai']
    processes = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for line in lines:
            print('=======================================')
            print(line)
            print('=======================================')
            processes.append(executor.submit(OaiFetcher.fetch_url, line, d))
    for task in as_completed(processes):
        print(task.result())


class OaiFetcher:
    """ esta clase se encarga de recolectar un OAI endpoint.
    crea una estructura de carpetas donde se almacena todo lo cosechado sin procesar
    dentro de data_dir guarda un zip con un UUID como nombre que dentro tiene:
        1- ficheros con el response de los siguientes verbos:
            - identify.xml
            - metadata_formats.xml
            - sets.xml
        2- carpetas con uuid aleatorios como nombre por cada record, con la forma:
            - id.xml
            - metadata_format_1.xml
            - metadata_format_2.xml
            - fulltext_1.ext
            - fulltext_2.ext
    """

    @classmethod
    def fetch_url(cls, url, data_dir=None, wait_time=3, source_type=utils.OJS):
        fetcher = OaiFetcher(url, data_dir=data_dir, request_wait_time=wait_time)
        return fetcher.start_harvest_pipeline()

    def __init__(self, url, data_dir=None, request_wait_time=3, source_type=utils.OJS):

        max_retries = 3
        timeout = 30

        self.url = url
        self.request_wait_time = request_wait_time
        self.id = str(uuid.uuid4())
        self.source_type = utils.OJS

        if not data_dir:
            self.data_dir = utils.default_data_dir
        else:
            self.data_dir = data_dir

        f = open(os.path.join(self.data_dir, self.id + '-url'), "w", encoding='UTF-8')
        f.write(self.url)
        f.close()

        self.harvest_dir = os.path.join(
            utils.temp_data_dir,
            "iroko-harvest-" + str(self.id)
            )
        shutil.rmtree(self.harvest_dir, ignore_errors=True)
        if not os.path.exists(self.harvest_dir):
            os.mkdir(self.harvest_dir)

        self.formats = []
        self.oai_dc = DubliCoreElements()
        self.nlm = JournalPublishing()

        # args = {'headers':request_headers,'proxies':proxies,'timeout':15, 'verify':False}
        args = {"headers": utils.request_headers, "timeout": timeout, "verify": False}
        self.sickle = Sickle(
            self.url,
            encoding='UTF-8',
            max_retries=max_retries,
            **args
            )

    def start_harvest_pipeline(self):
        """default harvest pipeline, identify, discover, process"""
        try:
            self.identity_source()
            self.get_items()
            return self.compress_harvest_dir()
        except Exception as e:
            f = open(os.path.join(self.data_dir, self.id + '-error'), "w", encoding='UTF-8')
            f.write(traceback.format_exc())
            f.close()
            shutil.rmtree(self.harvest_dir, ignore_errors=True)
            return None

    def compress_harvest_dir(self):
        """compress the harvest_dir to a zip file in harvest_data dir
        and deleted harvest_dir """
        shutil.rmtree(
            os.path.join(self.data_dir, str(self.id)),
            ignore_errors=True
            )
        utils.ZipHelper.compress_dir(self.harvest_dir, self.data_dir, str(self.id))
        shutil.rmtree(self.harvest_dir, ignore_errors=True)
        return os.path.join(self.data_dir, str(self.id))

    def identity_source(self):
        self.get_identify()
        self.get_formats()
        self.get_sets()

    def _write_file(self, name, content, extra_path=""):
        """helper function, always write to f = open(os.path.join(self.harvest_dir, extra_path,
        name),"w")"""

        f = open(os.path.join(self.harvest_dir, extra_path, name), "w", encoding='UTF-8')
        f.write(content)
        f.close()

    def _get_xml_from_file(self, name, extra_path=""):
        return utils.get_xml_from_file(self.harvest_dir, name, extra_path=extra_path)

    def get_identify(self):
        """get_identity, raise IrokoHarvesterError"""
        identify = self.sickle.Identify()
        xml = identify.xml
        self._write_file("identify.xml", identify.raw)

    def get_formats(self):
        """get_formats, raise IrokoHarvesterError"""

        arguments = {}
        items = self.sickle.ListMetadataFormats(**arguments)
        for f in items:
            self.formats.append(f.metadataPrefix)
        self._write_file("metadata_formats.xml", items.oai_response.raw)

        if "oai_dc" not in self.formats:
            self._write_file(
                'error_no_dublin_core', " oai_dc is not supported by {0} ".format(self.url)
                )

    def get_sets(self):
        """get_sets"""
        arguments = {}
        items = self.sickle.ListSets(**arguments)
        self._write_file("sets.xml", items.oai_response.raw)

    def get_items(self):
        """retrieve all the identifiers of the source, create a directory structure,
        and save id.xml for each identified retrieved.
        Check if the repo object identifier is the same that the directory identifier.
        If a item directory exist, delete it and continue"""

        xml = self._get_xml_from_file("identify.xml")
        identifier = xml.find(
            ".//{" + utils.xmlns.oai_identifier + "}repositoryIdentifier"
            )

        iterator = self.sickle.ListIdentifiers(
            metadataPrefix=self.oai_dc.metadataPrefix
            )
        count = 0
        for item in iterator:
            harvest_item_id = str(uuid.uuid4())
            p = os.path.join(self.harvest_dir, harvest_item_id)
            if not os.path.exists(p):
                os.mkdir(p)
            self._write_file("id.xml", item.raw, harvest_item_id)
            self._get_all_formats(item.identifier, harvest_item_id)

            time.sleep(self.request_wait_time)

    def _get_all_formats(self, identifier, harvest_item_id):
        """retrieve all the metadata of an item and save it to files"""

        for f in self.formats:
            try:
                arguments = {"metadataPrefix": f, "identifier": identifier}
                record = self.sickle.GetRecord(**arguments)
                self._write_file(f + ".xml", record.raw, harvest_item_id)
                time.sleep(self.request_wait_time)
                if f == "oai_dc":
                    xml = utils.get_xml_from_file(
                        self.harvest_dir, f + ".xml", harvest_item_id)
                    data = self.oai_dc.process_item(xml)
                    for id in data['identifiers']:
                        if id['idtype'] == 'url':
                            utils.get_files[self.source_type](
                                id['value'],
                                os.path.join(self.harvest_dir, harvest_item_id, 'files'))

            except Exception as e:
                self._write_file('error', traceback.format_exc(), harvest_item_id)
        time.sleep(self.request_wait_time)


