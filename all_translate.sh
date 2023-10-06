#!/bin/bash

# get list of srt files
for i in *.srt
do
  # Get the base name without extension
  base_name=$(basename "$i" .srt)

  # Check if this is already a .zh.srt file, if so, skip it
  if [[ $base_name == *.zh ]]; then
    continue
  fi

  # check if corresponding .zh.srt exists
  zh_srt_name="${base_name}.zh.srt"
  if [ ! -f "$zh_srt_name" ]
  then
    # .zh.srt doesn't exist, print the file name
    echo "Processing file: $i"

    # run python script
    python3 translate_srt.py "$i"
  fi
done
