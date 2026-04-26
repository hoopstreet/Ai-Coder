#!/bin/ash
while true; do
  if ! pgrep -f master_controller.py > /dev/null; then
    nohup python3 master_controller.py >> master.log 2>&1 &
  fi
  sleep 15
done
