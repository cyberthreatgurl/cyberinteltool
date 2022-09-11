#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 18:52:36 2022

@author: kdawg
"""
import logging
import psycopg2
from psycopg2 import Error

def create_database():
    try:
        connection = psycopg2.connect(user="kdawg",
                                      password="",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="kdawg")

        cursor = connection.cursor()

        cursor.execute("DROP TABLE IF EXISTS PATENTS")

        # SQL query to create a new table
        create_table_query = '''CREATE TABLE patents
              (FILE_ID SERIAL PRIMARY KEY NOT NULL,
              filename TEXT           NOT NULL,
              contents TEXT           ); '''
        # Execute a command: this creates a new table
        cursor.execute(create_table_query)
        connection.commit()
        logging.info("Table created successfully. ")

    except (Exception, Error) as error:
        logging.debug("Error %s while connecting to PostgreSQL", error)
        print('Error while connecting to PostgreSQL', error)
    finally:
        if connection:

            cursor.close()
            connection.close()
            logging.info("PostgreSQL connection closed.")

def database_exists():
    try:
        connection = psycopg2.connect(user="kdawg",
                                      password="",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="kdawg")

        cursor = connection.cursor()
    except (Exception, Error) as error:
        logging.debug("Error while connecting to PostgreSQL", error)
    finally:
        if connection:

            cursor.close()
            connection.close()
            logging.info("PostgreSQL connection is closed")

def record_exists(file_name):
    # open db
    try:
        connection = psycopg2.connect(user="kdawg",
                                      password="",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="kdawg")

        cursor = connection.cursor()
        # Executing a SQL query to insert data into  table
        insert_query = "select FILE_ID, FILENAME from patents where filename = %s"
        cursor.execute(insert_query,file_name)
        return cursor.fetchone() is not None
    except (Exception, psycopg2.Error) as error:
        logging.debug("Error while querying the database: ", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            logging.info("PostgreSQL connection is closed")

def pdf_database_write(file_name,extracted_text):
    
    try:
        connection = psycopg2.connect(user="kdawg",
                                      password="",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="kdawg")

        cursor = connection.cursor()
        # Executing a SQL query to insert data into  table
        insert_query = "INSERT INTO patents (FILENAME, CONTENTS) VALUES(%s,%s)"
        cursor.execute(insert_query, (file_name, extracted_text))
        connection.commit()
        logging.info("1 Record inserted successfully")
        # Fetch result
        #cursor.execute("SELECT * from patents")
        #record = cursor.fetchall()
        #print("Result ", record)


    except (Exception, psycopg2.Error) as error:
        logging.debug("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            logging.info("PostgreSQL connection is closed")