# Test
# Canada
# Here
# Red
# Blue

rsync -av --exclude='.git' /Users/thomasa/Desktop/CodeAdam/python-bluetooth/ /tmp/python-bluetooth-clean/ 
scp -r /tmp/python-bluetooth-clean/ robot@ev3dev.local:/home/robot/