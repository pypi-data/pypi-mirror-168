"""Cosmos :: Client to get connection. When this code will be called it will return only the connection based on the config passed.
Will return exception in cases where config will have issues.
# @Author : kazijavedalam
"""
import os
import logging
import json
from pathlib import Path
import urllib3

import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.errors as errors


# Path
HOME_DIR = Path(os.path.dirname(__file__)).parent.parent

# Logger
# logging_config = json.load(open(os.path.join(HOME_DIR, "logger.json")))
# logging.config.dictConfig(logging_config)
# logger = logging.getLogger(__name__)


class CosmosDBClient(object):

    def __init__(self, host, master_key):
        connection_policy = documents.ConnectionPolicy()
        connection_policy.SSLConfiguration = documents.SSLConfiguration()
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        connection_policy.SSLConfiguration.SSLCaCerts = False
        try:
            self.client = cosmos_client.CosmosClient(host, {'masterKey': master_key}, connection_policy)
        except Exception as err:
            self.client = err

