import json
from sickle import Sickle

sickle = Sickle('http://export.arxiv.org/oai2')
records = sickle.ListRecords(metadataPrefix='oai_dc')

for record in records:
    metadata = record.metadata
    identifier = ''.join(metadata['identifier'][0].split('/')[-2:])
    print(metadata)
    with open('jsons/{}'.format(identifier), 'w') as f:
        json.dump(metadata, f)

