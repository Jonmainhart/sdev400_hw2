"""
dynamolib.py

Jonathan Mainhart
SDEV 400
14 Sep 2021

Library of functions to interact with aws dynamoDB for homework 2.

Much of this code is courtesy of the examples provided by Amazon AWS team. Code snippets
are annotated throughout this file. Any snippets used are in compliance with the Apache
License, Version 2.0 as stipulated in the original work. A copy of the license is
available at https://aws.amazon.com/apache2.0
"""
import logging
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
db_client = boto3.client('dynamodb')

# table of certain name exists
def table_exists(table_name):
    """
    Checks if a table exists with a given name.
    :param table_name: str
    :return: True if table exists, otherwise False
    
    Some portions of this code Copyright 2010-2019 
    Amazon.com, Inc. or its affiliates. All Rights Reserved.
    
    MoviesListTables.py
    """
    tables_available = []
    for table in dynamodb.tables.all():
        tables_available.append(table.name) # Amazon
    if table_name in tables_available:
        return True
    return False
    
# create table of certain name with parameters
def create_course_table():
    """
    Creates the courses table for homework2
    :return: True if succuessful, otherwise False
    
    Some portions of this code Copyright 2010-2019 
    Amazon.com, Inc. or its affiliates. All Rights Reserved.
    
    MoviesCreateTable.py
    """
    dynamodb.create_table(
        TableName='Courses',
        KeySchema=[
        {
            'AttributeName': 'CourseID',
            'KeyType': 'HASH'  
        }
        ],
         AttributeDefinitions=[
        {
            'AttributeName': 'CourseID',
            'AttributeType': 'N'
        }
        ],
        ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
        }
        )

# populate table with course information
def populate_item(table_name, course_info):
    """
    Adds an item to the the dynamodb table.
    :param table_name: str
    :param course_info: list []
    
    Some portions of this code Copyright 2010-2019 
    Amazon.com, Inc. or its affiliates. All Rights Reserved.
    
    MoviesItemOps01.py
    """
    Subject, CatalogNbr, Title, Credits, CourseID = course_info
    
    try:
        if dynamodb.Table(table_name).put_item(
        Item={
            'Subject': Subject,
            'CatalogNbr': CatalogNbr,
            'Title': Title,
            'Credits': Credits,
            'CourseID': CourseID
        }
        ):
            return True
    except Exception as e:
        logging.debug(e)
    return False
  
# query function which returns course description based on subject and course number
def get_course_title(subject, catalog_num):
    """
    Gets course title from Courses table. Returns course title.
    :param subject: str
    :param catalog_num: int
    :return: str
    
    Some portions of this code Copyright 2010-2019 
    Amazon.com, Inc. or its affiliates. All Rights Reserved.
    
    MoviesScan.py
    """

    try:
       # scan and filter
       response = dynamodb.Table('Courses').scan(
           FilterExpression=Attr("Subject").eq(subject) & Attr("CatalogNbr").eq(catalog_num),
           ProjectionExpression=("Title")
           )
       
       title = [item.get('Title') for item in response['Items']][0]
       return title
       
    except Exception as e:
        logging.debug(e)
    