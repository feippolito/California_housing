# dataset:
# http://www.dcc.fc.up.pt/~ltorgo/Regression/cal_housing.html

import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import NearestNeighbors


class Housing:
    def __init__(self):    
        self.housing = pd.read_csv('new_housing.csv',sep=',',decimal='.',encoding='utf-8')
        
        exists = os.path.isfile(r'..\housing\user_data.csv')
        if not exists:
            user_data = pd.DataFrame(columns = ['Name' , 'Email', 'Longitude', 'Latitude', 'Age', 'Total rooms',
                                                'Total bedrooms','Population', 'Households', 'Income', 'Price',
                                                'Ocean proximity', 'n_neighbors'])
            user_data.to_csv (r'..\housing\user_data.csv', index = None, header=True)
            
        
    def encode_fit_transform(self, database):
        
        # one hot encoder for ocean_proximity
        self.onehot = OneHotEncoder(sparse=False, categories= 'auto')
        ocean_labels=database['Ocean proximity'].values.reshape(-1, 1)
        onehot_ocean_labels = self.onehot.fit_transform(ocean_labels)
        
        # concatenate onehot encoded values to dataframe
        dfOneHot = pd.DataFrame(onehot_ocean_labels,
                                columns = ["Ocean_"+str(int(i)) for i in range(onehot_ocean_labels.shape[1])])
        encoded_database = pd.concat([database, dfOneHot], axis=1)
        
        #clean dataframe
        encoded_database.drop('Ocean proximity', axis = 1, inplace = True) #drop ocean_proximity original column
        encoded_database.dropna(axis=0, how='any',inplace = True) #drop NaN
        
        #dataframe columns
        self.columns = encoded_database.columns.tolist()
        
        #normilize values all columns
        self.scaler = MinMaxScaler()
        encoded_database[self.columns] = self.scaler.fit_transform(encoded_database[self.columns])
        return encoded_database
    
    def findKneighbors_fit(self, database):
        self.nNeighbors = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(database)        
    
    def transform(self, sample_df):
        
        #transform
        #onehot encoder
        ocean_labels=self.sample_df['Ocean proximity'].values.reshape(-1, 1)
        onehot_ocean_labels = self.onehot.transform(ocean_labels)
        
        #concatenate onehot encoded values to dataframe
        dfOneHot = pd.DataFrame(onehot_ocean_labels,
                                columns = ["Ocean_"+str(int(i)) for i in range(onehot_ocean_labels.shape[1])])
        encoded_sample = pd.concat([self.sample_df, dfOneHot], axis=1)
        encoded_sample.drop('Ocean proximity', axis = 1, inplace = True) #drop ocean_proximity original column
        
        
        encoded_sample[self.columns] = self.scaler.transform(encoded_sample[self.columns]).astype(float)
        
        return encoded_sample
    
    def findKneighbors(self,sample, n_kneighbors = 5):
        self.housing_ = self.housing.copy(deep = True)
        n_none = [i for i in range(len(sample)) if sample[i] == None]
        
        # Transform list to dataframe
        columns_ = ['Longitude', 'Latitude', 'Age', 'Total rooms', 'Total bedrooms',
                    'Population', 'Households', 'Income', 'Price', 'Ocean proximity']
        
        for index in sorted(n_none, reverse=True):
            del columns_[index]
            del sample[index]
        
        # transform list to dataframe
        self.sample_df = pd.DataFrame(columns = columns_)
        self.sample_df.loc[0] = sample
        
        if len(n_none) != 0:
            #self.sample_df.drop(self.sample_df.columns[n_none],axis=1,inplace=True)
            self.housing_.drop(self.housing_.columns[n_none],axis=1, inplace=True)
        
        self.housing_encoded = self.encode_fit_transform(self.housing_)
        self.findKneighbors_fit(self.housing_encoded)
        
        self.encoded_sample = self.transform(self.sample_df)
        dist, ind = self.nNeighbors.kneighbors(self.encoded_sample, n_kneighbors)
        
        return self.housing.loc[ind[0].tolist()]
    
    def appendTocsv(self,user_id, sample, n_neighbors):
        n_neighbors = [n_neighbors]
        user_data = user_id + sample + n_neighbors
        with open("user_data.csv", "a") as fp:
            wr = csv.writer(fp, dialect='excel')
            wr.writerow(user_data)

