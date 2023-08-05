from keypartx.basemodes.avn_base import countFreq
import pandas as pd

import leidenalg as la
import igraph as ig 
import networkx as nx

from matplotlib import colors as cls
#import matplotlib
import numpy as np


## --- Edges function --- ## 

def dirNN(allNNedges):
    revNNedges=[]
    for nne in allNNedges:
        a = nne[0]
        b = nne[1]
        revNNedges.append([b,a])
    allNNEdges_dir = revNNedges + allNNedges
    return allNNEdges_dir

def weighted_edges(all_edges):
  all_edges1 = [tuple(x) for x in all_edges]
  edge_df = countFreq(all_edges1,'edge')
  all_edges_count = edge_df .shape[0]
  weighted_edges = []
  nodes0= []
  nodes1= []
  weighted_edgesDICT = []
  for edge,edge_freq in zip(edge_df.edge.to_list(), edge_df.edge_freq.to_list()):
    row = (edge[0],edge[1],edge_freq )
    node0 = edge[0]
    node1 = edge[1]
    nodes0.append(node0)
    nodes1.append(node1)
    weighted_edges.append(row)
    weighted_edgesDICT.append({'node1':edge[0],'node2':edge[1],'weight':edge_freq} )
  nodes = nodes0 +nodes1
  weighted_edgesDF = pd.DataFrame(weighted_edgesDICT)
  return weighted_edges, edge_df, nodes,weighted_edgesDF


def k_edges(all_edges,weight_k =1):
  all_edges_k =[]
  for edge in all_edges:
    if edge[2]>= weight_k:
      all_edges_k.append(edge)
  return all_edges_k

def wedge_type(all_adjV2N_edges_w=[],allNNEdges_dir_w=[],nn_edges = True, aVn_edges = True,weight_k =1):
    include_nn_not =""
    all_edges1 = []
    if nn_edges == True and aVn_edges == True:
        all_edges0 = all_adjV2N_edges_w  + allNNEdges_dir_w
        all_edges1 = k_edges(all_edges0,weight_k =weight_k)
        include_nn_not = 'avN_N edges wight_k = {}'.format(weight_k)
    elif aVn_edges:
        all_edges0 = all_adjV2N_edges_w
        all_edges1 = k_edges(all_edges0,weight_k =weight_k)
        include_nn_not = 'avN edges wight_k = {}'.format(weight_k)
    else:
        all_edges0 =allNNEdges_dir_w
        all_edges1 = k_edges(all_edges0,weight_k =weight_k)
        include_nn_not = 'NN edges wight_k = {}'.format(weight_k)
    return all_edges1, include_nn_not
   
   


## --- Partition --- ## 

def parti(all_edges,com_resolution=1):
    Gdc = nx.DiGraph() 
    #all_edges = all_adjV2N_edges_w  + allNNEdges_dir_w
    Gdc.add_weighted_edges_from(all_edges)
    print('length of nodes:',len(Gdc.nodes))
    #print(Gdc.nodes)


    weights = []
    for edge in all_edges:
      weights.append(edge[2])

    iGd = ig.Graph.from_networkx(Gdc)
    iGd.vs["name"] = iGd.vs["_nx_name"] # keep the networkx name instead of numbers 
    del(iGd.vs["_nx_name"])
    partition = la.find_partition(iGd, la.RBConfigurationVertexPartition, weights = weights,resolution_parameter = com_resolution)#max_comm_size=10 # the smaller resolution, the fewer community but bigger size
  
    comNUM = []
    nodeNames = []
    for i,pt in enumerate(partition):
      #print(i,pt)
      pt_names = [iGd.vs[index]['name'] for index in pt]
      nodeNames.append(pt_names)
      comNUM.append(i)
    comDF = pd.DataFrame({'community_No':comNUM,'nodes':nodeNames})
    
    return partition,iGd,Gdc,comDF


## ---Color setting for community network ---##

def colorsList(colorL = False):
    if colorL == False:
        colorList = ['darkred','gold','blue','orange','green','purple','lime']
    else:
        colorList = colorL
    colorList_rgba = []
    for color in colorList:
      colorList_rgba.append(list(cls.to_rgba(color)))
    #print(colorList_rgba)
    colorList_rgba1= []
    for i,a in enumerate(np.arange(.01,1,0.05)[::-1]): # do not start with 0 alpha will be no color,  reverse the order 
      for colors in colorList_rgba:
        if i <len(colorList):
          colors[-1]= 1
        else:
          colors[-1]= a
          #print(colors)
        colors1 = cls.to_hex(colors, keep_alpha=True)
      
        colorList_rgba1.append(colors1)
    return colorList_rgba1
