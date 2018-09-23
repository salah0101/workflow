#!/usr/bin/env bash
type=$1
in_file=$2
out_file=$3

l=$(cat ${in_file} | grep -v ";" | wc -l | cut -d' ' -f1)


echo "length: $h"

touch "${out_file}"

cat ${in_file} | grep ";" > "${out_file}"

if [ "$type" == "train" ]; then
  echo "getting training"
  cat ${in_file} | grep -v ";" | head -n $l >> "${out_file}"
fi
