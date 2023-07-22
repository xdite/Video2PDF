#!/bin/bash

# get list of srt files
for i in *.srt
do
  # check if corresponding .zh.srt exists
  zh_srt_name="${i%.*}.zh.srt"
  if [ ! -f "$zh_srt_name" ]
  then
    # .zh.srt doesn't exist, print the file name
    echo "Processing file: $i"

    # run python script
    python3 translate_srt.py "$i"
  fi
done
