"""
menu.py

Jonathan Mainhart
SDEV 400
14 Sep 2021

Menu functions for homework 2.
"""
import os
import csv
import logging
from time import sleep
import dynamolib as db

PROMPT = 'Please make a selection >>> '
INVALID_SELECTION = '\nPlease make a valid selection.\n'
CONTINUE = '... press enter to continue ...'


def build_db_menu():
    """
    Checks if db exists. Builds db if it does not exist, otherwise returns
    to caller. 
    :return: 
    """
    # check for db
    if db.table_exists('Courses'):
        print('"Courses" table already exists!')
        input(CONTINUE)
        return
    
    # build if needed
    print('creating table...')
    db.create_course_table()
    # wait for dynamo to catch up
    sleep(5)
    print('done')
    print('populating table with course information from local file')
    try:
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'courses.csv'))) as courses:
            reader = csv.reader(courses)
            for row in reader:
                # get info and cast to correct type 
                Subject, CatalogNbr, Title, Credits, CourseID = row
                CatalogNbr = int(CatalogNbr)
                Credits = int(Credits)
                CourseID = int(CourseID)
                # make a list to pass
                course_info = [Subject, CatalogNbr, Title, Credits, CourseID]
                # pass the list
                db.populate_item('Courses', course_info)
                # pause for the db to catch up
                sleep(1)
                
    except FileNotFoundError as fnf:
        logging.Logger(fnf)
    # another short pause to allow dynamo to catch up
    sleep(2)
    print('done')  
    input(CONTINUE)
    # return


def query_menu():
    """
    Displays query prompts and gathers user input to build query.
    """
    # check for db
    if not db.table_exists('Courses'):
        print('"Courses" table does not exists! Build it!')
        input(CONTINUE)
        return
    
    
    another_query = True
    # start loop
    while another_query:
        # get subject
        query_subject = ''
        while not query_subject:
            query_subject = input('Enter the 4 letter subject (e.g., SDEV)>>> ')[:4].upper()
            if not query_subject.isalpha() or len(query_subject) < 4:
                print('Must be 4 letters')
                query_subject = ''
        # get course number
        query_cat_num = ''
        while not query_cat_num.isdigit():
            query_cat_num = input('Enter the 3 digit course number (e.g., 400)>>> ')[:3]
            if not query_cat_num.isdigit() or len(query_cat_num) < 3:
                print('Must be 3 digits!')
                query_cat_num = ''
        
        # cast cat_num to int
        query_cat_num = int(query_cat_num)
        
        # pass to query 
        title = db.get_course_title(query_subject, query_cat_num)
        # print result if in db, otherwise doesn't exist
        if title == None:
            print(f'{query_subject} {query_cat_num} does not exist!')
        else:
            print(f'The title of {query_subject} {query_cat_num} is {title}')
        
        # another query?
        user_input = False
        while not user_input:
            
            user_input = input('Would you like another query? (y/n)>>> ')[:1].lower()
            # discard bad input
            if user_input not in ('y', 'n'):
                print(INVALID_SELECTION)
                user_input = False
            
            if user_input == 'n':
                another_query = False


def main_menu():
    """
    Displays main menu. Selections are build db, query db, or exit.
    """
    
    user_selection = 0

    while user_selection == 0:
        os.system('clear')
        print('Main Menu\n'
              '1. Build Course Database\n'
              '2. Query Course Database\n'
              '3. Exit')

        # get user selection
        user_selection = input(PROMPT).strip()
        # discard invalid selections
        if user_selection not in ('1', '2', '3'):
            print(f'{INVALID_SELECTION}')
            input(CONTINUE)
            user_selection = 0
        
        if user_selection == '1':
            # build db
            build_db_menu()
            user_selection = 0
            pass
        
        if user_selection == '2':
            # query db
            query_menu()
            user_selection = 0
            pass
        
        if user_selection == '3':
            # return to __main__ to exit
            return
