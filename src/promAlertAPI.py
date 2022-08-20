#!/usr/bin/python3
import requests as req
import json
import sys
import time
import os

print("Usage: ./{} ip:port".format(sys.argv[0]))

address = "172.27.22.82:9090" # Prometheus Server IP and Port..
promIP = address.split(":")[0]
promapi = 'http://{}/api/v1/query?query='.format(address)
parameters = ['prot_tcp', 'prot_icmp'] # We have considered two protocols for identifying the type of attack.

blockedIPs = []
unblockTime = 60

def applyRule(attackerIP, promIP):
	if attackerIP == promIP:
		print("Not Blocking the Server")
		return
	command = "iptables -A INPUT -s {} -j DROP".format(attackerIP)
	print("Executing ", command)
	os.system(command)
	time.sleep(3)
	blockedIPs.append([time.time(),attackerIP])

def grantAccess(blockedIPs): # Grant Access again after unblockTime
	for timeIP in blockedIPs:
		oldtime, attIP = timeIP
		if((time.time() - oldtime) > unblockTime): # For testing.. Will unblock the IP again after the specified time.
			command = "iptables -D INPUT -s {} -j DROP".format(attIP)
			print("Blocking IP, Executing ", command)
			os.system(command)
			time.sleep(3)

def checkAlert(parameter,resdict):
	result = resdict['data']['result']
	for res in result:
		ip = res['metric']['sip']
		pack = int(res['value'][1])
		if(pack > 600):  # Threshold for attack detection.
			print("\n[!]Packet Count", pack, parameter, "State => Alert, Flooding Detected by IP =>",ip)
			applyRule(str(ip),promIP)
		else:
			print("\nPacket Count", pack, parameter, "State => NORMAL")

while True:
	for parameter in parameters:
		print("Getting response for", promapi+'count({}) by (sip)'.format(parameter))
		try:
			response = req.get(promapi+'count({}) by (sip)'.format(parameter), timeout = 2).json()
			checkAlert(parameter,response)
			time.sleep(1)
		except req.exceptions.HTTPError as err:
			print("No Data/Timed out for", parameter)
			time.sleep(5)
			continue
	time.sleep(3)
	grantAccess(blockedIPs)

