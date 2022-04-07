#  Copyright (c) 2022. Universidad de Pinar del Rio
#  This file is part of SCEIBA (sceiba.cu).
#  SCEIBA is free software; you can redistribute it and/or modify it
#  under the terms of the MIT License; see LICENSE file for more details.
#

import re

from lxml import etree

from harvester.utils import (
    ContributorRole, Formatter, get_identifier_schema, get_multiple_elements,
    get_people_from_nlm, get_sigle_element, nsmap,
    )


class DubliCoreElements(Formatter):

    def __init__(self):

        self.metadataPrefix = 'oai_dc'
        self.xmlns = 'http://purl.org/dc/elements/1.1/'

    def process_item(self, xml: etree._Element):
        """given an xml item return a dict, ensure is http://purl.org/dc/elements/1.1/ valid and
        return the data"""

        data = {}
        header = xml.find('.//{' + nsmap['oai'] + '}header')
        metadata = xml.find('.//{' + nsmap['oai'] + '}metadata')

        setSpec = header.find('.//{' + nsmap['oai'] + '}setSpec')
        data['spec'] = setSpec.text

        identifier = header.find('.//{' + nsmap['oai'] + '}identifier')
        # data['original_identifier'] = identifier.text
        identifiers = []
        identifiers.append({'idtype': 'oai', 'value': identifier.text})

        pids = get_multiple_elements(
            metadata, 'identifier', xmlns=self.xmlns, itemname=None, language=None
            )

        for pid in pids:
            schema = get_identifier_schema(pid)
            if schema:
                identifiers.append({'idtype': schema, 'value': pid})
        # identifiers.insert(0, {'idtype': 'oai','value': identifier.text})
        data['identifiers'] = identifiers

        data['title'] = get_sigle_element(metadata, 'title', xmlns=self.xmlns, language='es-ES')

        data['creators'] = []
        creators = get_multiple_elements(metadata, 'creator', xmlns=self.xmlns, itemname='name')
        for creator in creators:
            if isinstance(creator['name'], str) and creator['name'] != '':
                creator['roles'] = []
                creator['roles'].append(ContributorRole.Author.value)
                data['creators'].append(creator)
        data['contributors'] = []
        contributors = get_multiple_elements(
            metadata, 'contributor', xmlns=self.xmlns, itemname='name',
            language='es-ES'
            )
        for contributor in contributors:
            if isinstance(contributor['name'], str) and contributor['name'] != '':
                data['contributors'].append(contributor)

        keywords = get_sigle_element(metadata, 'subject', xmlns=self.xmlns, language='es-ES')
        if keywords and isinstance(keywords, str):
            data['keywords'] = re.split('; |, ', keywords)

        desc = get_sigle_element(metadata, 'description', xmlns=self.xmlns, language='es-ES')
        if desc and desc != '':
            data['description'] = desc

        data['publisher'] = get_sigle_element(
            metadata, 'publisher', xmlns=self.xmlns, language='es-ES'
            )

        data['publication_date'] = get_sigle_element(
            metadata, 'date', xmlns=self.xmlns, language='es-ES'
            )

        types = get_multiple_elements(metadata, 'type', xmlns=self.xmlns)
        data['types'] = types

        formats = get_multiple_elements(metadata, 'format', xmlns=self.xmlns)
        data['formats'] = formats

        sources = get_multiple_elements(metadata, 'source', xmlns=self.xmlns)
        data['sources'] = sources

        data['language'] = get_sigle_element(metadata, 'language', xmlns=self.xmlns)

        relations = get_multiple_elements(metadata, 'relation', xmlns=self.xmlns)
        # separar el caso especial ref, de lo que realmente significa esto: una url con otro
        # objeto relacionado (asumiendo el caso mas comun: el pdf donde esta el articulo...)
        data['relations'] = relations

        coverages = get_multiple_elements(metadata, 'coverage', xmlns=self.xmlns)
        data['coverages'] = coverages

        rights = get_multiple_elements(metadata, 'rights', xmlns=self.xmlns)
        data['rights'] = rights

        return data


class JournalPublishing(Formatter):

    def __init__(self):
        self.metadataPrefix = 'nlm'
        self.xmlns = '{http://dtd.nlm.nih.gov/publishing/2.3}'

    def process_item(self, xml: etree._Element):
        """given an xml item return a dict, ensure is http://dtd.nlm.nih.gov/publishing/2.3
        is mainly focussed on contributors and authors"""

        data = {}
        header = xml.find('.//{' + nsmap['oai'] + '}header')
        metadata = xml.find('.//{' + nsmap['oai'] + '}metadata')

        identifier = header.find('.//{' + nsmap['oai'] + '}identifier')
        data['original_identifier'] = identifier.text
        setSpec = header.find('.//{' + nsmap['oai'] + '}setSpec')
        data['spec'] = setSpec.text

        # article_meta = xml.find('.//{' + self.xmlns + '}article-meta')
        # contribs = metadata.findall('.//' + self.xmlns + 'contrib')
        # # print(contribs)
        creators, contributors = get_people_from_nlm(metadata)
        #  = []
        # for contrib in contribs:
        #     p, is_author = IrokoPerson.get_people_from_nlm(contrib)
        #     # print(is_author)

        #     # TODO: los nombres de los autores se estan uniendo...
        #     if p is not None:
        #         if is_author:
        #             creators.append(p)
        #         else:
        #             contributors.append(p)
        data['creators'] = creators
        data['contributors'] = contributors
        return data
