#! python3
"""
PynamoDB
Jonathan Mainhart
SDEV 400
14 Sep 2021

PynamoDB creates, populates, and allows users to query a DynamoDB table. 
"""
import logging
import sys
import os
import menu


def main():
    """
    main() function of homework1 project.
    """
    # set up logging
    LOG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'log/homework2.log'))
    logging.basicConfig(level=logging.INFO,
                        filename=LOG_FILE,
                        datefmt='%d-%b-%y %H:%M:%S',
                        format='%(levelname)s: %(asctime)s: %(message)s')
    logging.info('starting pynamoDB')

    # present the main menu - all functions are accessed via the main and sub menus
    menu.main_menu()

    # clear the screen then exit with current UTC date and time
    os.system('clear')
    logging.info('finishing pynamoDB')
    sys.exit(0)


if __name__ == '__main__':
    main()
