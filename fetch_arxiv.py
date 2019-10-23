import json, os, datetime, requests.exceptions, time
from sickle import Sickle

repeat = True
while repeat:
    try:
        earliest_date = datetime.date(1,1,4)
        for fname in [fname for fname in os.listdir("jsons/") if fname != ".gitkeep"]:
            with open("jsons/{}".format(fname),"r") as f:
                d = json.load(f)
                ddate = datetime.date.fromisoformat(d["date"][0])
                earliest_date = max(earliest_date, ddate)

        sickle = Sickle('http://export.arxiv.org/oai2')
        
        records = sickle.ListRecords(metadataPrefix='oai_dc',**{"from":earliest_date})
        for record in records:
            metadata = record.metadata
            identifier = ''.join(metadata['identifier'][0].split('/')[-2:])
            print(metadata)
            with open('jsons/{}'.format(identifier), 'w') as f:
                json.dump(metadata, f)
        repeat = False
    except requests.exceptions.ReadTimeout as e:
        time.sleep(60)

