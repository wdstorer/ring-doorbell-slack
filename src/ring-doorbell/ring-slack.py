#!/usr/local/bin/python

import time
import requests
import json
import sys
import datetime
import config
import argparse
import socket
import getpass
import os
import string
from pathlib import Path
from ring_doorbell import Ring, Auth
from oauthlib.oauth2 import MissingTokenError

# Globals

headers = {
   "Accept": "application/json",
   "Content-Type": "application/json",
   "Authorization": "Basic " + config.authorizationkey
}

cache_file = Path('/token/test_token.cache')

def token_updated(token):
    cache_file.write_text(json.dumps(token))

def otp_callback():
    auth_code = input("2FA code: ")
    return auth_code

def httpgetrequest(url):
  response = requests.request(
    "GET",
    url,
    headers=headers
  )
  return response

def httppostrequest(url,payload):
  response = requests.request(
    "POST",
    url,
    data=payload,
    headers=headers
  )
  return response

def httpputrequest(url,payload):
  response = requests.request(
    "PUT",
    url,
    data=payload,
    headers=headers
  )
  return response

def notifyslack(channel, message):
  payload=json.dumps( {
    "channel": "#" + channel,
    "username": "Ringbot",
    "text": ":package: " + message,
    "attachments": [ {
      "fallback": "",
      "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png"
    } ],
    "icon_emoji": ":package:"
  } )

  response = httppostrequest(config.slackwebhook, payload)

def initialize_ring():
  if cache_file.is_file():
    auth = Auth("MyProject/1.0", json.loads(cache_file.read_text()), token_updated)
  else:
    auth = Auth("MyProject/1.0", None, token_updated)
    try:
      auth.fetch_token(config.ringuser, config.ringpassword)
    except MissingTokenError:
      auth.fetch_token(config.ringuser, config.ringpassword, otp_callback())
    
  ring = Ring(auth)
  ring.update_data()
  return ring

def ring_takesnapshot(doorbell):
  print("snapshot")

def check_doorbell_history(myring):
  print(myring)
  for doorbell in myring['authorized_doorbots']:

    # listing the last 15 events of any kind
    for event in doorbell.history(limit=15):
        print('ID:       %s' % event['id'])
        print('Kind:     %s' % event['kind'])
        print('Answered: %s' % event['answered'])
        print('When:     %s' % event['created_at'])
        print('--' * 50)

    # get a event list only the triggered by motion
    print(doorbell.history(limit=15))
    print(doorbell.name)
    while True:
      print(doorbell.check_alerts())
      time.sleep(5)

def notify_slack(doorbell):
  print("Someone is at " + doorbell.name)
  notifyslack("front-desk", "Someone is at the " + doorbell.name)

def check_doorbell_ring(myring):
  print(myring.devices()['authorized_doorbots'])
  doorbell = myring.devices()['authorized_doorbots'][0]
  print("running monitor for " + doorbell.name)
  while True:
    myring.update_dings()
    #print(myring.active_alerts())
    if myring.active_alerts() != []:
      print("Someone is at the door!")
      notify_slack(doorbell)
    time.sleep(5)



myring = initialize_ring()
check_doorbell_ring(myring)

