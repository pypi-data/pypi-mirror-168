#!/usr/bin/env python3
import logging
import paramiko
import os
from pathlib import Path
from paramiko import SSHClient
from mtlibs.sshClient import SshClient
from mtlibs.SSH import SSH
from dotenv import load_dotenv, find_dotenv
import argparse
import logging
from mtlibs.yaml import load_yaml_file
import json
from contentful_management import Client

APP_NAME = "mtdp"

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

load_dotenv(".env")

import logging
logging.basicConfig(level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import contentful


space_id = os.environ.get("CONTENTFUL_SPACE_ID")
access_token = os.environ.get("CONTENTFUL_ACCESS_TOKEN")
mng_token = os.environ.get("CONTENTFUL_MNG_TOKEN")
environment_id=os.environ.get("CONTENTFUL_ENVIRONMENT_ID")



def destroy_all():
    """删除所有模型以及数据（危险）"""
    
    # client = contentful.Client(
    #     space_id, 
    #     access_token  
    # )
    client = Client(mng_token)
    content_types = client.content_types(space_id, environment_id)
    for content_type in content_types:
        content_type.delete()
        logger.info(f"成功删除content_type: {content_type}")
        # client.content_types(space_id, environment_id).delete(content_type.id)
        
    
def setup_model():
    """生成模型"""
    space_id = os.environ.get("CONTENTFUL_SPACE_ID")
    access_token = os.environ.get("CONTENTFUL_ACCESS_TOKEN")
    mng_token = os.environ.get("CONTENTFUL_MNG_TOKEN")
    environment_id=os.environ.get("CONTENTFUL_ENVIRONMENT_ID")
    client = Client(mng_token)

    # Create a Content Type:
    content_type_id = 'some_content'  # Use `None` if you want the API to autogenerate the ID.
    content_type = client.content_types(space_id, environment_id).create(content_type_id, {
        'name': 'mt_meta',
        'description': '元数据',
        'displayField': 'name',
        'fields': [
            {
                'name': 'Name',
                'id': 'name',
                'type': 'Symbol',
                'localized': False
            }
        ]
    })

    # Update a Content Type:
    content_type.name = 'mt_meta'
    content_type.save()

def main():    
    destroy_all()
    setup_model()
    
    client = contentful.Client(
        'nzotnryd8qki',  # This is the space ID. A space is like a project folder in Contentful terms
        's3U9Zs9Y_R6nn_jkBl0qz_WODudOs56piXK6KV6NrTw'  # This is the access token for this space. Normally you get both ID and the token in the Contentful web app
    )
    # This API call will request an entry with the specified ID from the space defined at the top, using a space-specific access token.
    # entry = client.entry('demo')
    content_types = client.content_types()
    cat_content_type = client.content_type('demo')    
    logger.info(cat_content_type)
    
    entries = client.entries()
    logger.info(f"entries: {entries}")
    
    for e in entries:
        logger.info(f"e: {e}")
        logger.info(f"name: {e.name}")
    

if __name__ == "__main__":
    main()
