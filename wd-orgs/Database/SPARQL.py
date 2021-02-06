# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"


def get_resultsInstanceOf(QID):
    # Q43229 - organization
    query = """SELECT ?item  ?itemLabel  
               ?country  ?countryLabel
        
                WHERE {
                 ?item (wdt:P31)+ wd:""" f"{QID};" """
                                  rdfs:label ?itemLabel.
                    FILTER(lang(?itemLabel) = 'en')
                 
                    OPTIONAL { ?item  wdt:P17  ?country }      
                    SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
                 }
                 ORDER BY ?item"""

    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def get_resultsSubClass(QID):
    # Q43229 - organization
    query = """SELECT ?item ?itemLabel
                WHERE { 
                      ?item (wdt:P279)* wd:""" f"{QID};" """
                             rdfs:label ?itemLabel.
                      FILTER(lang(?itemLabel) = 'en')
                }
                ORDER BY ?item"""

    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def get_infoInstace(itemLabel):

    query = """SELECT ?item  ?itemLabel  ?itemDescription
           ?instanceOf  ?instanceOfLabel
           ?image
           ?inception
           ?nativeLabel
           ?foundedBy  ?foundedByLabel  
           ?country  ?countryLabel
           ?state  ?stateLabel
           ?region  ?regionLabel  
           ?headquartersLocation
           ?numEmployees
           ?officialWebsite  ?officialWebsiteLabel
           ?ISNI
           ?GRID
           ?quoraTopicID
           ?twitterUsername

    WHERE
       {     
    ?item wdt:P17 wd:Q241;
          rdfs:label ?itemLabel.
    FILTER ( CONTAINS(LCASE(?itemLabel), """  f'"{itemLabel}"' " """" ))

        OPTIONAL { ?item  wdt:P31  ?instanceOf }
        OPTIONAL { ?item  wdt:P18  ?image }
        OPTIONAL { ?item  wdt:P571  ?inception }
        OPTIONAL { ?item  wdt:P1705  ?nativeLabel }
        OPTIONAL { ?item  wdt:P112  ?foundedBy }
        OPTIONAL { ?item  wdt:P17  ?country }
        OPTIONAL { ?item  wdt:P131  ?state }   
        OPTIONAL { ?item  wdt:P276  ?region }
        OPTIONAL { ?item  wdt:P159  ?headquartersLocation }
        OPTIONAL { ?item  wdt:P1128  ?numEmployees }
        OPTIONAL { ?item  wdt:P856  ?officialWebsite }
        OPTIONAL { ?item  wdt:P213  ?ISNI }
        OPTIONAL { ?item  wdt:P2427  ?GRID }
        OPTIONAL { ?item  wdt:P3417  ?quoraTopicID }
        OPTIONAL { ?item  wdt:P2002  ?twitterUsername }

        SERVICE wikibase:label { bd:serviceParam wikibase:language  "en,es" }
      }"""
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


if __name__ == '__main__':
    resultsSubClass = get_infoInstace('Q43229')
    for result in resultsSubClass["results"]["bindings"]:
        print(result)

# resultsSubClass = get_resultsSubClass('Q43229')
# for result in resultsSubClass["results"]["bindings"]:
#     # subClass = SubClass(result.item.value)
#     print(result)

# resultsInstanceOf = get_resultsInstanceOf('Q43229')
# for result in resultsInstanceOf["results"]["bindings"]:
#     # subClass = SubClass(result.item.value)
#     print(result)