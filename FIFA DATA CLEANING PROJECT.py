#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np


# In[3]:


data = pd.read_csv('fifa21 raw data v2.csv')
data.head(10)


# In[4]:


#displaying hidden columns
pd.set_option("display.max_columns", None)


# In[5]:


data.sample(10)


# In[8]:


data.shape           #checking the shape of data


# In[9]:


data.info()           #checking the missing values in the data set


# In[10]:


data.describe()


# # Data Cleaning

# ## Creating a copy of Dataset

# In[11]:


df = data.copy()
df.head(2)


# ## Club

# #Current club of the player

# In[12]:


df['Club'].dtype


# In[13]:


df['Club'].unique()


# In[14]:


#Removing the invalid spaces

df['Club'] = df['Club'].str.strip()
df['Club'].unique()


# ## 11. Contract 

# #Contract details of the player

# In[15]:


df['Contract'].dtype


# In[16]:


df['Contract'].unique()


# In[17]:


# getting the values which do not match

for i, row in df.iterrows():
    if 'On Loan' in row['Contract'] or 'Free' in row['Contract']:
        print(row['Contract'])


# In[18]:


def contract_info(contract):
    if contract == 'Free' or 'On Loan' in contract:
        start_date = np.nan
        end_date = np.nan
        contract_length = 0
    else:
        start_date, end_date = contract.split(' ~ ')
        start_year = int(start_date[:4])
        end_year = int(end_date[:4])
        contract_length = end_year - start_year
    return start_date, end_date, contract_length

#Applying function to contract column & creating new columns

new_cols = ['Contract Start', 'Contract End', 'Contract Length (years)']
new_data = df["Contract"].apply(lambda x: pd.Series(contract_info(x)))

for i in range(len(new_cols)):
    df.insert(loc=df.columns.get_loc('Contract')+1+i, column=new_cols[i], value=new_data[i])


# In[19]:


df.sample(2)


# In[20]:


df[['Contract', 'Contract Start', 'Contract End', 'Contract Length (years)']].sample(10)


# In[21]:


#Creating contract categories

def category_status(contract):
    if contract == 'Free':
        return 'Free'
    elif 'On Loan' in contract:
        return 'On Loan'
    else:
        return 'Contract'
    
# adding contract Status Column

df.insert(df.columns.get_loc('Contract Length (years)')+1, 'Contract Status', df['Contract'].apply(category_status))


# In[22]:


df.head(10)


# In[23]:


df.tail(10)


# In[24]:


df[['Contract', 'Contract Start', 'Contract End', 'Contract Length (years)', 'Contract Status']].sample(10)


# ## Height

# In[25]:


df['Height'].dtype


# In[26]:


df['Height'].unique()


# In[27]:


def convert_height(height):
    if "cm" in height:
        return int(height.strip("cm"))
    else:
        feet, inches = height.split("'")
        total_inches = int(feet)*12 + int(inches.strip('"'))
        return round(total_inches * 2.54)
    
#applying Fn to Height Column

df["Height"] = df['Height'].apply(convert_height)
df['Height'].unique()


# In[28]:


df = df.rename(columns = {'Height':"Heights(cm)"})
df.sample(2)


# ## Weight

# In[29]:


df['Weight'].dtype


# In[30]:


df['Weight'].unique()


# In[31]:


def convert_weight(weight):
    if "kg" in weight:
        return int(weight.strip("kg"))
    else:
        pounds = int(weight.strip("lbs"))
        return round(pounds/2.205)
    
#Applying fn to the Weight column

df['Weight'] = df['Weight'].apply(convert_weight)
df['Weight'].unique()


# In[34]:


df = df.rename(columns = {'Weight':'Weight(kgs)'})
df.sample(5)


# # Missing Values

# ## Loan Date End 

# In[35]:


#Date when the player's loan ends(incase of Loan)

df['Loan Date End'].dtype



# In[36]:


df['Loan Date End'].unique()


# In[37]:


on_loan = df[df['Contract Status'] == 'On Loan']
on_loan[['Contract', 'Contract Status', 'Loan Date End']]


# #### Hence, we are able to understand why there were missing values in the "Loan Date End" column

# ## W/F

# ### Player's Weak Foot Rating(Out of 5)

# In[39]:


df['W/F'].dtype


# In[40]:


df['W/F'].unique()

# hence, we understand, why the data type is object as the stars are present next to the numbers. 
# It depends on the client requirements and the type of calculations we do in future which will decide whether we want to keep them as it is or remove the stars.

If we want to remove them, then below is the code:
# In[41]:


df['W/F'] = df['W/F'].str.replace('★',"")   # removing the stars using replace method
df['W/F'].unique()


# ## Hits

# In[42]:


#Number of the times the player has been searched for in the FIFA database

df['Hits'].dtypes


# In[43]:


df['Hits'].unique()


# In[ ]:




