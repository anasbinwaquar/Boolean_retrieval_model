import re
# from porter import PorterStemmer
from nltk.stem.porter import *
import os
import pathlib

#StopWord File reading
def preprocessing(stopwords,inverted_index,positional_index):
    path = pathlib.Path(__file__).parent.absolute()     
    path = str(path)
    stopwords_file=open(path + "\\Stopword-List.txt", "r", encoding = "utf-8")
    Lines=stopwords_file.readlines()
    for line in Lines:
        stopwords.append(line.strip()) 
    stopwords=[i for i in stopwords if i]
    stopwords_file.close()

    #DataSet File reading
    temp_dict={}
    # dataset=[[] for x in range (51)]
    dataset=[]
    temp2=''
    i=0
    TC=1    
    Stemmer=PorterStemmer()

    for docid in range(1,51):
        #Reset index for new file
        index=0
        #Read next file
        path = pathlib.Path(__file__).parent.absolute()     
        path = str(path)
        text=open(path+"\\ShortStories\\"+str(docid)+".txt","r",encoding="utf-8")
        temp=text.read()
        temp=temp.lower()
        temp2=temp
        #Regex Matching to remove special characters
        temp=re.sub(r"[-—“”’()\"#:<>{}*`+=~|.!/@;?,]", "", temp)
        temp=temp.split()       
        temp=[word for word in temp if not word in stopwords]
        temp=[ x for x in temp if x]
        #Inverted index
        for t in temp:
                t=Stemmer.stem(t)
                if t in inverted_index:
                    if docid not in inverted_index[t][1]:
                        inverted_index[t][1].append(docid)
                        inverted_index[t][0]=inverted_index[t][0]+1
                else:
                    inverted_index[t]=[]
                    #Doc Freq
                    inverted_index[t].append(1)
                    #Doc IDS
                    inverted_index[t].append([])
                    inverted_index[t][1].append(docid)
        temp=None
        #Positional_index
        #Regex Matching to remove special characters
        temp2=re.sub(r"[-—“”’()\"#:<>{}*`+=~|.!/@;?,]", "", temp2)
        temp2=temp2.split()
        for word in temp2:
            word=Stemmer.stem(word)
            #if exist
            if word in positional_index.keys():
                # print(word)
                positional_index[word][0]=positional_index[word][0]+1
                #If word appeared in same doc or not
                if docid in positional_index[word][1]:
                    positional_index[word][1][docid].append(index)
                #If not create another unique doc entry for doctionary  
                else:
                    positional_index[word][1][docid]=[]
                    positional_index[word][1][docid].append(index)  

            #if not
            else:
                positional_index[word]=[]
                positional_index[word].append(1)
                positional_index[word].append({})
                positional_index[word][1][docid]=[]
                positional_index[word][1][docid]=[index]
            index+=1

        text.close()

def query_processing(query,inverted_index,positional_index):
    query=re.sub(r"[-—“”’()\"#:<>{}*`+=~|.!/@;?,]", "", query)
    query=query.lower().split()
    Stemmer=PorterStemmer()
    last=[]
    words=[]
    operators=[]
    for word in query:
        if word != 'and' and word != 'or':
            words.append(Stemmer.stem(word))
        else:
            operators.append(word.lower())

    for word in words:
        word=Stemmer.stem(word)
    print(words)
    # print(operators)
    x=0
    t=''
    notlist=list(range(1,51))
    #Iterate the query words list to detect and solve proximity queries first
    for x in range(0,len(words)):
        #IF Index is numeric means the query represents proximity query X elements distance
        if words[x].isnumeric():
            words[x-2]=positional_index.get(words[x-2],[])
            words[x-1]=positional_index.get(words[x-1],[])
            #since indexing was done from 0 so add 1 
            t=int(words[x])+1
            #Empty the integer value to append list values for X docs which match proximity criteria
            words[x]=[]
            for l in range(1,51):
                Found=0
                temp=words[x-2][1].get(l,[])
                temp2=words[x-1][1].get(l,[])
                for k in temp:
                    pos=k
                    for i in temp2:
                        ind=pos+t
                        if i==ind:
                            print(l)
                            words[x].append(l)
                            #If found break the loop. no need to check further
                            Found=1
                            break
                        if Found==1:
                            break
                    if Found==1:
                        break
            
                temp2=words[x-2][1].get(l,[])
                temp=words[x-1][1].get(l,[])
                Found=0
                for k in temp:
                    pos=k
                    for i in temp2:
                        ind=pos+t
                        if i==ind:
                            if not (l in words[x]):
                                words[x].append(l)
                                #If found break the loop. no need to check further
                                Found=1
                                break
                        if Found==1:
                            break
                    if Found==1:
                        break
                #Remove duplicate documents
                words[x] = list(dict.fromkeys(words[x]))
            #Condition to handle Not with positional queries
            if words[x-3]=='not':
                words[x]=sorted([i for i in notlist if i not in words[x]])
                words[x-3]=''
            #set empty spaces on the words which were used to make list to remove the empty spaces later for further query
            words[x-1]=''
            words[x-2]=''
    #removing empty spaces from words list 
    print (words)
    while("" in words) :
        words.remove("")
    temp=''
    temp2=''
    print(words)
    x=0
    #Query processing part
    while(1):
        if(x==len(words)):
            break
        else:
            t1=words[x]
            #IF the index type is already list means it was positional query and its been processed already incement X and proceed
            if isinstance(t1, list):
                x+=1
                continue
            elif t1=='not':
                # print('not',words[x+1])
                try:
                    Tlist=inverted_index.get(words[x+1],[])
                    words[x]=sorted([i for i in notlist if i not in Tlist[1]])
                    notlist=list(range(1,51))
                except:
                    words[x]=list(range(1,51))
                del words[x+1]
                x+=1
            else:
                # print(words[x])
                Tlist=inverted_index.get(words[x],[])
                try:
                    words[x]=Tlist[1]
                except:
                    words[x]=[]
                x+=1
    x=0
    C=0
    # print(words)
    # print(operators)
    for op in operators:
        if C==0:
            Tlist=words[x]
            Tlist2=words[x+1]
            if op=='and':
                last=[e for e in Tlist if e in Tlist2]
            elif op=='or':
                for i in Tlist:
                    last.append(i)
                for i in Tlist2:
                    if i not in last:
                        last.append(i)
            last=sorted(last)
            C+=1
            x+=2
        else:
            Tlist=words[x]
            if op=='and':
                last=sorted([e for e in Tlist if e in last])
            elif op=='or':
                for i in Tlist:
                    if i not in last:
                        last.append(i)
            last=sorted(last)
            x+=1
        print('Last ',x,last)

    if len(operators)==0:
        last=words[0]

    return last

    
stopwords=[]
inverted_index = {}
positional_index= {}
preprocessing(stopwords,inverted_index,positional_index)
query='smiling face /2'
ans=query_processing(query,inverted_index,positional_index)
# print(inverted_index)
# print(ans)