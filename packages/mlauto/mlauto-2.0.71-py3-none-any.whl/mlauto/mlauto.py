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


def project(project_name, path=None):

  if (path == None) or (os.path.exists(path) == False):
    #print("Saving to flow/"+project_name+"/new_file.json")
    print("Saving to flow/new_file.json")
    if not os.path.exists('flow'):
      os.mkdir('flow')
      path = "flow/new_file.json"
    #if not os.path.exists('flow/'+project_name):
    #  os.mkdir('flow/'+project_name)
    #path = "flow/"+project_name+"/new_file.json"
    
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

  flow_config = {
      "name": project_name,
      "project_id": response_dict['project_id'],
      "date": 123,
      "time": 456,
      "blocks": [],
      "nodes": []
  }

  with open(path, 'w') as f:
    json.dump(flow_config, f, indent=4)

  f.close()
      

def block(block_name, path=None):

  if (path == None):
    if (os.path.exists("flow/new_file.json") == False):
      print("Cannot find json file on "+path)
      print("Please run mlauto.project before creating a block")
      return 0
  else:
    if (os.path.exists(path) == False):
      print("Cannot find json file on "+path)
      print("Please run mlauto.project before creating a block")
      return 0

  with open('flow/new_file.json') as f:
    data = json.load(f)
    
  print(data)

  if len(data['blocks']) == 0: 
    data = {'project_id': data['project_id'], 'block_name': block_name, 'username': os.environ['username'], 'key': os.environ['key']}
  else:
    data = {'project_id': data['project_id'], 'block_name': block_name, 'connect_with': data['blocks'][-1], 'username': os.environ['username'], 'key': os.environ['key']}
  
  response = requests.post('http://'+IP+'/api/create_block', data=data)
  
  if response.text == '0':
    print("Authentication failed")
    f.close()
  else:
    response_dict = ast.literal_eval(response.text)
    
    if response_dict['connect_with'] == 0:
      print("Couldn't find connecting block. Please create it.")
      return

    data['blocks'].append(response_dict['block_id'])
    json.dump(data, f, indent=4)

    f.close()
    
    print({'_id': response_dict['block_id'], 'type':'block'})
    return {'_id': response_dict['block_id'], 'type':'block'}


      
  
def node(block, node_name, node_description, connect_with=None):

  if connect_with == None:
    data = {'node_name': node_name, 'node_description': node_description,
            'username': os.environ['username'], 'key': os.environ['key'], 'block_id': block['_id']}
  else:
    data = {'node_name': node_name, 'connect_with': connect_with['_id'], 'node_description': node_description,
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


