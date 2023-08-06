
from IPython.core.display import display, HTML
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.physics import Physics
from pyvis.network import Network
import time,re,spacy,itertools
from keypartx.basemodes.text_edges import text2edges
import pandas as pd 
import math, matplotlib
from itertools import cycle, islice
import coreferee
nlp = spacy.load('en_core_web_lg')
nlp.add_pipe('coreferee')


## -- avnn edges-- ##
def avnn(comments_en,by_review = False,other_edges = True,verbose_text = False,only_otherNouns = False, only_opiAV = True, nncompound = True):

    time_start = time.time()
    all_adjV2N_edges = []
    allNNedges = [] # noun to noun is the noun in adjV2N 
    all_new_nodes= []
    all_old_nodes= []
    new_node_nouns= []
    new_node_verbs= []
    new_node_adjs= []

    """    by_review = False # by review or by sentence in review
        #opinion_verbs = False
        other_edges = True # not match verb, adj, noun
        verbose_text = False
        only_opiAV = True
        only_otherNouns =only_otherNouns
        nncompound = True"""
        
    for ia,line_ori in enumerate(comments_en):
        print(ia)
        try:
            line = line_ori.replace('\n','') # remove new line in the paragraph
            line = line.replace('\t','')
            line1 = re.sub('[:@#$+=%*`)(><]', ' , ', line)
            #line1 = re.sub(r'\b\d+\b', ' ', line1)
            line1 = re.sub(" \d+", "  ", line1)
            time.sleep(.5)
            line1 = re.sub(r'\b' + "th" + r'\b', ' ', line1) 
            line1 = line1.replace("."," . ") # in case: it is great.the food become a word of great.the
            line1 = line1.replace("!"," . ") # in case: it is great.the food become a word of great.the
            line1 = line1.replace("?"," . ") # ?,!, . for the sentence dependency 
            line1 = re.sub(' +', ' ', line1).strip() #remove extra space whitespace 
            print('line1:', line1)
            if by_review:
                all_adjV2N_edges0, allNNedges0, all_new_nodes0, all_old_nodes0,new_node_nouns0,new_node_verbs0,new_node_adjs0 = text2edges(line1,verbose= False, verbose_text = verbose_text,include_otherEdge = other_edges,only_otherNouns =only_otherNouns,only_opiAV = only_opiAV,nncompound= nncompound)
                #all_adjV2N_edges, allNNedges, all_adjV2N_edges_drop, all_new_nodes, all_old_nodes,new_node_nouns,new_node_verbs,new_node_adjs
                allNNedges.extend(allNNedges0)
                all_adjV2N_edges.extend(all_adjV2N_edges0)
                all_new_nodes.extend(all_new_nodes0)
                all_old_nodes.extend(all_old_nodes0)
                new_node_nouns.extend(new_node_nouns0)
                new_node_verbs.extend(new_node_verbs0)
                new_node_adjs.extend(new_node_adjs0)
            else:
                for ib,sent in enumerate(nlp(line1).sents):   # dependency parse https://spacy.io/usage/linguistic-features#sbd sentence
                    #print(sent)
                    if len(sent.text.split())>2: # minimal 2 words
                        print('sentence' + str(ib),sent.text)
                        all_adjV2N_edges0, allNNedges0, all_new_nodes0, all_old_nodes0,new_node_nouns0,new_node_verbs0,new_node_adjs0 = text2edges(sent.text,verbose_text = verbose_text,include_otherEdge = other_edges,only_otherNouns =only_otherNouns,only_opiAV = only_opiAV,nncompound= nncompound)
                        
                        allNNedges.extend(allNNedges0)
                        all_adjV2N_edges.extend(all_adjV2N_edges0)
                        all_new_nodes.extend(all_new_nodes0)
                        all_old_nodes.extend(all_old_nodes0)
                        new_node_nouns.extend(new_node_nouns0)
                        new_node_verbs.extend(new_node_verbs0)
                        new_node_adjs.extend(new_node_adjs0)
        except:
            print('---sth wrong ---')
        
    print('processing time:', time.time()-time_start)
    return all_adjV2N_edges,allNNedges,all_new_nodes,all_old_nodes,new_node_nouns,new_node_verbs,new_node_adjs


