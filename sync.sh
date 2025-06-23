#!/bin/bash

# Local folder to watch (adjust this)
LOCAL_PATH="/Users/thomasa/Desktop/CodeAdam/python-bluetooth"

# Remote target (adjust this if needed)
REMOTE_USER="robot"
REMOTE_HOST="ev3dev.local"
REMOTE_PATH="/home/robot/"

# Watch and sync on change
fswatch -o "$LOCAL_PATH" | while read change; do
  echo "Change detected. Syncing..."
  ssh "$REMOTE_USER@$REMOTE_HOST" "mkdir -p $REMOTE_PATH"
  scp -r "$LOCAL_PATH/" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH"
done