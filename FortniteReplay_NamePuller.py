
# coding: utf-8

# In[6]:


filePath = 'C://Users//*USERNAME*//AppData//Local//FortniteGame//Saved//Demos//'
replayFileName = 'TEST_SAMPLE.replay'
#replayFileName = 'UnsavedReplay-2018.09.29-20.01.57.replay'
#replayFileName = 'UnsavedReplay-2018.10.01-21.19.57.replay'

def getStringStripNull(data, idx, len):
    thisString = data[idx:idx+len-1]
    return thisString.decode('utf-8')

def getString3(data, idx):
    length = getInt(data,idx,4)   
    if (length<1):
        return('??????????????')
    return( data[idx+4:idx+length+4].decode('utf-8') )
    

def getInt(data,idx,len):
    #print(data[idx])
    #print(data[idx+1])
    #print(data[idx+2])
    #print(data[idx+3])    
    return(int.from_bytes( data[idx:idx+len], byteorder='little', signed=True ) )


nameList = []


def processPlayerElim(data, idx):
    tag1_len = getInt(data,idx,4)
    
    tag2_len = getInt(data,idx+15,4)
    if (tag1_len!=0x0B or tag2_len!=0x0F):
        print('TAGLEN MISMATCH')
        
    tag1=getStringStripNull(data, idx+4, tag1_len)
    tag2=getStringStripNull(data, idx+19, tag2_len)
    
    if (tag1!='playerElim' or tag2!='versionedEvent'):
        print('TAG MISMATCH', tag1, tag2, len(tag1), len('playerElim'), len(tag2), len('versionedEvent'))    
       

    name1_len = getInt(data,idx+91,4)
    

    


    name2offset = 0
    name1=None
    
    if name1_len<0:
        if name1_len==-7:
            name2offset += 4 + 14
        elif name1_len==-8:
            name2offset += 4 + 16
        else:
            print( 'Neg name 1 len at offset', format(idx,'#04x') )
            print('name1_len', name1_len)
            raise ValueError( 'ENCOUNTERED UNKNOWN NEG PLAYER1 NAME LEN' )
    else:
        name1=getStringStripNull(data, idx+91+4, name1_len)
        name2offset += 4 + name1_len
        
    name2_len = getInt(data,idx+91+name2offset,4)
    name2=None
    
    if name2_len<0:
        print( 'Neg name 2 len at offset', format(idx,'#04x') )
        #print('name2_len',name2_len)
        #raise ValueError( 'ENCOUNTERED UNKNOWN NEG PLAYER2 NAME LEN:' )
    else:
        #print('name2 idx',format(idx+91+name2offset,'#04x') )
        name2=getStringStripNull(data, idx+91+4+name2offset, name2_len)
        
    if name1 is not None:
        nameList.append(name1)        
        
    if name2 is not None:
        nameList.append(name2)

        
    #print(name1,name2)
    
    

with open(filePath + replayFileName, "rb") as binary_file:
    data = binary_file.read()



nextIndex = 0
nameList = []
#print('---------')
while True:
    #print('...')
    nextIndex = data.find( bytes('playerElim','utf-8'),nextIndex+1)
    if nextIndex<0:
        break;
    processPlayerElim(data,nextIndex-4)
    
    
nameList = list(set(nameList))
nameList.sort()
print("Player Count:",len(nameList))
print()
print('PlayerList')
print('----------')
for p in nameList:
    print(p)    
    

