import csv, json, sys, re, time, requests
from lxml import etree

csvfname = sys.argv[1]
newjsonfname = sys.argv[2]

text_tags = [
        "id",
        "published",
        "title",
        "summary",
]
xml_tags = {
        "primary_category":"term",
        "category":"term"
}

single_tags = [
        "id",
        "published",
        "title",
        "summary",
        "primary_category",
]
list_tags = [
        "category"
]

BLOCK_SIZE = 10

URL_BASE = "http://export.arxiv.org/api/query?id_list="

with open(csvfname, mode="r", encoding="utf-8", newline='') as csvf:
    with open(newjsonfname, mode="w", encoding="utf-8", newline='') as njsonf:
        reader = csv.reader(csvf, delimiter='\t', quotechar='"')

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
        papers = []
        try:
            with requests.Session() as sess:
                for i in range(0,len(arxiv_ids),BLOCK_SIZE):
                    url = URL_BASE+(",".join(arxiv_ids[i:i+BLOCK_SIZE]))
                    xml = requests.get(url).content
                    
                    tree = etree.ElementTree(etree.XML(xml))
                    root = tree.getroot()
                    for entry in [e for e in root if "entry" in e.tag]:
                        edict = {
                                **{t:None for t in single_tags},
                                **{t:[] for t in list_tags}
                        }
                        for value in entry:
                            tag = value.tag
                            tag = tag.replace("{http://www.w3.org/2005/Atom}","").replace("{http://arxiv.org/schemas/atom}","")
                            if tag in text_tags:
                                entry_value = value.text
                            elif tag in xml_tags:
                                entry_value = value.get(xml_tags[tag])
                            if tag in single_tags:
                                edict[tag] = entry_value
                            elif tag in list_tags:
                                edict[tag] += [entry_value]
                        papers.append(edict)
                        print("{i}: {aid} {title}".format(i=len(papers), aid=edict["id"][-10:], title=edict["title"][:60].replace("\n","")))
                    #end for entry
                    
                    time.sleep(1.01)
                #end for
            #end with
        except KeyboardInterrupt:
            pass
        
        json.dump(papers, njsonf, ensure_ascii=False)
    #end with
#end with
