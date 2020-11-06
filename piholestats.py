#! /usr/bin/python

import requests
import json
import time
from influxdb import InfluxDBClient

try:
  with open('config.json', 'r') as f:
    config = json.load(f)
  with open('SECRETS.json','r') as s:
    secrets = json.load(s)



HOSTNAME = config["HOSTNAME"] # Pi-hole hostname to report in InfluxDB for each measurement
PIHOLE_API = config["PIHOLE_API"]
INFLUXDB_SERVER = config["INFLUXDB_SERVER"] # IP or hostname to InfluxDB server
INFLUXDB_PORT = config["INFLUXDB_PORT"] # Port on InfluxDB server
INFLUXDB_USERNAME = secrets["user"]
INFLUXDB_PASSWORD = secrets["password"]
INFLUXDB_DATABASE = config["INFLUXDB_DATABASE"]
DELAY = config["DELAY"] # seconds

def send_msg(domains_blocked, dns_queries_today, ads_percentage_today, ads_blocked_today):
  json_body = [
      {
          "measurement": "piholestats",
          "tags": {
              "host": HOSTNAME
          },
          "fields": {
              "domains_blocked": int(domains_blocked),
                    "dns_queries_today": int(dns_queries_today),
                    "ads_percentage_today": float(ads_percentage_today),
                    "ads_blocked_today": int(ads_blocked_today)
          }
      }
  ]
  client = InfluxDBClient(INFLUXDB_SERVER, INFLUXDB_PORT,INFLUXDB_USERNAME,INFLUXDB_PASSWORD, INFLUXDB_DATABASE) # InfluxDB host, InfluxDB port, Username, Password, database
  #client.create_database(INFLUXDB_DATABASE) # Uncomment to create the database (expected to exist prior to feeding it data)
  client.write_points(json_body)

api = requests.get(PIHOLE_API) # URI to pihole server api
API_out = api.json()

# print (API_out) # Print out full data, there are other parameters not sent to InfluxDB
domains_blocked = (API_out['domains_being_blocked'])#.replace(',', '')
dns_queries_today = (API_out['dns_queries_today'])#.replace(',', '')
ads_percentage_today = (API_out['ads_percentage_today'])#
ads_blocked_today = (API_out['ads_blocked_today'])#.replace(',', '')
send_msg(domains_blocked, dns_queries_today, ads_percentage_today, ads_blocked_today)
