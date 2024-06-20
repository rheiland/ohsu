#
# e.g.:
# python pcdl_test.py output_model1_1rule
#

import sys
import pathlib
import pcdl

print("# args=",len(sys.argv))
if (len(sys.argv) < 2):
    print("Usage:")
else:
    kdx = 1
    out_dir = sys.argv[kdx]
    print("out_dir= ", out_dir)

iframe = 72
print("----- frame # ",iframe)
for idx in [iframe]:
    xml_file = "output%08d.xml" % idx
    try:
        print("-- try to read ",xml_file)
        mcds = pcdl.TimeStep(xml_file, out_dir, microenv=False, graph=False, verbose=True)
    except:
        print("-- break - quit")
        break

    ctype = mcds.data['discrete_cells']['data']['cell_type']
    print("# cells= ",ctype.shape[0])

    current_time = mcds.get_time()
    print('time (min)= ', current_time )