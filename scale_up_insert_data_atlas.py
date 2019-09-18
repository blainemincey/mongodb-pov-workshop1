#!/usr/bin/env python3
import pymongo
import sys
import settings

connection = pymongo.MongoClient(settings.DB_CONNECTION)
print('Inserting records continuously....')
connect_problem = False

# Drop the existing collection
connection.mydb.records.drop()

# the first record
val = 1

while True:
    try:
        connection.mydb.records.insert_one({'val': val});
        val += 1

        if val % 100 == 0:
            print(val,  'records inserted')

        if connect_problem:
            print('Reconnected')
            connect_problem = False

    except KeyboardInterrupt:
        print
        sys.exit(0)

    except:
        print('\n********\n\nConnection problem\n\n********\n')
        connect_problem = True
