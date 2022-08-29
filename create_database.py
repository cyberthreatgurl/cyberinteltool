#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 18:52:36 2022

@author: kdawg
"""

import psycopg2
from psycopg2 import Error

try:
    connection = psycopg2.connect(user="kdawg",
                                  password="",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="kdawg")

    cursor = connection.cursor()
    # SQL query to create a new table
    create_table_query = '''CREATE TABLE patents
          (ID INT PRIMARY KEY     NOT NULL,
          filename TEXT           NOT NULL,
          contents TEXT           ); '''
    # Execute a command: this creates a new table
    cursor.execute(create_table_query)
    connection.commit()
    print("Table created successfully in PostgreSQL ")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if connection:

        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

