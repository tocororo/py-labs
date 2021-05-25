import dedupe
from messy_data import messy_object
import logging
import optparse
import os
import json

data = {}

for obj in messy_object:
    #obj_id = int(obj["id"])
    data[obj["id"]] = obj["metadata"]

if __name__ == '__main__':

    optp = optparse.OptionParser()
    optp.add_option('-v', '--verbose', dest='verbose', action='count',
                    help='Increase verbosity (specify multiple times for more)'
                    )
    (opts, args) = optp.parse_args()
    log_level = logging.WARNING
    if opts.verbose:
        if opts.verbose == 1:
            log_level = logging.INFO
        elif opts.verbose >= 2:
            log_level = logging.DEBUG
    logging.getLogger().setLevel(log_level)

    #input_file = 'csv_example_messy_input.csv'
    #output_file = 'csv_example_output.csv'
    settings_file = 'csv_example_learned_settings'
    training_file = 'csv_example_training.json'

    # If a settings file already exists, we'll just load that and skip training
    if os.path.exists(settings_file):
        print('reading from', settings_file)
        with open(settings_file, 'rb') as f:
            deduper = dedupe.StaticDedupe(f)
    else:
        # ## Training

        # Define the fields dedupe will pay attention to
        fields = [

            {'field': 'name', 'type': 'String'},
            # {'field': 'aliases', 'type': 'Text', 'corpus' : [
            #  "University of Cienfuegos Carlos Rafael Rodr\u00edguez",
            #  "Universidad de Cienfuegos Carlos Rafael Rodr\u00edguez"
            # ]},
            # {'field': 'acronyms', 'type': 'Text', 'corpus' : [
            #     "IPK"
            # ]},
            # {'field': 'types', 'type': 'Text', 'corpus': [
            #     "Facility"
            # ]},
            # {'field': 'email_address', 'type': 'String', },
            # {'field': 'established', 'type': 'Price'},
            # {'field': 'identifiers', 'type': 'FuzzyCategorical', 'corpus': [
            #         {"idtype":"grid","value":"grid.467442.7"},{"idtype":"isni","value":"0000 0001 0756 2653"},{"idtype":"wkdata","value":"Q1070161"},{"idtype":"ror","value":"https://ror.org/02m74w963"}
            # ]},
            # {'field': 'addresses', 'type': 'FuzzyCategorical', 'corpus': [
            # {"city":"Havana","country":"Cuba","country_code":"CU","lat":23.07259,"line_1":"","line_2":"","lng":-82.383594,"postcode":"","primary":False,"state_code":""}
            # ]},
            # {'field': 'labels', 'type': 'FuzzyCategorical', 'corpus': [
            #     {"iso639": "es", "label": "Instituto Superior de Tecnolog\u00edas y Ciencias Aplicadas"}
            # ]},
        ]

        # Create a new deduper object and pass our data model to it.
        deduper = dedupe.Dedupe(fields)

        # If we have training data saved from a previous run of dedupe,
        # look for it and load it in.
        # __Note:__ if you want to train from scratch, delete the training_file
        if os.path.exists(training_file):
            print('reading labeled examples from ', training_file)
            with open(training_file, 'rb') as f:
                deduper.prepare_training(data, f)
        else:
            deduper.prepare_training(data)

        # ## Active learning
        # Dedupe will find the next pair of records
        # it is least certain about and ask you to label them as duplicates
        # or not.
        # use 'y', 'n' and 'u' keys to flag duplicates
        # press 'f' when you are finished
        print('starting active labeling...')

        dedupe.console_label(deduper)

        # Using the examples we just labeled, train the deduper and learn
        # blocking predicates
        deduper.train()

        # When finished, save our training to disk
        with open(training_file, 'w') as tf:
            deduper.write_training(tf)

        # Save our weights and predicates to disk.  If the settings file
        # exists, we will skip all the training and learning next time we run
        # this file.
        with open(settings_file, 'wb') as sf:
            deduper.write_settings(sf)

    # ## Clustering

    # `partition` will return sets of records that dedupe
    # believes are all referring to the same entity.

    print('clustering...')
    clustered_dupes = deduper.partition(data, 0.5)

    print('# duplicate sets', len(clustered_dupes))
    print ('clustered_dupes', clustered_dupes)
    print( 'enumerate', enumerate(clustered_dupes))
    cluster_membership = {}
    for cluster_id, (records, scores) in enumerate(clustered_dupes):
        for record_id, score in zip(records, scores):
            cluster_membership[record_id] = {
                    "Cluster ID": messy_object[cluster_id]['metadata']['id'],
                    "confidence_score": score
            }
    print (cluster_membership)
    with open('data.json', 'w') as outfile:
        for obj in messy_object:
            # obj_id = int(obj['id'])
            data.update(cluster_membership[obj['id']])
            json.dump(data, outfile)
