#!/bin/bash

# Start SSH daemon in the background
/usr/sbin/sshd -D &

# Run your Python script
python3 /code/main.py
