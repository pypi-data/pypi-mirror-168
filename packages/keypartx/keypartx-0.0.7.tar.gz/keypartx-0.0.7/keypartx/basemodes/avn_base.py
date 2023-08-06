
import pandas as pd 
import re ,spacy
import coreferee
nlp = spacy.load('en_core_web_lg')
nlp.add_pipe('coreferee')

#1 count frequence of list
def countFreq(my_list,extra_name=""):
# Creating an empty dictionary
    freq = {}
    for item in my_list:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1
    keys =[]
    values = []
    for key, value in freq.items():
        keys.append(key)
        values.append(value)
    keys_name = extra_name
    
    dlist = {keys_name:keys,(keys_name +'_freq'):values}
    df_freq = pd.DataFrame(dlist)
    df_freq = df_freq.sort_values(by= (keys_name +'_freq'), ascending=False)
    return df_freq


#2 coreferee
#import coreferee, spacy
#nlp = spacy.load('en_core_web_lg')
#nlp.add_pipe('coreferee')

#core_text = "Although he was very busy with his work, Peter had had enough of it. He and his wife decided they needed a holiday. They travelled to Spain because they loved the country very much."
def coref(core_text):
  doc = nlp(core_text)
  #doc._.coref_chains.print()
  refs = doc._.coref_chains

  keyNs = []
  key_list =[]
  for ref in refs:
    keyN = ref[ref.most_specific_mention_index]
    if len(keyN)==1:
        key_l = [a[0] for a in list(ref)]
        keyNs.append(keyN[0])
        key_list.append(key_l)

  words_index = {}
  for i, token in enumerate(doc):
    for keyN, keyL in zip(keyNs, key_list):
      if i in keyL and token.tag_ =="PRP":
        #print(token.text)
        word = doc[keyN].text
        words_index.update({i:word})
  words2 = []
  for i, token in enumerate(doc):
    if i in list(words_index):
      word = words_index[i]
    else:
      word = token.text
    words2.append(word)
  coref_text = " ".join(words2)
  return coref_text


#3 lemmatize the words
def lemma_en(text):
    #python -m spacy download en_core_web_sm 
    # Create a Doc object
    #text = "asked I am gone you went to supermarkets to you are bought buy drinks visited and traveled by flying"
    doc = nlp(text)
    
    #lemmatized_text = " ".join([token.text for token in doc if token.text in ['him','her','them'] else token.lemma_])
    words = []
    for token in doc :
      if token.text in ['him','her','them']: # for coreference, otherwise it will be changed to he, she, they
          word = token.text
      else:
        word = token.lemma_
      words.append(word)
       
    lemmatized_text = " ".join(words)

    #print(lemmatized_text)
    return lemmatized_text

def lemma_noun(text):
    #python -m spacy download en_core_web_sm 
    # Create a Doc object
    #text = "asked I am gone you went to supermarkets to you are bought buy drinks visited and traveled by flying"
    doc = nlp(text)
    
    #lemmatized_text = " ".join([token.text for token in doc if token.text in ['him','her','them'] else token.lemma_])
    words = []
    for token in doc :
      if token.pos_ == "NOUN": # for coreference, otherwise it will be changed to he, she, they
          word = token.lemma_
      else:
        word = token.text
      words.append(word)
       
    lemmatized_text = " ".join(words)

    #print(lemmatized_text)
    return lemmatized_text


#4 nouns compund

from spacy.matcher import Matcher
# Matcher is initialized with the shared vocab
def nnncomp(text):
  # Each dict represents one token and its attributes
  matcher = Matcher(nlp.vocab)
  # Add with ID, optional callback and pattern(s)
  pattern = [{"POS": "NOUN"},{"POS": "NOUN","OP":"+"}]
  matcher.add('NA+', [pattern])
  doc = nlp(text)
  # Match by calling the matcher on a Doc object
  matches = matcher(doc)
  # Matches are (match_id, start, end) tuples
  spans =[]
  for match_id, start, end in matches:
      # Get the matched span by slicing the Doc
      span = doc[start:end]
      #print(span.text)
      spans.append(span)
  nnncomp_spans  = spacy.util.filter_spans(spans) # only get the longest span
  nnncomp0 = [x.text for x in nnncomp_spans]
  nnncomp1 = ["".join(x.split()) for x in nnncomp0]
  return nnncomp0,nnncomp1