## -- avn network -- ## 
def keynet(all_edges1,heading='avN_N Network',core_K =1,plot_graph = True,save_add ="avnn.html",height='600px', width='100%',bgcolor='white',font_color="black", directed = True, notebook =True):

    # get Networkx 
    #import math
    Gd = nx.DiGraph() 
    #all_edges1 = all_adjV2N_edges_w + allNNEdges_dir_w
    Gd.add_weighted_edges_from(all_edges1)
    print('length Gd nodes: ',len(Gd.nodes))
    #print(Gd.nodes)


    # pyvis network plot 
    nt=Network(height=height, width=width,heading=heading,bgcolor=bgcolor,font_color=font_color, directed = directed, notebook =notebook )
    nt.set_edge_smooth('cubicBezier')
    error_noeds =[]
    nodes = []
    values = []
    for node,degree in dict(Gd.degree).items():
      #degree = math.log(degree,100)
      degree1 = 0.01*degree
      color =""
      shape =""
      node1 = ""
      if 'vvv' in node:
        color = 'red'
        shape = 'square'   # shape  image, circularImage, diamond, dot, star, triangle, triangleDown, square and icon.
        #node1 = node[:-2]
        node1 = re.sub(r'[2][a-zA-Z]{2}',"2",node)
      elif 'aaa' in node:
        color = 'brown'
        shape = 'triangle'
        #node1 = node[:-2]
        node1 = re.sub(r'[2][a-zA-Z]{2}',"2",node)
      elif 'nnn' in node:
        color = 'blue'
        shape = 'dot'
        #node1 = node[:-2]
        node1 = re.sub(r'[2][a-zA-Z]{2}',"2",node)
      else:
        error_node = node
        #print(node)
        Gd.remove_node(error_node)  # remove error node
        error_noeds.append(error_node)
      nodes.append(node[:-2])
      values.append(degree)
      nt.add_node(node1,title = node[:-4].replace('2nnn'," ") +':'+str(degree),value=degree1,color = color, shape =shape) #value=degree
    #nt.add_nodes(nodes, value = values)

    weights = []
    all_edges =[]              # get final all_edges after errors 
    for edge in all_edges1:
      if any(ern in edge for ern in error_noeds):
        print(edge,':error edge removed')

      elif all([dict(Gd.degree)[node]>=core_K for node in edge[:2]]):                   
        elabel = str(edge[2])
        value = int(edge[2])
        weights.append(edge[2])
        edge0 = re.sub(r'[2][a-zA-Z]{2}',"2",edge[0])
        edge1 = re.sub(r'[2][a-zA-Z]{2}',"2",edge[1])
        nt.add_edge(edge0,edge1, title = elabel,width = value)
        #nt.add_edge(edge[0][:-2],edge[1][:-2], title = elabel,width = value)
        all_edges.append(edge)
        
    print('length Gd nodes after error node removed:',len(Gd.nodes))
    print('all edges after k-core: ', len(all_edges))
    
    if plot_graph:
        nt.show_buttons(filter_=['physics']) 
        nt.show("network_map.html")
        display(HTML('network_map.html'))
    if save_add:      
        nt.save_graph(save_add)
    # all_edges after k-core of all_edges1
    return all_edges,Gd



