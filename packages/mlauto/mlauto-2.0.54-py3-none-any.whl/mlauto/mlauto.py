import torch
import torchvision
import matplotlib.pyplot as plt
import numpy as np
random_seed = 1
torch.backends.cudnn.enabled = False
torch.manual_seed(random_seed)
from scipy.signal import savgol_filter

import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import os

import socket
import pickle, json, requests, ast

import pkg_resources


IP = '127.0.0.1:8000'

def login(username, key):
  print("Logging in...")
  credentials = {'username':username, 'key':key, 'task':'login'}
  response = requests.post('http://'+IP+'/api/python_login', data=credentials)
  if response.text == '1':
    os.environ["username"] = username
    os.environ["key"] = key
    print("Successfully connected to tunerml!")
  else:
    print("Credentials could not be verified.")


def project(project_name):
  installed_packages = pkg_resources.working_set #Save all installed packages for that project
  installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])
  
  data = {'project_name': project_name, 'installed_packages': str(installed_packages_list), 'username': os.environ['username'], 'key': os.environ['key']}
  response = requests.post('http://'+IP+'/api/create_project', data=data)
  
  if response.text == '0':
    print("Authentication failed")
  else:
    response_dict = ast.literal_eval(response.text)
    
    if response_dict['exists'] == 0:
      print("Created a new project.")
    else:
      print("Project exists. Created a new run")

  print(str(response_dict['project_id']))
  return str(response_dict['project_id'])


      

def block(project_id, block_name, connect_with=None):
  print(connect_with)
  if connect_with == None: 
    data = {'project_id': project_id, 'block_name': block_name, 'username': os.environ['username'], 'key': os.environ['key']}
  else:
    data = {'project_id': project_id, 'block_name': block_name, 'connect_with': connect_with, 'username': os.environ['username'], 'key': os.environ['key']}
    
  response = requests.post('http://'+IP+'/api/create_block', data=data)
  
  if response.text == '0':
    print("Authentication failed")
  else:
    response_dict = ast.literal_eval(response.text)
    
    if response_dict['connect_with'] == 0:
      print("Couldn't find connecting block. Please create it.")
      return

    print({'_id': response_dict['block_id'], 'type':'block'})
    return {'_id': response_dict['block_id'], 'type':'block'}


      
  
def node(block, node_name, node_description, connect_with=None):

  if connect_with == None:
    data = {'node_name': node_name, 'node_description': node_description,
            'username': os.environ['username'], 'key': os.environ['key'], 'block_id': block['_id']}
  else:
    data = {'node_name': node_name, 'connect_with': connect_with, 'node_description': node_description,
            'username': os.environ['username'], 'key': os.environ['key'], 'block_id': block['_id']}
    
  response = requests.post('http://'+IP+'/api/create_node', data=data)

  if response.text == '0':
    print("Authentication failed")
  else:
    response_dict = ast.literal_eval(response.text)
    
    if response_dict['connect_with'] == 0:
      print("Couldn't find connecting node. Please create it.")
      return

    print({'_id': response_dict['node_id'], 'type':'node'})
    return {'_id': response_dict['node_id'], 'type':'node'}





def log(obj, variables):
  data = {'_id': obj['_id'], 'type': obj['type'], 'variables': str(variables), 'username': os.environ['username'], 'key': os.environ['key']}
  response = requests.post('http://'+IP+'/api/set_variables', data=data)



