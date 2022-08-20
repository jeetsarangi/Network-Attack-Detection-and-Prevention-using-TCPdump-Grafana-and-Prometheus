#!/bin/bash
while true; do (timeout 20 /opt/grok-exporter/grok_exporter --config=./agent.yml) ; sleep 1; done;