## -- avn network colored by community 
def communet(partition,iGd,Gdc,all_edges,colorList_rgba1,plot_graph = True,save_add ="network_community.html",height='600px', width='100%',heading='Community Network'):
    #import matplotlib

    #from itertools import cycle, islice
    colorList1  = list(islice(cycle(colorList_rgba1),len(partition)))

    ntc=Network(height=height, width=width,heading=heading,bgcolor='white',font_color="black", directed = True, notebook =True)
    ntc.set_edge_smooth('cubicBezier')
    error_noeds =[]
    for com, color in zip(partition, colorList1):
      for index in com:
        
        node = iGd.vs[index]['name']
        #print(node)
        #node1 = node[:-2]
        node1 = re.sub(r'[2][a-zA-Z]{2}',"2",node)

        if 'vvv' in node:
          shape = 'square'   # shape  image, circularImage, diamond, dot, star, triangle, triangleDown, square and icon.
          degree = dict(Gdc.degree)[node]
          title = node +':'+str(degree)
          ntc.add_node(node1,title = node[:-4].replace('2vvv'," ") +':'+str(degree),color = color, value =10*degree, shape =shape) #value=degree

        elif 'aaa' in node:
          shape = 'triangle'
          degree = dict(Gdc.degree)[node]
          title = node +':'+str(degree)
          ntc.add_node(node1,title = node[:-4].replace('2aaa'," ") +':'+str(degree),color = color,value =10*degree, shape =shape) #value=degree
        elif 'nnn' in node:
          shape = 'dot'
          degree = dict(Gdc.degree)[node]
          title = node +':'+str(degree)
          ntc.add_node(node1,title = node[:-4].replace('2nnn'," ") +':'+str(degree),value=100*degree,color = color, shape =shape) #value=degree

    weights = []
    for edge in all_edges:
      elabel = str(edge[2])
      #value = int(edge[2])*.5
      value = math.log(int(edge[2]),2)
      #print(elabel)
      weights.append(edge[2])
      
      edge0 = re.sub(r'[2][a-zA-Z]{2}',"2",edge[0])
      edge1 = re.sub(r'[2][a-zA-Z]{2}',"2",edge[1])
      ntc.add_edge(edge0,edge1, title = elabel,width = value)
      #ntc.add_edge(edge[0][:-2],edge[1][:-2], title = elabel,width = value)
    if plot_graph:
        ntc.show_buttons(filter_=['physics'])  
        ntc.show('example1.html')
        display(HTML('example1.html'))
    if save_add:
        ntc.save_graph(save_add)
        


## --plot color by nouns in AVNN community --#

