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


# gray unit network to sentence by order of degree and weight

class unit2sent:
  """community nodes: {('food2nnn',5),('good2aaa',2),('love2vvv',3)}
     community edges:{('good2aaa','food2nnn',2),('love2nnn','food2vvv',3)}
     ncR: core noun degree/ core nouns degree sum
     vdR: verb to core noun edge/ verbs to core noun edges sum
     adR: adjective to core noun edge/ adjectives to core noun edges sum
     ndR: noun to core noun edge/ nouns to core noun edges sum
     """   
  def __init__(self, commu_nodes,commu_edges):
    self.commu_nodes =  commu_nodes
    self.commu_edges = commu_edges

  # 1. core nouns in community 

  def corenoun(self,ncR=.01):
    commu1_nodes = self.commu_nodes
    nnodes = []
    ndegrees =[]
    for node in commu1_nodes:
      if 'nnn' in node[0]:
        nnodes.append(node[0])
        ndegrees.append(node[1])
        
    cn_nodeDF = pd.DataFrame({'cn_nodes':nnodes,'cn_degrees':ndegrees})
    cn_nodeDF = cn_nodeDF.sort_values(by='cn_degrees',ascending= False)

    noun_cores0 = cn_nodeDF.cn_nodes.to_list()
    noun_coresD = cn_nodeDF.cn_degrees.to_list()
    #ncR = .1
    core_nouns= []
    core_nounsD =[]
    for nc,ncd in zip(noun_cores0,noun_coresD):
      nrc = ncd/sum(noun_coresD)
      if nrc>ncR:
        core_nouns.append(nc)
        core_nounsD.append(ncd)
    return core_nouns,core_nounsD


  ## 2. avn order by degree

  def avn2coren(self,c_noun,c_nounD=False,vdR = .1, adR =.1,ndR =.1):
    commu1_edges = self.commu_edges
    avns =[]
    avnWs = []
    avnPs =[]
    for edge in commu1_edges:
      if c_noun in edge[1]:
        avn = edge[0]
        if 'nnn' in avn:
          avnP ='NOUN'
        elif 'aaa' in avn:
          avnP ="ADJ"
        elif 'vvv' in avn:
          avnP ="VERB"
        avnW= edge[2]
        avns.append(avn)
        avnWs.append(avnW)
        avnPs.append(avnP)

    avnDF = pd.DataFrame({'avns':avns,'avnWs':avnWs,'avnPs':avnPs})

    verbDF = avnDF[avnDF['avnPs'] == 'VERB']
    verbDF = verbDF.sort_values(by ='avnWs', ascending = False)

    nounDF = avnDF[avnDF['avnPs'] == 'NOUN']
    nounDF = nounDF.sort_values(by ='avnWs', ascending = False)

    adjDF = avnDF[avnDF['avnPs'] == 'ADJ']
    adjDF =  adjDF.sort_values(by='avnWs', ascending = False)


    verbs = verbDF.avns.to_list()
    verbsD = verbDF.avnWs.to_list()

    nouns = nounDF.avns.to_list()
    nounsD = nounDF.avnWs.to_list()

    adjs = adjDF.avns.to_list()
    adjsD = adjDF.avnWs.to_list()


    #vdR = 0.4
    #adR = 0.2
    #ndR = 0.1
    vlist =[]
    for v, vd in zip(verbs,verbsD):
        vdr = vd/sum(verbsD)
        if vdr> vdR:
          v = v.replace('2vvv',"")
          vlist.append((v + "(" + str(vd) +")"))
    alist = []
    for a, ad in zip(adjs,adjsD):
        adr = ad/sum(adjsD)
        if adr>adR:
          a = a.replace('2aaa',"")
          alist.append((a + "(" + str(ad) +")"))
    nlist = []
    for n, nd in zip(nouns,nounsD):
        ndr = nd/sum(nounsD)
        if ndr> ndR:
          n = n.replace('2nnn',"")
          nlist.append((n + "(" + str(nd) +")"))
    c_noun1 = c_noun.replace('2nnn','')
    if c_nounD:
      avn2cn = {c_noun1 +"(" + str(c_nounD) +")": [vlist,alist,nlist]}
    else:
      avn2cn = {c_noun1: [vlist,alist,nlist]}
      print('{} degree NOT added'.format(c_noun))
    
    return  avn2cn