#5 negative adjective compound
def negadj(textneg,negword):
  matcher = Matcher(nlp.vocab)
  pattern = [{"LOWER": negword}, {"POS": "ADV","OP":"*"},{"POS": "ADJ","OP":"+"}] #"OP":"+" 1 or more * 0 or more
  matcher.add('No+adj', [pattern])

  #textneg = "I do not like you never know it be not really pretty, it means no money no girl"
  doc = nlp(textneg)

  matches = matcher(doc)

  spans =[]
  for match_id, start, end in matches:
      # Get the matched span by slicing the Doc
      span = doc[start:end]
      #print(span.text)
      if len(span.text.split())>1: #not,not pretty
        spans.append(span)
  adj_doc = spacy.util.filter_spans(spans) # only get the longest span

  negadj0 =[]
  negadj1 =[]
  if len(adj_doc)>0:
    for sp in adj_doc:
      negadj0.append(sp.text)
      ss = []
      for s in sp:
        if s.text == negword: # never is adv 
          ss.append(s.text)
        elif s.pos_ == "ADV":
          pass
        else:
          ss.append(s.text)
      negadj1.append("".join(ss))
  else:
    negadj0 =[]
    negadj1 =[]
  #print(negadj0,negadj1, sep="\n")
  return negadj0,negadj1


#6 negative verb compound


def negverb(textneg,negword):
  matcher1 = Matcher(nlp.vocab)
  pattern1 = [{"POS": "AUX","OP":"*"},{"LOWER": negword}, {"POS": "ADV","OP":"*"},{"POS": "VERB","OP":"+"}] #"OP":"+" 1 or more * 0 or more
  matcher1.add('No+verb', [pattern1])
  pattern2 = [{"POS": "AUX","OP":"*"},{"LOWER": negword}, {"POS": "ADV","OP":"*"},{"LOWER":"like"}] #"OP":"+" 1 or more * 0 or more
  matcher1.add('No+verb2', [pattern2])

  #textneg = "I do not like you never know it be not really pretty, it means no money no girl"
  doc = nlp(textneg)
  matches = matcher1(doc)
  spans =[]
  for match_id, start, end in matches:
      # Get the matched span by slicing the Doc
      span = doc[start:end]
      #print(span.text)
      if len(span.text.split())>1: #not,not like
        spans.append(span)
  verb_doc = spacy.util.filter_spans(spans) # only get the longest span
  #print('verb_doc:',verb_doc)
  negverb0 =[]
  negverb1 =[]
  if len(verb_doc)>0:
    for sp in verb_doc:
      ss = []
      ss1 = []
      for s in sp:
        if s.pos_ == "AUX":
          ss.append(s.text)
        elif s.text == negword: # never is adv 
          ss.append(s.text)
          ss1.append(s.text)
        elif s.pos_ == 'ADV':
          ss.append(s.text)
        else:
          ss.append(s.text)
          ss1.append(s.text)
      negverb0.append(" ".join(ss))
      negverb1.append("".join(ss1))
  else:
    negverb0 =[]
    negverb1 =[]
  #print(negverb0,negverb1, sep="\n")
  return negverb0,negverb1

#7 merg quoted words

def quote(text):
  quote0 = []
  quote1 = []
  for qt in re.findall(r'"(.*?)"', text): # double quote
    if len(qt.split())<4: # in case there's xxxxx it's 
      qt1 = re.sub(r'[^\w\s]', '', qt) # remove punct in quotes "good-good"
      qtj = "".join(qt1.split())
      quote0.append(qt)
      quote1.append(qtj)
  for qt in re.findall(r"'(.*?)'", text): # single quote
    if len(qt.split())<4:
      qt1 = re.sub(r'[^\w\s]', '', qt) # remove punct in quotes 'good-good'
      qtj = "".join(qt1.split())
      quote0.append(qt)
      quote1.append(qtj)
  #print(quote0,quote1)
  return quote0,quote1

