
# coding: utf-8

# In[2]:

import os.path
import pandas as pd
import numpy as np
from datetime import timedelta

class UI_Retention :
    
    def __init__(self, path):
        if os.path.isfile(path) :
            self.path = path
            self.cust_data = pd.DataFrame()
        else :
            sys.exit("Incorrect path")
    
    def Read_CSV(self) :
        self.cust_data = pd.read_csv(self.path)
    
    def Clean_Data(self) :
        #changing the datatype of column to datetime
        self.cust_data['event_time'] = pd.to_datetime(self.cust_data['event_time'])
        #Dropping unnecessary columns
        self.cust_data.drop(['Unnamed: 0','event_count'],1,inplace=True)
        #Considering only "UI_OPEN_COUNT" events
        self.cust_data = self.cust_data[(self.cust_data['event_name'] == 'UI_OPEN_COUNT')]
        #Changing the Datetime format to consider only Date
        self.cust_data['event_time']  = self.cust_data['event_time'].map(pd.Timestamp.date)
        #Dropping duplicated 
        self.cust_data = self.cust_data.drop_duplicates()
        #Creating a new Column "Rank" to extract only the new users on any day
        self.cust_data['Rank'] = self.cust_data.groupby(['user_id','os_name'])['event_time'].rank(ascending=True)
    
    def Calculate_Ret(self,start_date,End_date,OS_name = "ALL" , version = "ALL") :
        temp_date = pd.to_datetime(start_date).date()
        end_date = pd.to_datetime(End_date).date()
        re_open = 0
        total = 0
        os_list = []
        version_list = []


        if OS_name == "IOS" :
            os_list.append(OS_name)
        elif OS_name == "android" :
            os_list.append(OS_name)
        elif OS_name == "ALL" :
            os_list = ["IOS","android"]
        else :
            print ("Incorrect OS Name")

        if version == "1.4.4" :
            version_list.append(version)
        elif version == "1.7.0" :
            version_list.append(version)
        elif version == "1.7.5" :
            version_list.append(version)
        elif version == "ALL" :
            version_list = ["1.4.4","1.7.0","1.7.5"]
        else :
            print ("Incorrect Version")
        
        self.cust_data.shape


        while temp_date <=  end_date :
		
		#Considering only the new users on any day based on the conditions given.
            list_1 = list(self.cust_data[(self.cust_data['event_time'] == temp_date) & (self.cust_data['Rank'] == 1) 
                                & (self.cust_data['os_name'].isin(os_list)) & (self.cust_data['sdk_version'].isin(version_list))]['user_id'])
		
		#Extracting the users exactly after 7 days from the start date to calculate the UI metric
            list_2 = list(self.cust_data[(self.cust_data['event_time'] == temp_date+timedelta(days=7))
                                & (self.cust_data['os_name'].isin(os_list)) & (self.cust_data['sdk_version'].isin(version_list))]['user_id'])
		
		#total number of retained users
            re_open+= len(list(set(list_1).intersection(list_2)))
		
		#total number of new users
            total+= len(list_1)
            temp_date+= timedelta(days=1)
        
		#UI metric calculation
        if total > 0 :
            percent = (float(re_open)/total)*100
        else :
            percent = 0.0
        return format(percent,'.2f')+" %"

        


# In[3]:

data_obj = UI_Retention(r"C:\Users\VISWANATH\Desktop\Aditya\Study\Kamcord\data.csv")


# In[ ]:

# 1 question:
Start_date = input("enter the start date in YYYY-MM-DD format")
End_date = input("enter the end date in YYYY-MM-DD format")
os_name = input("enter the os type(IOS,android)")
version = input("enter the versions(1.4.4,1.7.0,1.7.5)")
data_obj.Calculate_Ret(start_date = Start_date,End_date = End_date ,OS_name = os_name ,version = version)


# In[4]:

# 2 question
data_obj.Read_CSV()


# In[5]:

data_obj.Clean_Data()


# In[6]:

# 3(A) question: What was the overall Day7 UI Retention over the month of September?
data_obj.Calculate_Ret(start_date = '2014-09-01',End_date = '2014-09-30')


# In[7]:

# 3(B) question: What was the Day7 UI Retention from September 8 through September 10 for the Android SDK?
data_obj.Calculate_Ret(start_date = '2014-09-08',End_date = '2014-09-10',OS_name = 'android')


# In[8]:

# 3(C) question: What was the Day7 UI Retention over the month of September for version 1.7.5 of the iOS SDK?
data_obj.Calculate_Ret(start_date = '2014-09-01',End_date = '2014-09-30',OS_name = 'IOS',version='1.7.5')

