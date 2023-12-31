###############################################################################
#  
#  Carelink Client 2 CLI
#  
#  Description:
#
#    This is the command line interface of the Carelink Client. It is used
#    to download a patients recent pump and sensor data from the Carelink 
#    Cloud. The data is saved to a JSON file.
#  
#  Author:
#
#    Ondrej Wisniewski (ondrej.wisniewski *at* gmail.com)
#  
#  Changelog:
#
#    31/12/2023 - Initial version
#
#  Copyright 2023, Ondrej Wisniewski 
#
###############################################################################

import carelink_client2
import argparse
import time
import json
import datetime

VERSION = "1.0"


def writeJson(jsonobj, name):
   filename = name + "-" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
   try:
      f = open(filename, "w")
      f.write(json.dumps(jsonobj,indent=3))
      f.close()
   except Exception as e:
      print("ERROR: failed to save %s (%s) " % (filename, str(e)))
      return False
   else:
      return True


# Parse command line 
parser = argparse.ArgumentParser()
parser.add_argument('--user',     '-u', type=str, help='CareLink user name', required=True)
parser.add_argument('--country',  '-c', type=str, help='CareLink two letter country code', required=False)
parser.add_argument('--repeat',   '-r', type=int, help='Repeat request times', required=False)
parser.add_argument('--wait',     '-w', type=int, help='Wait minutes between repeated calls', required=False)
parser.add_argument('--data',     '-d', help='Save recent data', action='store_true')
parser.add_argument('--verbose',  '-v', help='Verbose mode', action='store_true')
args = parser.parse_args()

# Get parameters from CLI
user     = args.user
country  = args.country
repeat   = 1 if args.repeat == None else args.repeat
wait     = 5 if args.wait == None else args.wait
data     = args.data
verbose  = args.verbose

#print("country  = " + country)
#print("repeat   = " + str(repeat))
#print("wait     = " + str(wait))
#print("data     = " + str(data))
#print("verbose  = " + str(verbose))

# Create client instance
client = carelink_client_2.CareLinkClient(userName=user)
if verbose:
   print("Client created")
   
if client.init():
   client.printUserInfo()
   for i in range(repeat):
      if verbose:
         print("Starting download, count: %d" % (i+1))
      try:
         recentData = client.getRecentData()
         if client.getLastResponseCode() == 200:
            if(data):
               if writeJson(recentData, "data"):
                  if verbose:
                     print("Data saved successfully")
         # Error occured
         else:
            print("ERROR: failed to get data (response code %d)" % client.getLastResponseCode())
            break
      except Exception as e:
         print(e)
         break
            
      if i < repeat - 1:
         if verbose:
            print("Waiting %d minutes before next download" % wait)
         time.sleep(wait * 60)
else:
   print("ERROR: failed to initialize client (response code %d)" % client.getLastResponseCode())
