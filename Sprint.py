#!/usr/bin/env python
# coding: utf-8

# In[2]:


#Module 6 Week 4 Sprint


# In[1]:


import json
import pymongo as pm
import pandas as pd  


# In[2]:


client = pm.MongoClient("mongodb://localhost:27017/")
myDb = client['Data_Tracker']
collection = myDb["DataVault"]
print(collection)


# In[3]:


stockData = pd.read_csv('Inventory.csv')
print(stockData)


# In[35]:


mongoData = []
n=1
col =stockData.columns
for i in range(len(stockData)):
    row = stockData.iloc[i:n,:]
    template = {}
    for c in col:
        value = row.get_value(index=i,col=c)
        try:
            value = float(value)
        except:
            x=0
        template[c]= value
    mongoData.append(template)
    n+=1

print(len(mongoData),mongoData)


# In[36]:


for item in mongoData:
    #insert = collection.insert_one(item)
    print(item, insert,'\n')


# In[34]:


#Clear documents in collection 
def clearCollection(col):
    x = col.delete_many({})
    print(x.deleted_count,'documents deleted')


# In[22]:


for info in collection.find().sort('Amount',-1):
    print(info)


# In[23]:


#Filtering to display a specific category
searchQuery = {'Category':{'$regex':'CHOCOLATES'}}
chocData = collection.find(searchQuery).sort('Amount',-1)
for choc in chocData:
    print(choc)


# In[37]:


#Create collection of top 3 categories
topCollec = myDb['Top 3']
print(topCollec)
for stuff in mongoData:
    if stuff['Category'] in top3cats:
        some=0
        #insert = topCollec.insert_one(stuff)


# In[38]:


top3data = topCollec.find().sort('Amount',1)
for d in top3data:
    print(d)


# In[33]:


#Deleting entries from top 3
itemsToDel = ['Mutton_Curry','Squash', 'Twista']
for x in itemsToDel:
    del_query = {'Product':{'$regex': x}}
    deletedItems = topCollec.delete_many(del_query)
    print(deletedItems.deleted_count,'items delted')


# In[43]:


#Product to find an update
#object id of item to update :{'_id': ObjectId('5e957c42492b0732c5bd3644')}
result = collection.update_many({'Product': 'Fritos'},
                                {'$inc': {'Amount': 3}}, upsert=True)

# boolean confirmation that the API call went through
print ("acknowledged:", result.acknowledged)

# integer of the number of docs modified
print ("number of docs updated:", result.modified_count)

# dict object with more info on API call
print ("raw_result:", result.raw_result)


# In[48]:


#Search and filter for the least 5 items 

bottom3 = collection.find()
count=0
while count<3:
    for b in bottom3:
        if (b['Amount']<10):
            print(b)
            count+=1
        else:
            continue
        

