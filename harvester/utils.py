#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#
import enum

import os
import re
from collections import defaultdict
from zipfile import ZipFile

from lxml import etree
from harvester.fulltext.ojs import get_article_files
from harvester.fulltext.dspace import get_record_files

request_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, '
                  'like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }

nsmap = {
    'oai': 'http://www.openarchives.org/OAI/2.0/',
    'oai-identifier': 'http://www.openarchives.org/OAI/2.0/oai-identifier',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'xml': 'http://www.w3.org/XML/1998/namespace',
    'nlm': 'http://dtd.nlm.nih.gov/publishing/2.3'
    }

OJS = "ojs"
DSPACE = "dspace"

default_data_dir = "data"
temp_data_dir = "/tmp"

get_files = {
    OJS: get_article_files,
    DSPACE: get_record_files
}

identifiers_schemas = [
    "ark",
    "arxiv",
    "doi",
    "bibcode",
    "ean8",
    "ean13",
    "handle",
    "isbn",
    "issn_l",
    "issn_p",
    "issn_e",
    "issn_c",
    "issn_o",
    "istc",
    "lsid",
    "pmid",
    "pmcid",
    "purl",
    "upc",
    "url",
    "urn",
    "orcid",
    "gnd",
    "ads",
    "oai",
    "prnps",
    "ernps",
    "oaiurl",
    "grid",
    "wkdata",
    "ror",
    "isni",
    "fudref",
    "orgref",
    "reup",
    "grid",
    "wkdata",
    "ror",
    "isni",
    "fudref",
    "orgref",
    "reup",
    "orgaid",
    "uniid",
    "sceibaid"
    ]


class Formatter(object):
    """ A Formatter will return a dict given something
    (xml, html, or something else) """

    def __init__(self):
        self.metadataPrefix = None

    def get_metadata_prefix(self):
        """name of the formater oai_dc, nlm, jats"""
        return self.metadataPrefix

    def process_item(self, item):
        """given an item return a dict given an item"""
        raise NotImplementedError


class SourceHarvesterMode(enum.Enum):
    FILE_SYSTEM = "ERROR"
    REMOTE = "HARVESTED"


class Item:
    format = ''
    raw = ''
    data = {}


class BaseHarvester(object):
    """any harvester"""

    def process_pipeline(self):
        raise NotImplementedError



"""
several functions and classes that utils across the harvester module,
has oai-pmh specifics and other things,
Probably we need a better desing for the hole module, in the mean time, here can be most diverse
functions, all related to the task of harvesting....
"""

XMLParser = etree.XMLParser(
    remove_blank_text=True, recover=True, resolve_entities=False
    )


class xmlns():
    oai = 'http://www.openarchives.org/OAI/2.0/'

    oai_identifier = 'http://www.openarchives.org/OAI/2.0/oai-identifier'

    dc = 'http://purl.org/dc/elements/1.1/'

    xsi = 'http://www.w3.org/2001/XMLSchema-instance'

    xml = 'http://www.w3.org/XML/1998/namespace'

    nlm = 'http://dtd.nlm.nih.gov/publishing/2.3'


def get_sigle_element(metadata, name, xmlns='dc', language=None):
    # # print('get_sigle_element: '+name)
    elements = metadata.findall('.//{' + xmlns + '}' + name)
    if len(elements) > 1:
        for e in elements:
            lang = '{' + nsmap['xml'] + '}lang'
            if language and lang in e.attrib:
                if e.attrib[lang] == language:
                    return e.text
        # print('self.logger no '+language+' error')
    if len(elements) == 1:
        return elements[0].text
    # # print('self.logger no name error...')


def get_multiple_elements(metadata, name, xmlns='dc', itemname=None, language=None):
    # # print('get_multiple_elements: '+name)
    results = []
    elements = metadata.findall('.//{' + xmlns + '}' + name)
    for e in elements:
        lang = '{' + nsmap['xml'] + '}lang'
        apend = None
        if language and lang in e.attrib:
            if e.attrib[lang] == language:
                if (itemname == ''):
                    apend = e.text
                else:
                    apend = {itemname: e.text}
        else:
            if (itemname):
                apend = {itemname: e.text}
            else:
                apend = e.text
        if e.text is not None and e.text != '' and apend is not None:
            results.append(apend)
    return results


def xml_to_dict(tree, paths=None, nsmap=None, strip_ns=False):
    """Convert an XML tree to a dictionary.

    :param tree: etree Element
    :type tree: :class:`lxml.etree._Element`
    :param paths: An optional list of XPath expressions applied on the XML tree.
    :type paths: list[basestring]
    :param nsmap: An optional prefix-namespace mapping for conciser spec of paths.
    :type nsmap: dict
    :param strip_ns: Flag for whether to remove the namespaces from the tags.
    :type strip_ns: bool
    """
    paths = paths or ['.//']
    nsmap = nsmap or {}
    fields = defaultdict(list)
    for path in paths:
        elements = tree.findall(path, nsmap)
        for element in elements:
            tag = re.sub(
                r'\{.*\}', '', element.tag
                ) if strip_ns else element.tag
            fields[tag].append(element.text)
    return dict(fields)


