#!/bin/bash

# This script was pulled from https://gist.github.com/lafentres/8c48c91b95788061a7f2743f1bb440fb and
# is shared here as a convenience.


# Credit to https://gist.github.com/alisdair/ffc7c884ee36ac132131f37e3803a1fe for the excellent original 
# script that this one is based on. This script modifies the original to create the HDR version. 

# Credit to https://sharpletters.net/2025/04/16/hdr-emoji/ for the HDR imagemagick command.

# Generate an HDR Slack emoji, given a reasonable image
# input. I recommend grabbing an emoji from https://emojipedia.org/

set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 input.png"
  exit 1
fi

file_path=$1
cd "$(dirname "$file_path")"
file=$(basename -- "$file_path")
file_name="${file%.*}"
file_extension="${file#*.}"
file_type=$(file "${file}" -b --mime-type)

# Scale to 128x128
scaled="${file_name}-scaled.${file_extension}"
convert \
  -gravity center \
  -background none \
  -geometry 128x128 \
  "${file}" \
  "${scaled}"

# HDRify it!
# https://sharpletters.net/2025/04/16/hdr-emoji/
# Adjust the Multiply value up or down to preserve color as opposed to brightness
hdr_file="hdr-${file_name}.${file_extension}"
magick "${scaled}" \
  -define quantum:format=floating-point \
  -colorspace RGB \
  -auto-gamma \
  -evaluate Multiply 1.5 \
  -evaluate Pow 0.9 \
  -colorspace sRGB \
  -depth 16 \
  -profile 2020_profile.icc \
  "${hdr_file}"

echo "Created ${hdr_file}"

# Clean up
rm "${scaled}"

# We did it y'all
echo "${file} has been HDRified! Enjoy!"
Comment
