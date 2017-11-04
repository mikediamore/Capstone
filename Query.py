#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 13:19:32 2017

@author: Michael Di Amore
"""


from pandas import read_gbq
import pandas as pd
import pandas_datareader.data as web
import quandl
import json


"""
##############
README FIRST
#############

Goal:
-----
Create Python querying classes to aid the Capstone group in first pass 
data analysis. Maybe use this tool first before moving completely to spark 
or for inital data exploration.

Prerequisites:
------
First set up your google api to bigquery and set up a project name. There are 
instructions all over the internet but here's a useful guide for ubuntu.

    https://cloud.google.com/sdk/docs/quickstart-debian-ubuntu
    https://pandas-gbq.readthedocs.io/en/latest/install.html#dependencies

You might need to install the google big query library but I think we can work 
directly via pandas for now. You might also need to set up a "Service Account Key"
Go to Credentials in your google cloud platform. I'm not sure if this is necessary
in our current state but might be later? 

You'll also need to install the quandl library, I thought it might be an interesting
data source to use there's lots of macroeconomic data there for free.  See this
as an example:
    
    https://www.quandl.com/data/FRED-Federal-Reserve-Economic-Data


Usage:
------
Simply call the query method of the class to query big query by passing an SQL
type query through the method you should get a message with a link redirecting you
to authorize the query (this only needs to be done once per python session)


To do:
-----
If we find the financial indicators to of the FRED index from quandl to be 
relevant we can download all of them instead of passing FRED/GDP, FRED/DFF since
that's very inefficient

Find a way to streamling querying so we don't have to go to google to authenticate it
on the first run


Ideas:
-----
I think we can use the FRED database to give us macroeconomic indicators to predict
GDP, Fed Funds Rate, that's on a high level. On a lower level if we can predict
changes in the VIX index we can effectively predict market movements in general
which I think would be the ultimate solution. An estimate of market volatility
will affect all things from consumer spending, corporate borrowing, etc.

"""


class query_tool():
    """
    Query Tool to use on Gdelt, Yahoo, and quandl data sets
    basically just pandas wrappers. I figured this was a good first step
    
    Parameters:
    -----------
        proj_id : String project name, allows for setting up your own project 
                    to test with.
        start_date : Start Date as string ex: '2017-10-01'
        end_date : End Date as string ex : '2017-12-31'
        ticker: Can be None, but is used for quandl and yahoo query
    
    """
    
    def __init__(self,proj_id,start_date,end_date,ticker):
        
        self.proj_id = proj_id
        self.start_date = start_date
        self.end_date = end_date
        self.ticker = ticker
    
    
    def query_gdelt(self,query):
        """
        Pass a SQL-like query as string into this function to query the gdelt 
        
        Example query:
        SELECT V2Tone,DATE FROM [gdelt-bq:gdeltv2.gkg] 
        where DATE > 20170801000000and DATE < 20170805000000 
        and V2Themes like '%WB_332%'
        
        Here WB_332 is a World Bank Code, see the GDELT documentation for more
        information.
        """
        
        self.query = query
        df = read_gbq(query,self.proj_id,reauth=False)
        self.gdelt_df = df
        return(df)

    def query_yahoo(self):
        """
        Queries Yahoo to get EoD prices for a particular security. Might also
        be able to get relevant indices like the VIX or SPY using ^VIX or ^SPY
        
        """
        
        df = web.DataReader(self.ticker, 'yahoo', self.start_date, self.end_date)
        self.yahoo_df = df
        return(df)


    def query_quandl(self,api_code,auth_key):
        """"
        Queries the quandl database you provide via the api code
        given your authentication key. Quandl accounts are free.
        
        I DO NOT STORE THE AUTH_KEY it's bad practice to store passcodes.
        Just pass it as a var in your interpreter and make sure its gone
        before posting to github
        
        Example API CODE: FRED/GDP, FRED/DFF
        """
        
        self.api_code = api_code
        df = quandl.get(self.api_code, start_date=self.start_date, 
                                            end_date=self.end_date,authtoken=auth_key)
        self.quandl_df = df
        return(df)
        

    def set_ticker(self,ticker):
        """
        Useful for setting a ticker that was previous None, i.e. you wanted to query
        gdelt but now you want to query yahoo and don't wnat to do  query_tool.ticker = XXX
        this is just a wrapper
        """
        self.ticker = ticker
        
        
    
    def __getattribute__(self,attr):
        """
        Useful bit of code, returns none if you call an attribute that doesn't
        exist
        """
        
        try:
            return object.__getattribute__(self, attr)
        except AttributeError:
            return None
        
    def save_gdelt_df(self,name,save_type='csv',h5_dict_name=None):
        """
        Save down the gdelt_df given a name note the csv/h5 extension is not
        needed as it's automatically appended
        
        For larger datasets we might want to save down as h5 so that's included
        as well
        """
        
        if save_type == 'csv':
            self.gdelt_df.to_csv(name+'.csv')
        elif save_type == 'h5':
            self.gdelt_df.to_hdf(name+'.h5',h5_dict_name,format='table',mode='w')
        
def load_json(path):
    """
    Helper function to properly load a JSON
    """
    
    with open(path, 'r') as f:
        data = json.load(f)
    return(data)


    
    

if __name__ == '__main__':
    project_id = 'capstone-v0'
    start = '2017-10-01'
    end = '2017-10-05'
   
    
    #big_query_key = pd.read_json('Capstone-v0-8b4dcea9e181.json',typ='series')
#    big_query_key  = load_json('Capstone-v0-8b4dcea9e181.json')
#    
    quandl_api_key =  pd.read_table('quandl_code.txt')
    test_tool = query_tool(project_id,start,end,'SPX')
    
    
    example_query = """SELECT V2Tone,DATE FROM [gdelt-bq:gdeltv2.gkg] 
                    where DATE > 20170801000000and DATE < 20170803000000 
                    and V2Themes like '%WB_332%'
                    """
    test_tool.query_gdelt(example_query)
    