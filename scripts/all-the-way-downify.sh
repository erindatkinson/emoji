#!/bin/bash

# Credit to https://gist.github.com/alisdair/ffc7c884ee36ac132131f37e3803a1fe for the excellent original
# script that this one is based on. This script modifies the original to create the all-the-way-down effect.

# Generate a `:*-all-the-way-down:` Slack emoji, given a reasonable image
# input. I recommend grabbing an emoji from https://emojipedia.org/

set -euo pipefail

if [ $# -eq 0 ]; then
  echo "Usage: $0 input.png"
  exit 1
fi

file_path=$1
cd "$(dirname "$file_path")"
file=$(basename -- "$file_path")
file_name="${file%.*}"

# Scale to 128x128
scaled="${file%.*}-scaled.png"
convert \
  -gravity center \
  -background none \
  -geometry 128x128 \
  "${file}" \
  "${scaled}"

# Generate tiled image for scrolling
tiled="${file%.*}-tiled.png"
convert \
  -gravity center \
  -background none \
  -size 128x512 \
  tile:"${scaled}" \
  "${tiled}"

# Generate scrolling frames
frame="${file%.*}-frame"
n=0
count=16
pixels_to_scroll=8
while [ "$n" -lt "$count" ]; do
  x=0
  y=$((n * pixels_to_scroll))

  # Scroll the image and crop it to 128x128
  convert \
    -gravity center \
    -background none \
    -roll "+${x}-${y}" \
    -crop 128x128+0+0 \
    +repage \
    "${tiled}" \
    "${frame}"-"${n}".gif

  n=$((n + 1))
done

# Combine the frames into a GIF
gif="${file%.*}-all-the-way-down.gif"
convert \
  -background none \
  -set dispose Background \
  -delay 1x10 \
  -loop 0 \
  $(for i in $(seq 0 15); do echo ${frame}-${i}.gif; done) \
  "${gif}"

# Clean up
rm "${scaled}" "${tiled}" "${frame}"-*.gif

# We did it y'all
echo "Created ${gif}. Enjoy!"