#8 hyphenated and entity words
# hyphenated words
def hyphen(text):
  hypen0 = re.findall("((?:\w+-)+\w+)",text) 
  hypen1= []
  for hyp in hypen0:
    hypj = "".join(hyp.split('-'))
    hypen1.append(hypj)
  #print(hypen0,hypen1)
  return hypen0,hypen1

# entity words 
def entity(text):
  doc = nlp(text)
  entity0 =[]
  entity1 = []
  for ent in doc.ents:
      #print(ent.text, ent.start_char, ent.end_char, ent.label_)
      entt = ent.text
      entity0.append(entt)
      enttj = "".join(entt.split())
      entity1.append(enttj)
  #print(entity0,entity1)
  return entity0,entity1

#9 n't lemmatize(ntverb)
# (ntwerb)change n't to not Apostrophe
def ntverb(text1):
  ntverb0 = []
  ntverb1 =[]
  for word in text1.split():
    if "n’t" in word:
      #print(word)
      ntverb0.append(word)
      ntverb1.append(lemma_en(word))
    elif "n't" in word:
      #print(word)
      ntverb0.append(word)
      ntverb1.append(lemma_en(word))

  #print(ntverb0,ntverb1)
  return ntverb0,ntverb1

#10 remove coma in Adj,Adj
def nonAcomaA(text1):
  #text1 = 'wonderful, beautiful and great country'
  text1 = text1 + "  "  # in case "wonderful," sentence, then there will be no poss[i+2]
  cols = ['index','word','pos']
  rows =[]
  for d in nlp(text1):
    row = d.i,d.text,d.pos_
    rows.append(row)
    #print(row)

  df = pd.DataFrame(rows, columns=cols)
  words = df.word.to_list()
  poss = df.pos.to_list()
  indexs = df.index.to_list()
  index_drop = []
  for i in range(len(df)-1):
    if words[i+1] =="," and poss[i] == poss[i+2]=="ADJ":
      #print(words[i:i+2])
      index_drop.append(indexs[i+1])

  df2 = df.drop(index_drop)
  nonAcomaA_sent = ' '.join(df2.word.to_list())
  return nonAcomaA_sent 

#11 av2n and nn edges
import itertools
def av2Nedge(adjNverbs2): # adjNverbs2 must be list
  av2Nedges =[]
  all_nouns1 = [] # nouns in adjVn edges 
  
  for anbs in adjNverbs2:
    cols = ['word','pos']
    rows=[]
    for anb in nlp(anbs):
      #print(anb.text,anb.pos_)
      if anb.text =='be':
        row = 'be','VERB'
      else:
        row = anb.text,anb.pos_
      rows.append(row)
    df_wp = pd.DataFrame(rows,columns =cols)
    nouns = df_wp[df_wp['pos'] == 'NOUN'].word.to_list()
    #all_nouns1.extend(nouns) 
    notNs = df_wp[df_wp['pos'] != 'NOUN'].word.to_list()
    for adjV in notNs:
      if adjV !='be':
        for nn in nouns:
          #print(adjV,nn)
          av2Nedges.append([adjV,nn])
          all_nouns1.append(nn)
  if len(all_nouns1)>1:
    nn_edges = list(itertools.combinations(set(all_nouns1), 2)) #noun noun edges edge
  else:
    nn_edges =[]

  return av2Nedges, nn_edges

#12 (mapnoun,mapadj,mapverb)mapping new words 
def mapnoun(new_textn,verbose = False):
  doc1 = nlp(new_textn)
  for token in doc1:
    if verbose:
      print(token.text,token.pos_,token.tag_, token.dep_)
    
  for comp in new_textn.split():
    # Add attribute ruler with exception for "The Who" as NNP/PROPN NNP/PROPN
    ruler = nlp.get_pipe("attribute_ruler")
    # Pattern to match "The Who"
    patterns = [[{"LOWER": comp.lower()}]]
    # The attributes to assign to the matched token
    attrs = {"TAG": "NNP", "POS": "NOUN",}
    # Add rules to the attribute ruler
    ruler.add(patterns=patterns, attrs=attrs)  # "The" in "The Who"
  if verbose:
    print('---')
  doc2 = nlp(new_textn)
  for token in doc2:
    if verbose:
      print(token.text,token.pos_,token.tag_, token.dep_)
  if verbose:
    print('---noun---')
