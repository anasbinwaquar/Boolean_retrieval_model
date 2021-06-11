import re
from porter import PorterStemmer

#StopWord File reading
def preprocessing(stopwords,inverted_index,positional_index):
    stopwords_file=open('Stopword-List.txt','r')
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
        text=open('ShortStories/'+str(docid)+'.txt','r',encoding="utf8")  
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
                    positional_index[word][1][docid].append([index])
                #If not create another unique doc entry for doctionary  
                else:
                    positional_index[word][1][docid]=[]
                    positional_index[word][1][docid].append([index])  

            #if not
            else:
                positional_index[word]=[]
                positional_index[word].append(1)
                positional_index[word].append({})
                positional_index[word][1][docid]=[]
                positional_index[word][1][docid]=[index]
            index+=1

        text.close()

# print(inverted_index['veri'])
# inverted_index=sorted(inverted_index.items())
# positional_index=sorted(positional_index.items())

last=[]
temp=[]
templist=[]
Tlist=[]
Tlist2=[]
notlist=list(range(1,51))
stopwords=[]
inverted_index = {}
positional_index= {}
preprocessing(stopwords,inverted_index,positional_index)
query='god and man and love'
query=query.lower().split()
Stemmer=PorterStemmer()
words=[]
operators=[]
for word in query:
    if word != 'and' and word != 'or':
        words.append(Stemmer.stem(word))
    else:
        operators.append(word)

for word in words:
    word=Stemmer.stem(word)

x=0
while(1):
    if(x==len(words)):
        break
    else:
        t1=words[x]
        if t1=='not':
            print('not',words[x+1])
            Tlist=inverted_index.get(words[x+1])
            words[x]=sorted([i for i in notlist if i not in Tlist[1]])
            notlist=list(range(1,51))
            del words[x+1]
            x+=1
        else:
            print(words[x])
            Tlist=inverted_index.get(words[x])
            words[x]=Tlist[1]
            x+=1

print(words)
print(operators)


x=0
C=0
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
        print(last)
        C+=1
        x+=2
    else:
        Tlist=words[x]
        if op=='and':
            last=sorted([e for e in Tlist if e in last])
        elif op=='or':
            for i in Tlist:
                if i not in last:
                    last.append(Tlist)
        last=sorted(last)
        x+=1
    print('Last ',x,last)

if len(operators)==0:
    last=words[0]
print(last)










# print(notlist)
# for x in range(0,len(operators)):
#     if(C==0):
#         t1=words.pop()
#         t2=words.pop()
#         Tlist=inverted_index.get(t1)
#         Tlist2=inverted_index.get(t2)
#         if operators[x]=='not':
#             Tlist[1]=sorted([i for i in notlist if i not in Tlist[1]])
#             print(Tlist[1])
#         if operators[x+2]=='not':
#             notlist=list(range(1,51))
#             Tlist2[1]=sorted([i for i in notlist if i not in Tlist2[1]])
#             print(Tlist2[1])
#         if operators[x+1]=='and':
#             last=[e for e in Tlist[1] if e in Tlist2[1]]
#         elif operators[x+1]=='or':
#             last.append(Tlist[1])
#             last.append(Tlist2[1])
#         # print(last)
#         x+=3
#         C+=1
#     else:  
#         print(operators[x])
        # Tlist=[]
        # t1=words.pop()  
        # Tlist=inverted_index.get(t1)
        # if operators[x]=='and':
        #     for w1 in Tlist[1]:
        #         if w1 in last and w1 in Tlist[1]:
        #             temp.append(w1)
        # last=temp
        # if operators[x]=='or':
        #     for w1 in Tlist[1]:
        #         last.append(w1)
    # C+=1

# print(sorted(last))