def communet_nnc(partition,iGd,Gdc,all_edges,colorList_rgba1,plot_graph = True,save_add = 'community_NNColors.html', height='600px', width='100%',heading='Community_NNColors',bgcolor='white',font_color="black", directed = True, notebook =True):
    #import matplotlib,itertools

    partition_all_names = [] 
    for index in partition:
        partition_all_names.append([iGd.vs[index]['name'] for index in index])

    list2d_all =  [x for x in partition_all_names]
    all_nodes_index =  list(itertools.chain(*list2d_all))

    nodes_NN_index = []
    for part in partition_all_names:
      part1 = [x for x in part if 'nnn' in x]
      nodes_NN_index.append(part1)

    other_nodes = [x for x in all_nodes_index if x not in nodes_NN_index ]

    ## all com
    com_a = 0
    com_aa = []
    com_edges =[]
    com_nodes = []
    for com in partition_all_names :
      com_a += 1
      com_aa.append(com_a)
      edges = []
      nodes= []
      for node in com:
        #node = iGd.vs[index]['name']
        #print('nn',node)
        edge = Gdc.in_edges(node)
        edges.append(edge)
        nodes.append(node)
      com_edges.append(edges)
      com_nodes.append(nodes)

    ## nn com 
    colorList1  = list(islice(cycle(colorList_rgba1),len(nodes_NN_index )))

    ntc2 =Network(height=height, width=width,heading=heading,bgcolor=bgcolor,font_color=font_color, directed =directed, notebook =notebook)
    ntc2.set_edge_smooth('cubicBezier')
    com_nn_a = 0
    com_nn_aa = []
    com_nn_edges =[]
    com_nn_nodes = []
    for com_nn, color_nn in zip(nodes_NN_index , colorList1):
      com_nn_a += 1
      com_nn_aa.append(com_nn_a)
      nn_edges = []
      nn_nodes= []
      for node in com_nn:
        
        #node = iGd.vs[index]['name']
        #print('nn',node)
        nn_edge = Gdc.in_edges(node)
        nn_edges.append(nn_edge)
        nn_nodes.append(node)
        #node1 = node[:-2]
        node1 = re.sub(r'[2][a-zA-Z]{2}',"2",node)

        shape = 'dot'
        degree = dict(Gdc.degree)[node]
        title = node +':'+str(degree)
        ntc2.add_node(node1,title = node[:-4].replace('2nnn'," ") +':'+str(degree),value=.5*degree,color = color_nn, shape =shape) #value=degree
      com_nn_edges.append(nn_edges)
      com_nn_nodes.append(nn_nodes)
    for node in other_nodes:
        color = 'gray'
        #node = iGd.vs[index]['name']
        node1 = node[:-2]
        if 'vvv' in node:
          shape = 'square'   # shape  image, circularImage, diamond, dot, star, triangle, triangleDown, square and icon.
          degree = dict(Gdc.degree)[node]
          title = node +':'+str(degree)
          ntc2.add_node(node1,title = node[:-4].replace('2vvv'," ") +':'+str(degree),color = color, value =.1*degree, shape =shape) #value=degree
        elif 'aaa' in node:
          shape = 'triangle'
          degree = dict(Gdc.degree)[node]
          title = node +':'+str(degree)
          ntc2.add_node(node1,title = node[:-4].replace('2aaa'," ") +':'+str(degree),color = color,value =.1*degree, shape =shape) #value=degree
        elif 'nnn' in node:
          shape = 'dot'
          degree = dict(Gdc.degree)[node]
          title = node +':'+str(degree)
          ntc2.add_node(node1,title = node[:-4].replace('2nnn'," ") +':'+str(degree),value=.5*degree,color = color, shape =shape) #value=degree



    weights = []
    for edge in all_edges:
      elabel = str(edge[2])
      #value = int(edge[2])*.5
      value = math.log(int(edge[2]),2)
      #print(elabel)
      weights.append(edge[2])

      edge0 = re.sub(r'[2][a-zA-Z]{2}',"2",edge[0])
      edge1 = re.sub(r'[2][a-zA-Z]{2}',"2",edge[1])
      ntc2.add_edge(edge0,edge1, title = elabel,width = value)

      #ntc2.add_edge(edge[0][:-2],edge[1][:-2], title = elabel,width = value)

    if plot_graph:
        ntc2.show_buttons(filter_=['physics'])  
        ntc2.show('example2.html')
        display(HTML('example2.html'))
    if save_add:
        ntc2.save_graph(save_add)

    com_dict = []
    for com, edges,nodes in  zip(com_aa,com_edges,com_nodes):
        for edge,node in zip(edges,nodes):
            dict1 = {'community_nn':com,'edges':edge,'node':node}
            com_dict.append(dict1)
    nnColor_df = pd.DataFrame(com_dict)
    return nnColor_df