def mapadj(new_textadj,verbose = False):
  doc1 = nlp(new_textadj)
  for token in doc1:
    if verbose:
       print(token.text,token.pos_,token.tag_, token.dep_)
    
  for comp in new_textadj.split():
    # Add attribute ruler with exception for "The Who" as NNP/PROPN NNP/PROPN
    ruler = nlp.get_pipe("attribute_ruler")
    # Pattern to match "The Who"
    patterns = [[{"LOWER": comp.lower()}]]
    # The attributes to assign to the matched token
    attrs = {"TAG": "NNP", "POS": "ADJ"}
    # Add rules to the attribute ruler
    ruler.add(patterns=patterns, attrs=attrs)  # "The" in "The Who"
  if verbose:
      print('---')
  doc2 = nlp(new_textadj)
  for token in doc2:
    if verbose:
        print(token.text,token.pos_,token.tag_, token.dep_)
  if verbose:
    print('---neg adj---')

def mapverb(new_textverb,verbose = False):
  doc1 = nlp(new_textverb)
  for token in doc1:
    if verbose:
        print(token.text,token.pos_,token.tag_, token.dep_)
    
  for comp in new_textverb.split():
    # Add attribute ruler with exception for "The Who" as NNP/PROPN NNP/PROPN
    ruler = nlp.get_pipe("attribute_ruler")
    # Pattern to match "The Who"
    patterns = [[{"LOWER": comp.lower()}]]
    # The attributes to assign to the matched token
    attrs = {"TAG": "NNP", "POS": "VERB",}
    # Add rules to the attribute ruler
    ruler.add(patterns=patterns, attrs=attrs)  # "The" in "The Who
  if verbose:
    print('---')
  doc2 = nlp(new_textverb)
  for token in doc2:
    if verbose:
       print(token.text,token.pos_,token.tag_, token.dep_)
  if verbose:
       print('---neg verb---')
       
#13 (adjNVmatch) match AdjN,NbeAdj,Nverb,verbN
from spacy.matcher import Matcher
def adjNVmatch(text5):
  # Matcher is initialized with the shared vocab
  #from spacy.matcher import Matcher
  # Each dict represents one token and its attributes
  matcher = Matcher(nlp.vocab)
  # Add with ID, optional callback and pattern(s)

  pattern = [{"POS": "NOUN","OP":"+"},{"LOWER": "be","OP":"+"}, {"POS": "ADV","OP":"*"},{"POS": "ADJ","OP":"+"}] #"OP":"+" 1 or more * 0 or more # ugly and expensive ugly is adj, ugly expensive ugly is adv
  matcher.add('NA+adj', [pattern])
  #pattern2 =[{"LIKE_EMAIL":True}]
  pattern2 = [{"POS": "ADJ","OP":"+"},{"POS": "NOUN","OP":"+"}]
  matcher.add('A+N', [pattern2])

  pattern3 = [{"POS": "VERB"},{"POS": "NOUN","OP":"+"}]
  matcher.add('V+N', [pattern3])

  pattern4 = [{"POS": "NOUN","OP":"+"},{"LOWER": "be","OP":"+"},{"POS": "VERB"}]
  matcher.add('N+V', [pattern4])

  #doc = nlp("restaurantfood be nice expensive food like nice expensive , company be recommend,address , the price-quality ration is not quite right, soon cafe be hot cool massage place, beautiful destination, I like hotel")
  doc = nlp(text5)
  matches = matcher(doc)
  # Matches are (match_id, start, end) tuples
  spans =[]
  for match_id, start, end in matches:
      # Get the matched span by slicing the Doc
      span = doc[start:end]
      #print(span.text)
      spans.append(span)
  adjNverbs1 = spacy.util.filter_spans(spans) # only get the longest span
  adjNverbs2 = [x.text for x in adjNverbs1]
  return adjNverbs2 



