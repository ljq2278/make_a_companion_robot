#!/bin/bash

kill $(cat /tmp/vision.pid*)
kill $(cat /tmp/auditory.pid*)
kill $(cat /tmp/expression.pid*)

# Remove the PID files
rm /tmp/vision.pid*
rm /tmp/auditory.pid*
rm /tmp/expression.pid*

python3 ./vision/see_and_upload.py &
echo $! > /tmp/vision.pid

python3 ./auditory/listen_and_upload_ir.py &
echo $! > /tmp/auditory.pid

python3 ./expression/mood_and_speak.py &
echo $! > /tmp/expression.pid





