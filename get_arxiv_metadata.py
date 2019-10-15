import csv, sys, re, time, urllib.request
from lxml import etree

csvfname = sys.argv[1]
newcsvfname = sys.argv[2]

BLOCK_SIZE = 512

URL_BASE = "http://export.arxiv.org/api/query?id_list="

with open(csvfname, mode="r", encoding="utf-8", newline='') as csvf:
    with open(newcsvfname, mode="w", encoding="utf-8", newline='') as ncsvf:
        reader = csv.reader(csvf, delimiter='\t', quotechar='"')
        writer = csv.writer(ncsvf, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        arxiv_ids = []
        for i, row in enumerate(reader):
            title = row[1]
            url = row[-2] if row[-1]=="" else row[-1]
            aid = url.split("/")[-1]
            if "." in aid:
                arxiv_ids.append(aid)
            if i % 1000 == 0:
                print("{i}: {aid} {title}".format(i=i, aid=aid, title=title[:60]))
            #end if
        #end for
        arxiv_ids = arxiv_ids[1:]
        data_xmls = []
        for i in range(0,len(arxiv_ids),BLOCK_SIZE):
            url = URL_BASE+(",".join(arxiv_ids[i:i+BLOCK_SIZE]))
            print(url)
            data = urllib.request.urlopen(url).read()
            data_xmls.append(data)
            print(data)
            break
            time.sleep(1.0)
        
        for xml in data_xmls:
            tree = etree.ElementTree(etree.XML(xml))
            root = tree.getroot()
            print(root)
            help(etree)
            
    #end with
#end with
