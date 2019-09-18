#!/usr/bin/env python3
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Accessing variables.
API_PUBLIC_KEY = os.getenv('API_PUBLIC_KEY')
API_PRIVATE_KEY = os.getenv('API_PRIVATE_KEY')
PROJECT_ID = os.getenv('PROJECT_ID')
CLUSTER_NAME = os.getenv('CLUSTER_NAME')
DB_CONNECTION = os.getenv('DB_CONNECTION')

print("Settings loaded from .env file.")
