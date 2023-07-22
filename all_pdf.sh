#!/bin/bash

# get list of mp4 files
for i in *.mp4
do
  # check if corresponding pdf exists
  pdf_name="${i%.*}.pdf"
  if [ ! -f "$pdf_name" ]
  then
    # pdf doesn't exist, print the file name
    echo "Processing file: $i"

    # run python script
    python main.py "$i"
  fi
done
