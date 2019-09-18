#!/usr/bin/env python3

import time
from timeit import default_timer as timer
import settings
from pymongo import MongoClient
import hashlib
import sys
import os

####
# Start script
####
startTs = time.gmtime()
start = timer()
print('============================')
print('Start Rolling Update Reads  ')
print('============================')
print('\nStarting ' + time.strftime('%Y-%m-%d %H:%M:%S', startTs) + '\n')


####
# Main start function
####
def main():
    client = MongoClient(DB_CONNECTION)
    db = client['rollingUpdatesDatabase']

    # refresh collection by dropping it
    db.rollingUpdatesCollection.drop()

    # recreate collection
    my_collection = db.create_collection('rollingUpdatesCollection')

    md5_hash = hashlib.md5()

    seq = 1

    cursor = my_collection.watch()
    try:
        for doc in cursor:
            try:
                md5_hash.update(doc['fullDocument']['random'].encode())
                print('Seq: ', seq, ' md5: ', md5_hash.hexdigest())
                sys.stdout.flush()
                seq += 1

            except:
                print('Cannot read: No cluster instance available for reading.')
    except KeyboardInterrupt:
        keyboard_shutdown()


####
# Swallow the verbiage that is spat out when using 'Ctrl-C' to kill the script
# and instead just print a simple single line message
####
def keyboard_shutdown():
    print('\Interrupted\n')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)


####
# Constants (URL, SECRET, and NUM_REQUESTS loaded from .env file)
####
DB_CONNECTION = settings.DB_CONNECTION

####
# Main
####
if __name__ == '__main__':
    main()

####
# Indicate end of script
####
end = timer()
endTs = time.gmtime()
print('\nEnding ' + time.strftime('%Y-%m-%d %H:%M:%S', endTs))
print('===============================')
print('Total Time Elapsed (in seconds): ' + str(end - start))
print('===============================')
