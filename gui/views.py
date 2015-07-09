from __future__ import with_statement # for python 2.5
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import HttpResponse
import json,yaml,ast
import unicodedata
import sys
import os
import time
import openravepy
import numpy.random as rand
if not __openravepy_build_doc__:
	from openravepy import *
	from numpy import *
import xml.dom.minidom
import sys
from optparse import OptionParser
from openravepy.misc import OpenRAVEGlobalArguments
import pickle
from bs4 import BeautifulSoup
from threading import Thread,Lock
from functools import partial
app=None
trajectorySaveLocation=None
robot=None
configParams=None
openraveLock=Lock()
stopValLock=Lock()
stopVal=0


def initOpenrave():
	env_colladafile = '/home/siddhantmanocha/apache/feedback/feedback/environment/env_100_context_1.dae'
	trajectorySaveLocation='/home/siddhantmanocha/apache/feedback/feedback/environment/t1.pk'
	global envG
	global robot
	envG=Environment()
	envG.Load(env_colladafile)
	envG.SetViewer('qtcoin')
	robot = envG.GetRobots()[0]
	global trajectorySaveLocation
	global configParams
	trajectorySaveLocation='/home/siddhantmanocha/apache/feedback/feedback/environment/t1.pk'
	configParams=dict()
	configParams['start_configs']=list()
	configParams['end_configs']=list()
	configParams['start_configs'].append('PR2')
	configParams['start_configs'].append('pillow_2')
	configParams['start_configs'].append('bed_1')
	configParams['start_configs'].append('pillow_1')
	configParams['end_configs'].append('pillow_2')
	configParams['end_configs'].append('bed_1')
	configParams['end_configs'].append('pillow_1')
	configParams['end_configs'].append('bed_1')

# globThread = Thread(target=initOpenrave)
# globThread.start()

@api_view(['GET'])


def initApp(request):
	if request.method == 'GET':
		initOpenrave()

def playTraj(request):
	if request.method == 'GET':

		data=ast.literal_eval(dict(request.GET)['query'][0])
		json_data=json.dumps(data)
		data=yaml.safe_load(json_data)

		print 'Request Processing'
		print 'called'
		i=0
		nThread = Thread(target=playGivenTraj, args=(i,))
		nThread.start()

		# query=unicodedata.normalize('NFKD', dict(request.GET)['query'][0]).encode('ascii','ignore').strip()
		return HttpResponse(json.dumps({'result':{'success':1}}), content_type="application/json")

def resumeTraj(request):
	if request.method == 'GET':
		data=ast.literal_eval(dict(request.GET)['query'][0])
		json_data=json.dumps(data)
		data=yaml.safe_load(json_data)


def capTraj(request):
	if request.method == 'GET':
		data=ast.literal_eval(dict(request.GET)['query'][0])
		json_data=json.dumps(data)
		data=yaml.safe_load(json_data)


def capNextTraj(request):
	if request.method == 'GET':
		data=ast.literal_eval(dict(request.GET)['query'][0])
		json_data=json.dumps(data)
		data=yaml.safe_load(json_data)


def saveSeq(request):
	if request.method == 'GET':
		data=ast.literal_eval(dict(request.GET)['query'][0])
		json_data=json.dumps(data)
		data=yaml.safe_load(json_data)
		print data
		return HttpResponse(json.dumps({'result':{'success':1}}), content_type="application/json")

def waitrobot(robot):
	"""busy wait for robot completion"""
	while not robot.GetController().IsDone():
		time.sleep(0.01)

def move_arm(openrave_traj,env,robot):
	trajXML=BeautifulSoup(openrave_traj)
	content=trajXML.data.string.split(' ')
	trajXML.data['count']=2
	global stopVal
	traj = RaveCreateTrajectory(env,'')
	for i in range(0,len(content)-9,8):
		while True:
			if stopVal==0:
				break
			elif stopVal==1:
				continue
			elif stopVal ==-1:
				return
		trajXML.data.string=" ".join(content[i:i+16])+" "
		print 'waypoint',i/8+1,'of',len(content)/8
		trajToParse=str(trajXML.body.contents[0])
		traj.deserialize(trajToParse)
		robot.GetController().SetPath(traj)
		waitrobot(robot)
	return

def Playtraj(index):
	global envG
	global trajectorySaveLocation
	global robot
	with open(trajectorySaveLocation,'rb') as ff:
		trajs = pickle.load(ff)	
	move_arm(trajs[index],envG,robot)

def playGivenTraj(index):
	with openraveLock:
		global stopVal
		stopVal=0
		Playtraj(index)
		print 'Hello World'
