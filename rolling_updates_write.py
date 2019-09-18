#!/usr/bin/env python3

import time
from timeit import default_timer as timer
import settings
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
import hashlib
import sys
import os
import random

####
# Start script
####
startTs = time.gmtime()
start = timer()
print('============================')
print('Start Rolling Update Writes ')
print('============================')
print('\nStarting ' + time.strftime('%Y-%m-%d %H:%M:%S', startTs) + '\n')


####
# Main start function
####
def main():
    client = MongoClient(DB_CONNECTION)
    db = client['rollingUpdatesDatabase']

    try:
        # try to create the collection which should FAIL
        my_collection = db.create_collection('rollingUpdatesCollection')
        print('Start READ process before the WRITE process!')
        # drop the collection
        my_collection.drop()
        sys.exit(0)
    except CollectionInvalid:
        my_collection = db['rollingUpdatesCollection']
        if my_collection.count_documents({}) > 0:
            print('Start READ process before the WRITE process!')
            sys.exit(0)

    # now we can start writing data
    md5_hash = hashlib.md5()

    seq = 1

    try:
        while True:
            try:
                # Create random data to be added to MongoDB cluster
                rvalue = random.getrandbits(128)

                # Insert data as hex string value for readability
                my_collection.insert_one({"random": hex(rvalue)})

                # Now we successfully have written document to cluster
                # update the hash and the sequences number
                md5_hash.update(hex(rvalue).encode())
                print("Seq: ", seq, " md5:", md5_hash.hexdigest())
                sys.stdout.flush()
                seq += 1

            except:
                print("Cannot write: No primary available for writes!")
                print("make sure you use retryWrites=true to prevent this error")

            time.sleep(1)

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