#!/bin/bash

kill $(cat /tmp/vision.pid*)
kill $(cat /tmp/auditory.pid*)
kill $(cat /tmp/expression.pid*)
kill $(cat /tmp/keyboard.pid*)

# Remove the PID files
rm /tmp/vision.pid*
rm /tmp/auditory.pid*
rm /tmp/expression.pid*
rm /tmp/keyboard.pid*





