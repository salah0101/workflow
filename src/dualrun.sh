#!/usr/bin/env bash

echo "src/predict.py $1 $3 &"
src/predict.py $1 $3 &
a=$!
echo "ocs contextual $2 --ipc=$3 --stat=$4 > $5"
ocs contextual $2 --ipc=$3 --stat=$4 > $5
kill ${a}
