#!/usr/bin/env python
# coding: utf-8

# dataset:
# http://www.dcc.fc.up.pt/~ltorgo/Regression/cal_housing.html

# In[13]:


import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import NearestNeighbors


# In[14]:


class Housing:
    def __init__(self):
        self.housing = pd.read_csv('housing.csv',sep=',',decimal='.',encoding='utf-8')
        self.housing_encoded = self.encode_fit_transform(self.housing)
        
        self.findKneighbors_fit(self.housing_encoded)
        
    def encode_fit_transform(self, database):
        
        #one hot encoder for ocean_proximity
        self.onehot = OneHotEncoder(sparse=False, categories= 'auto')
        ocean_labels=database.ocean_proximity.values.reshape(-1, 1)
        onehot_ocean_labels = self.onehot.fit_transform(ocean_labels)
        
        #concatenate onehot encoded values to dataframe
        dfOneHot = pd.DataFrame(onehot_ocean_labels,
                                columns = ["Ocean_"+str(int(i)) for i in range(onehot_ocean_labels.shape[1])])
        encoded_database = pd.concat([database, dfOneHot], axis=1)
        
        #clean dataframe
        encoded_database.drop('ocean_proximity', axis = 1, inplace = True) #drop ocean_proximity original column
        encoded_database.dropna(axis=0, how='any',inplace = True) #drop NaN
        
        #dataframe columns
        self.columns = encoded_database.columns.tolist()
        
        #normilize values all columns
        self.scaler = MinMaxScaler()
        encoded_database[self.columns] = self.scaler.fit_transform(encoded_database[self.columns])
        
        return encoded_database
    
    def findKneighbors_fit(self, database):
        self.nNeighbors = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(database)        
    
    def transform(self, sample):
        columns_ = ['longitude', 'latitude', 'housing_median_age', 'total_rooms',
                    'total_bedrooms', 'population', 'households', 'median_income',
                    'median_house_value', 'ocean_proximity']

        #transform list to dataframe
        sample_df = pd.DataFrame(columns = columns_)
        sample_df.loc[0] = sample
        
        #transform
        #onehot encoder
        ocean_labels=sample_df.ocean_proximity.values.reshape(-1, 1)
        onehot_ocean_labels = self.onehot.transform(ocean_labels)
        
        #concatenate onehot encoded values to dataframe
        dfOneHot = pd.DataFrame(onehot_ocean_labels,
                                columns = ["Ocean_"+str(int(i)) for i in range(onehot_ocean_labels.shape[1])])
        encoded_sample = pd.concat([sample_df, dfOneHot], axis=1)
        
        encoded_sample.drop('ocean_proximity', axis = 1, inplace = True) #drop ocean_proximity original column
        
        
        encoded_sample[self.columns] = self.scaler.transform(encoded_sample[self.columns]).astype(float)
        
        return encoded_sample
    
    def findKneighbors(self,sample, n_kneighbors = 5):
        self.encoded_sample = self.transform(sample)
        dist, ind = self.nNeighbors.kneighbors(self.encoded_sample, n_kneighbors)
        return self.housing.loc[ind[0].tolist()]
        


# house1 = Housing()

# datatable1 = house1.findKneighbors([-120.24,
#  32.85,
#  54.0,
#  1467.0,
#  190.0,
#  496.0,
#  177.0,
#  7.2574,
#  352100.0,
#  'NEAR BAY'], 10)