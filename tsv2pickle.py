#! /usr/bin/env python
#################################################################################
#     File Name           :     tsv2pickle.py
#     Created By          :     yc
#     Creation Date       :     [2017-03-22 19:36]
#     Last Modified       :     [2017-05-03 21:16]
#     Description         :
#################################################################################

import sys
import pickle
import os


data = {}
flist = sys.argv[1:]

if len(flist) < 2:
    print("less than two files")
    sys.exit()

for f in flist:
    if os.path.isfile(f):
        with open(f) as subf:
            for line in subf:
                en, cn = line.replace("\n", "").split("\t")
                cnlist = [cni for cni in cn.split(";") if cni]
                if en not in data:
                    data[en] = cnlist
                else:
                    data[en] = data[en] + cnlist


data_join = {}
for k in data:
    data_join[k] = ";".join(set(data[k]))
    # if len(k.split(" ")) == 2:
        # dlist = [d for d in data[k] if not d.endswith("亚种")]
        # data_join[k] = ";".join(set(dlist))
    # else:
        # data_join[k] = ";".join(set(data[k]))


with open('./all.species.tsv', 'w') as f:
    fcontent = []
    for k in data_join:
        fcontent.append("{}\t{}".format(k, data_join[k]))
    f.write("\n".join(fcontent))


with open('./species.data.pickle', 'wb') as f:
    pickle.dump(data_join, f, protocol=pickle.HIGHEST_PROTOCOL)
