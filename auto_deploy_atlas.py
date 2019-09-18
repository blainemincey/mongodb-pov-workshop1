#!/usr/bin/env python3

import requests
import json
import settings
import time
import datetime
from timeit import default_timer as timer
import sys
from requests.auth import HTTPDigestAuth

####
# Start script
####
start = timer()
print("============================")
print("  CREATE ATLAS CLUSTER      ")
print("============================")
print("Starting " + time.asctime() + "\n")


####
# Main start function
####
def main():
    # create the request headers
    headers = {
        'Content-Type': 'application/json',
    }

    # For complete options, see
    # https://docs.atlas.mongodb.com/reference/api/clusters-create-one/
    data = {
        "name": CLUSTER_NAME,
        "clusterType": "REPLICASET",
        "mongoDBMajorVersion": "3.6",
        "numShards": 1,
        "providerSettings": {
            "providerName": "GCP",
            "regionName": "EASTERN_US",
            "instanceSizeName": "M10"
        },
        "replicationFactor": 3,
        "backupEnabled": True,
        "autoScaling": {"diskGBEnabled": True}
    }

    # create the cluster
    t1 = datetime.datetime.now()
    print(t1, " - Creating cluster: ", CLUSTER_NAME)
    response = requests.post(url_create, headers=headers, data=json.dumps(data),
                             auth=HTTPDigestAuth(API_PUBLIC_KEY, API_PRIVATE_KEY))
    if response.status_code != 201:
        print('Error:')
        print(response.json())
    else:
        timeout = time.time() + 60 * 15  # 15 minute timeout
        while True:
            response = requests.get(url_status, auth=HTTPDigestAuth(API_PUBLIC_KEY, API_PRIVATE_KEY))
            stateName = response.json()["stateName"]
            t2 = datetime.datetime.now()
            print(t2, " - Cluster status: ", stateName)

            if stateName == "IDLE":
                print("Cluster created in: ", t2 - t1)
                break
            if time.time() > timeout:
                print("TIMEOUT: Cluster creation is still in progress")
                print("Please go to the MongoDB Atlas UI.")
                break
            time.sleep(5)


####
# Constants loaded from .env file
####
API_PUBLIC_KEY = settings.API_PUBLIC_KEY
API_PRIVATE_KEY = settings.API_PRIVATE_KEY
PROJECT_ID = settings.PROJECT_ID
CLUSTER_NAME = settings.CLUSTER_NAME

# Other Constants
url_create = 'https://cloud.mongodb.com/api/atlas/v1.0/groups/' + PROJECT_ID + '/clusters'
url_status = 'https://cloud.mongodb.com/api/atlas/v1.0/groups/' + PROJECT_ID + '/clusters/' + CLUSTER_NAME

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