#!/bin/bash
while true; do (timeout 10 sudo tcpdump -nn arp or icmp or udp or tcp | awk '{print(NR,$2,$3,$4,$5,$6,$7)}' > netlog.txt); sleep 1; done;