## -single community with gray connection -## 
def gray_unit(nnColor_df,Gdc,all_edges,comLen = False,plot_graph = False, save_folder='gray_units/',height='600px', width='100%',heading='Gray Unit Community Network',bgcolor='white',font_color="black", directed = True, notebook =True):
    if comLen == False:
        com_len = len(set(nnColor_df.community_nn.to_list()))
    else:
        com_len = comLen
    
    commus= []
    colorEdges = []
    colorNodes = []
    grayEdges = []
    grayNodes = []
    
    for community_index in range(com_len):
      com_DF1 = nnColor_df[nnColor_df['community_nn'] == community_index +1]
      comNodes_ori = com_DF1.node.to_list()
      comEdges0 = com_DF1.edges.to_list()
      comNodes= []
      comEdges = []
      for edges in comEdges0:
        for edge in edges:
          comEdges.append(edge)
          for node in edge:
            comNodes.append(node)
      #print(len(comNodes))
      comNodes = sorted(set(comNodes))
      #print(len(comNodes))
      #print(len(comEdges))
      #print(len(set(comEdges)))
      comEdges = sorted(set(comEdges))

      ntc3=Network(height=height, width=width,heading=heading,bgcolor=bgcolor,font_color=font_color, directed = directed, notebook =notebook)
      ntc3.set_edge_smooth('cubicBezier')


      for node in comNodes:
          color_v =""
          color_n = ""
          color_a =""
          if node in comNodes_ori:
            color_v = 'red'
            color_n ='blue'
            color_a ='brown'
          else:
            color_v = 'gray'
            color_n = 'gray'
            color_a = 'gray'
          

          #node = iGd.vs[index]['name']
          #node1 = node[:-2]
          node1 = re.sub(r'[2][a-zA-Z]{2}',"2",node)
          if 'vvv' in node:
            shape = 'square'   # shape  image, circularImage, diamond, dot, star, triangle, triangleDown, square and icon.
            degree = dict(Gdc.degree)[node]
            title = node +':'+str(degree)
            ntc3.add_node(node1,title = node[:-4].replace('2vvv'," ") +':'+str(degree), value =.1*degree, color = color_v,shape =shape) #value=degree
          elif 'aaa' in node:
          
            shape = 'triangle'
            degree = dict(Gdc.degree)[node]
            title = node +':'+str(degree)
            ntc3.add_node(node1,title = node[:-4].replace('2aaa'," ") +':'+str(degree),value =.1*degree, color = color_a,shape =shape) #value=degree
          elif 'nnn' in node:
            shape = 'dot'
            degree = dict(Gdc.degree)[node]
            title = node +':'+str(degree)
            ntc3.add_node(node1,title = node[:-4].replace('2nnn'," ") +':'+str(degree),value=.5*degree,color = color_n, shape =shape) #value=degree
            

      for edge in all_edges:
        for edge1 in comEdges:
          if edge1 == edge[:2]:
            elabel = str(edge[2])
            #value = int(edge[2])*.5
            value = math.log(int(edge[2]),2)
            #print(elabel)

            edge0 = re.sub(r'[2][a-zA-Z]{2}',"2",edge[0])
            edge1 = re.sub(r'[2][a-zA-Z]{2}',"2",edge[1])
            ntc3.add_edge(edge0,edge1, title = elabel,width = value)
            #ntc3.add_edge(edge[0][:-2],edge[1][:-2], title = elabel,width = value)
      if plot_graph:
        ntc3.show_buttons(filter_=['physics']) 
        if community_index == com_len-1: 
            ntc3.show(str(community_index) + 'example3.html')
            display(HTML(str(community_index) + 'example3.html'))
      if save_folder:
        ntc3.save_graph(save_folder+ '/{}.html'.format(community_index +1))

      # gray_color edges dataframe 
      gray_nodes = [x for x in comNodes if x not in comNodes_ori]
      gray_edges = []
      color_edges = []
      for edge in all_edges:
        for edge1 in comEdges:
          if edge1 == edge[:2]:
            if len(gray_nodes)>0:
              for node in gray_nodes:
                if node in edge1:
                  gray_edges.append(edge)
                else:
                  color_edges.append(edge)
            else:
              gray_edges = []
              color_edges.append(edge)

      color_nodes = comNodes_ori
      #if len(gray_nodes)<1:
        #gray_nodes = []
      #set(color_edges),set(color_nodes),set(gray_edges),set(gray_nodes)
      grayNodeDs= []
      for node in gray_nodes:
        degree = dict(Gdc.degree)[node]
        nodeD = (node,degree)
        grayNodeDs.append(nodeD)
      colorNodeDs = []
      for node in color_nodes:
        degree = dict(Gdc.degree)[node]
        nodeD = (node,degree)
        colorNodeDs.append(nodeD)      
    
      
      commus.append(community_index)
      colorEdges.append(set(color_edges))
      colorNodes.append(set(colorNodeDs))
      grayEdges.append(set(gray_edges))
      grayNodes.append(set(grayNodeDs))
    colorGrayDF = pd.DataFrame({'commus': commus,'colorEdges':colorEdges,'colorNodes':colorNodes,'grayEdges':grayEdges,'grayNodes':grayNodes})
    return colorGrayDF