import gzip
import json
import glob
import os


# files = glob.glob("../JSON2RDF/msmarco_v2_passage_links/msmarco_v2_passage_links_*")
# for file in files:
#     passages = []
#     with gzip.open(file, "rb") as infile:
#         with open(os.path.join("../JSON2RDF/msmarco_v2_unzipped_whole/",os.path.basename(file).replace(".gz","")),"w+") as of:
#             for line in infile:
#                 l = json.loads(line)
#                 if len(l["passage"]) > 0:
#                     passages.append(l)
#             rst = {"passages":passages}
#             of.write(json.dumps(rst)+"\n")

files = glob.glob("msmarco_v2_passage_links/msmarco_v2_passage_links_*")
for file in files:
    passages = []
    with gzip.open(file, "rb") as infile:
        with open(os.path.join("msmarco_v2_unzipped_slim/",os.path.basename(file).replace(".gz","")),"w+") as of:
            for line in infile:
                l = json.loads(line)
                if len(l["passage"]) > 0:
                    passage = []
                    for item in l['passage']:
                        passage.append({"entity_id":item["entity_id"], "entity":item["entity"]})
                    l["passage"] = passage
                    l.pop("spans", None)
                    passages.append(l)
            rst = {"passages":passages}
            of.write(json.dumps(rst)+"\n")