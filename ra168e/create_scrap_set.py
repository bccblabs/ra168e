from collections import defaultdict
from pymongo import MongoClient
import pickle
db0 = MongoClient("localhost", 27017).pure_urls.urls
db1 = MongoClient("localhost", 27017).pure_urls.urls2

src_dict = defaultdict(list)


num_insts = 9
def insert_docs (db):
    for x in db.find({}):
        doc = x['_id']
        if len(doc['bodyType']) > 0 and len(x['images']) > 50:
            label = "%s_%s_%s_%s" %(doc['make'], doc['model'], doc['gen_name'].replace(" ", "__"), doc['bodyType'].replace(" ", "__"))
            src_dict[label] += x['images']

def stats ():
    total = 0
    num_labels = len (src_dict.keys())
    batch_size = num_labels/num_insts
    for x in xrange (0, num_labels, batch_size):
        dump_docs (src_dict.keys()[x:x+batch_size], x/batch_size)

def dump_docs(labels, batch):
    doc = defaultdict(list)
    for x in labels:
        doc[x] = src_dict[x][:1000]
    print "batch %d dump %d labels" %(batch, len (labels))
    pickle.dump(doc, open("src_" + str(batch), "wb"))

insert_docs(db0)
insert_docs(db1)
stats()
