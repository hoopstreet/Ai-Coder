#!/bin/ash
pgrep -f master_controller.py > /dev/null
if [ $? -ne 0 ]; then
    echo "$(date): Agent down. Restarting..." >> /root/Ai-Coder/persistence.log
    nohup python3 /root/Ai-Coder/master_controller.py >> /root/Ai-Coder/master.log 2>&1 &
fi
