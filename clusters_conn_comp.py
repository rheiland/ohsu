#
# e.g.:
# python clusters_conn_comp.py output_model1_1rule
#
__author__ = "Randy Heiland"

import sys
import pathlib
#import xml.etree.ElementTree as ET
#import math
# import scipy.io
# from pyMCDS import pyMCDS
# from pyMCDS_cells import pyMCDS_cells
import pcdl
#import matplotlib
import numpy as np
import networkx as nx
# import matplotlib.pyplot as plt

out_dir = None
print("# args=",len(sys.argv))
if (len(sys.argv) < 3):
    print(f'Invalid args -- Usage: {sys.argv[0]} <dir> <frame>\n')
    sys.exit(-1)
else:
    kdx = 1
    out_dir = sys.argv[kdx]
    print("out_dir= ", out_dir)
    kdx += 1
    iframe = int(sys.argv[kdx])

# fig, ax = plt.subplots()

# ------- 1st plot all computed values (at every 10 hours)
hr_delta = 20
#hr_delta = 10
# for idx in range(0,615, hr_delta):

# iframe = 72
print("----- finding clusters for frame # ",iframe)
#for idx in [480]:
for idx in [iframe]:
    xml_file = "output%08d.xml" % idx
    try:
        # mcds = pyMCDS_cells(xml_file, out_dir)   
        # mcds = pcdl.TimeStep(xml_file,out_dir)
        print("-- try to read ",xml_file)
        mcds = pcdl.TimeStep(xml_file,out_dir, microenv=False, graph=False, verbose=True)
    except:
        print("-- break - quit")
        break

    ctype = mcds.data['discrete_cells']['data']['cell_type']
    print("# cells= ",ctype.shape[0])

    current_time = mcds.get_time()
    print('time (min)= ', current_time )

    xv = mcds.data['discrete_cells']['data']['position_x']
    yv = mcds.data['discrete_cells']['data']['position_y']
    r = mcds.data['discrete_cells']['data']['radius']

    for cell_type in [0,1]:
        print("\n------ cell_type = ",cell_type)
        id_ctype = np.where(ctype == cell_type)  # return 2D array: id_ct0=  (array([ 0,  2, ...  48]),)  ?
        # print("id_ct0= ",id_ct0)
        id_ctype = id_ctype[0]
        # print(id_ctype)
        # max_idx = 6
        # max_idx = len(id_ct0[0])
        max_idx = len(id_ctype)
        print("len(id_ctype)= ",len(id_ctype))
        # print("partial: ",id_ct0[0][0:max_idx])

        radius = 8.41271055     # default
        dmax = 2*radius + 1.e-6
        dmax2 = dmax*dmax

        G = nx.Graph()

        kdx = 0
        kmax = len(id_ctype)
        for kdx in range(0,kmax):
            ii = id_ctype[kdx]
            for ndx in range(kdx,kmax):
                jj = id_ctype[ndx]

                if ii != jj:
                    x1 = xv[ii]
                    x2 = xv[jj]
                    y1 = yv[ii]
                    y2 = yv[jj]
                    d2 = (x1-x2)**2 + (y1-y2)**2
                    if d2 < dmax2:
                        G.add_edge(ii,jj)

        # print(f'type(nx.connected_components(G)= {type(nx.connected_components(G))}')
        lcc = list(nx.connected_components(G))
        # print(f'type(lcc[0])= {type(lcc[0])}')
        # print(f'{type(nx.connected_components(G))}')
        l_ids = []
        for ic in lcc:
            l_ids += ic
        isolated_cells = set(id_ctype) - set(l_ids)
        print("missing (isolated) cell ids=",isolated_cells)
        # print(f'l_ids= {l_ids}')
        print(f'\nfor time={current_time}: # of clusters for cell type {cell_type} = { len(isolated_cells) + len(list(nx.connected_components(G)))}\n')
        print(f'    {list(nx.connected_components(G))}')
