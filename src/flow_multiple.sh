#!/usr/bin/env sh

flow=$(cat $1 | awk -f src/flow.awk)
echo "$flow $(basename $1) $2 $3 $4 $5"
