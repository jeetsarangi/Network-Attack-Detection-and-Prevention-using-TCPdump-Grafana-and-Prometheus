#!/bin/bash
while true; do timeout 600 prometheus --config.file=./prometheus.yml --storage.tsdb.path=/opt/prometheus/data --storage.tsdb.retention.time=10s ; sleep 1; rm -rf /opt/prometheus/data*; sleep 1;done;
