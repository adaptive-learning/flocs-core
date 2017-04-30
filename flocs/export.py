from datetime import datetime
import csv
import os
from .utils.names import camel_to_kebab_case, pluralize


def export_state(dirpath, state):
    datestamp = datetime.now().strftime('%Y-%m-%d')
    # the last empty path ('') is there to make it a directory, not a file
    full_dirpath = os.path.join(dirpath, datestamp, '')
    os.makedirs(full_dirpath, exist_ok=True)
    for entity_class, entity_map in state.entities.items():
        export_entity_map(full_dirpath, entity_class, entity_map)


def export_entity_map(dirpath, entity_class, entity_map):
    file_name = pluralize(camel_to_kebab_case(entity_class.__name__)) + '.csv'
    full_path = os.path.join(dirpath, file_name)
    fields = entity_class._fields
    with open(full_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(fields)
        for entity in entity_map.values():
            writer.writerow(entity)