def get_iroko_harvester_agent():
    return {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
        }


def get_xml_from_file(base_directory, file_name, extra_path=""):
    """get an lxml tree from a file with the path:
        base_directory + extra_path + file_name
        rise an Exception if the file not exists
    """

    xmlpath = os.path.join(base_directory, extra_path, file_name)
    if not os.path.exists(xmlpath):
        raise Exception(
            "Path: {0} not exists".format(
                xmlpath
                )
            )
    return etree.parse(xmlpath, parser=XMLParser)

def get_identifier_schema(pid):
    for schema in identifiers_schemas:
        if schema in pid:
            return schema
    if 'http' in pid or 'https' in pid:
        return 'url'
    return None


class ZipHelper:

    @classmethod
    def compress_dir(cls, src_path, dst_path, dst_filename):
        """
        compress the content (files and directory recursivelly) of the directory in the end of
        src_path
        to a zip file in dst_path/dst_filename
        the idea is not compress the full src_path into the zip, but relative to the directory in
        the end of the src_path.
        :param src_path: source path
        :param dst_path: destination path, excluding filename
        :param dst_filename: filename in destination path.
        :return:
        """
        zip_path = os.path.join(
            dst_path,
            dst_filename
            )
        result = []
        if os.path.isdir(src_path):
            cls._get_zip_items(result, src_path, '')
        else:
            head, tail = os.path.split(src_path)
            result.append({'src': src_path, 'arcname': tail})
        with ZipFile(zip_path, 'w') as zipObj:
            for item in result:
                zipObj.write(item['src'], arcname=item['arcname'])

    @classmethod
    def _get_zip_items(cls, result: list, src_path, item_path):
        if os.path.isdir(src_path):
            for item in os.listdir(src_path):
                cls._get_zip_items(
                    result,
                    os.path.join(src_path, item),
                    os.path.join(item_path, item)
                    )
        else:
            result.append({'src': src_path, 'arcname': item_path})

class ContributorRole(enum.Enum):
    Author = "Author"
    ContactPerson = "ContactPerson"
    DataCollector = "DataCollector"
    DataCurator = "DataCurator"
    DataManager = "DataManager"
    Distributor = "Distributor"
    Editor = "Editor"
    JournalManager = "JournalManager"
    Funder = "Funder"
    HostingInstitution = "HostingInstitution"
    Other = "Other"
    Producer = "Producer"
    ProjectLeader = "ProjectLeader"
    ProjectManager = "ProjectManager"
    ProjectMember = "ProjectMember"
    RegistrationAgency = "RegistrationAgency"
    RegistrationAuthority = "RegistrationAuthority"
    RelatedPerson = "RelatedPerson"
    ResearchGroup = "ResearchGroup"
    RightsHolder = "RightsHolder"
    Researcher = "Researcher"
    Sponsor = "Sponsor"
    Supervisor = "Supervisor"
    WorkPackageLeader = "WorkPackageLeader"


def get_people_from_nlm(metadata: etree._Element):
    """get a IrokoPerson from {http://dtd.nlm.nih.gov/publishing/2.3}contrib
    etree._Element
    return creators, contribs dics, """

    xmlns = '{http://dtd.nlm.nih.gov/publishing/2.3}'
    contribs_xml = metadata.findall('.//' + xmlns + 'contrib')

    contributors = {}

    for contrib in contribs_xml:
        person = dict()

        surname = contrib.find(xmlns + 'name/' + xmlns + 'surname')
        given_names = contrib.find(xmlns + 'name/' + xmlns + 'given-names')
        aff = contrib.find(xmlns + 'aff')
        email = contrib.find(xmlns + 'email')
        if given_names is None and surname is None:
            # FIXME if a person dont have surname or given name, then is not a person....
            #  even if there is an email?
            continue
        else:
            name = ""
            if given_names is not None and given_names.text is not None:
                name += given_names.text
            if surname is not None and surname.text is not None:
                name += ' ' + surname.text
            person['name'] = name
            if aff is not None:
                person['affiliations'] = []
                person['affiliations'].append(aff.text)
            if email is not None:
                person['email'] = email.text
            person['roles'] = []
            if 'corresp' in contrib.attrib:
                if contrib.attrib['corresp'] == "yes":
                    person['roles'].append(ContributorRole.ContactPerson.value)
            if 'contrib-type' in contrib.attrib:
                ctype = contrib.attrib['contrib-type']
                if ctype == "author":
                    person['roles'].append(ContributorRole.Author.value)
                if ctype == "editor":
                    person['roles'].append(ContributorRole.Editor.value)
                if ctype == "jmanager":
                    person['roles'].append(ContributorRole.JournalManager.value)
            if person['name'] in contributors.keys():
                contributors[person['name']]['roles'].extend(person['roles'])
            else:
                contributors[person['name']] = person
    creators = []
    contribs = []
    for name in contributors:
        person = contributors[name]
        if ContributorRole.Author.value in person['roles']:
            creators.append(person)
        else:
            contribs.append(person)
    return creators, contribs
