#!/usr/bin/env python
# coding: utf-8

#importing libraries
from ast import parse
from time import time
from sqlalchemy import create_engine
import pandas as pd
import argparse 
import os
parser = argparse.ArgumentParser()



def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table = params.table
    path = params.path

    #creating the python-database connection
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    #converting the parquet file to csv, will see why in following codes
    pd.read_parquet(path,engine = "pyarrow").to_csv("output.csv", index = False)
    print("Finished Converting the parquet file to csv")

    #Processing data in chunks
    df_iter = pd.read_csv("output.csv", iterator=True, chunksize=100000)
    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    #adding the column names
    df.head(n=0).to_sql(name=table, index = False , con=engine, if_exists="replace") 

    t_start = time()
    # adding the first batch of rows
    df.to_sql(name=table, index = False, method = "multi", con=engine, if_exists="append")
    t_end = time()
    print('First Batch of data process, time took %.3f second' %(t_end - t_start))

    print("======================================================================")
    
    print('Ingestion of rest of the data started')


    # Iteration to ingest rest of the data
    while True:
        try:
            t_start = time()
            df = next(df_iter)

            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

            df.to_sql(table, index=False, method = "multi", con=engine, if_exists='append')

            t_end = time()

            print('inserted another chunk, took %.3f second' %(t_end - t_start))
        except StopIteration:
            print("Finished ingesting data into the postgres database")
            os.remove("output.csv")
            break


if __name__ == '__main__':
    parse = argparse.ArgumentParser("Data Ingestion to Postgres")

    # user
	# password
	# host
	# port
	# database name
	# table name
	# path of the parquet file

    parser.add_argument('--user', help="user name for postgres")
    parser.add_argument('--password', help="password for postgres")
    parser.add_argument('--host', help="host for postgres")
    parser.add_argument('--port', help="port for postgres")
    parser.add_argument('--db', help="database name for postgres")
    parser.add_argument('--table', help="name of the table where we will write the results to")
    parser.add_argument('--path', help="path of the file")

    args = parser.parse_args()
    main(args)