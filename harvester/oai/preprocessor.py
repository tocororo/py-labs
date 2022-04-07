#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#


from os import listdir, path

from lxml import etree

XMLParser = etree.XMLParser(remove_blank_text=True, recover=True, resolve_entities=False)

from .formaters import DubliCoreElements, JournalPublishing


class OaiPreprocessor:

    def __init__(self, logger, source, data_dir):

        self.logger = logger
        self.source = source
        p = data_dir
        self.harvest_dir = path.join(p, str(self.source.id))
        # print(self.harvest_dir)
        self.dc = DubliCoreElements(None)
        self.nlm = JournalPublishing(None)
        self.formats = ['marcxml', 'nlm', 'oai_dc', 'oai_marc', 'rfc1807']

    def process_all_items(self):
        """using the directory structure, iterate over the source folders and retrieve all the
        metadata of all records."""
        if path.exists(self.harvest_dir):
            for item in listdir(self.harvest_dir):
                self.process_full_item(item)

    def process_full_item(self, item):
        """retrieve all the metadata of an item and save it to files"""
        idpath = path.join(self.harvest_dir, item, "id.xml")
        # print(idpath)
        if path.exists(idpath):
            dc = self.process_metadata(item, 'oai_dc', self.dc)
            nlm = self.process_metadata(item, 'nlm', self.dc)
            data = self.create_record_data(dc, nlm)

    def process_metadata(self, item, metadata_format, formater):
        xmlpath = path.join(self.harvest_dir, item, metadata_format + ".xml")
        if path.exists(xmlpath):
            xml = etree.parse(xmlpath, parser=XMLParser)
            return formater.process_item(xml)

    def create_record_data(self, dc, nlm):
        data = {}

        data['original_identifier'] = dc['original_identifier']
        data['source'] = self.source.uuid

        data['title'] = dc['title']

        data['keywords'] = dc['keywords']
        data['description'] = dc['description']
        data['language'] = dc['language']
        data['publication_date'] = dc['publication_date']

        creators = []
        for c in dc['creators']:
            creators.append({'name': str(c)})
        data['creators'] = creators

        # ref = []
        # for c in oai_record.metadata['relation']:
        #     ref.append({'raw_reference': str(c)})
        # data['references'] = ref

        return data
