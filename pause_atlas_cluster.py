#!/usr/bin/env python3

import requests
import settings
import time
from timeit import default_timer as timer
from requests.auth import HTTPDigestAuth
import json

####
# Start script
####
start = timer()
print("============================")
print("  Pause Atlas Cluster       ")
print("============================")
print("Starting " + time.asctime() + "\n")


####
# Main start function
####
def main():
    cluster_to_pause = 'https://cloud.mongodb.com/api/atlas/v1.0/groups/' + PROJECT_ID + '/clusters/' + CLUSTER_NAME

    # create the request headers
    headers = {
        'Content-Type': 'application/json',
    }

    # pause the cluster -- true or false
    data = {
        'paused': 'false'
    }

    # pause the cluster
    response = requests.patch(cluster_to_pause, headers=headers, data=json.dumps(data),
                             auth=HTTPDigestAuth(API_PUBLIC_KEY, API_PRIVATE_KEY))

    print('Pause Results: ' + response.text)


####
# Constants loaded from .env file
####
API_PUBLIC_KEY = settings.API_PUBLIC_KEY
API_PRIVATE_KEY = settings.API_PRIVATE_KEY
PROJECT_ID = settings.PROJECT_ID
CLUSTER_NAME = settings.CLUSTER_NAME

####
# Main
####
if __name__ == '__main__':
    main()

####
# Indicate end of script
####
end = timer()
print("\nEnding " + time.asctime())
print('====================================================')
print('Total Time Elapsed (in seconds): ' + str(end - start))
print('====================================================')
