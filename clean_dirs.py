#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import time
import subprocess
import os

from datetime import datetime, timedelta
base_dir = "/home/pi/Carl/Projects/noise_level_protocol/"
today_folder = base_dir + "mp3/" + datetime.now().strftime('%Y%m%d')
tomorrow = datetime.now() + timedelta(days=1)
tomorrow_folder = base_dir + "mp3/" + tomorrow.strftime('%Y%m%d')
csv_folder = base_dir + "csv/"

print("Deleting mp3/ and csv/")
result = subprocess.Popen("rm -r " + base_dir + "mp3/", shell=True,  stdout=subprocess.PIPE)
result = subprocess.Popen("rm -r " + base_dir + "csv/",   shell=True,  stdout=subprocess.PIPE)
time.sleep(3)

if not os.path.exists(today_folder):
  os.makedirs(today_folder)
  print("Today folder created")
if not os.path.exists(tomorrow_folder):
  os.makedirs(tomorrow_folder)
  print("Tommorrow folder created")
if not os.path.exists(csv_folder):
  os.makedirs(csv_folder)
  print("CSV folder created")

