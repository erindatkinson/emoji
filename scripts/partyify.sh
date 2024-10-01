#!/bin/bash

# This script was pulled from https://gist.github.com/lafentres/7950c77b4a6f41ca1ea3c985795fffbc
# And linked here as a convenience.

# Credit to https://gist.github.com/alisdair/ffc7c884ee36ac132131f37e3803a1fe for the excellent original 
# script that this one is based on. This script modifies the original to create the party effect. 

# Generate a `:*-party:` Slack emoji, given a reasonable image
# input. I recommend grabbing an emoji from https://emojipedia.org/

set -euo pipefail

if [ $# -eq 0 ]; then
  echo "Usage: $0 input.png"
  exit 1
fi

input=$1
cd "$(dirname "$input")"

filename=$(basename -- "$input")

# Scale to 128x128
scaled="${filename%.*}-scaled.png"
convert \
  -gravity center \
  -background none \
  -geometry 128x128 \
  "$filename" \
  "$scaled"

# Generate party colored frames
party_colors=(
  "#93fe90" 
  "#96fefd"
  "#96b9fd"
  "#cf7cfa"
  "#ef4cef"
  "#ef4c97"
  "#f0596a"
  "#f0803c"
  "#f0bb57"
  "#fad58e"
  "#c4d58e"
)
frame="${filename%.*}-frame"
for i in ${!party_colors[@]}; do
  # Tint the image
  convert \
    "$scaled" \
    -intensity Lightness \
    -colorspace gray \
    -fill "${party_colors[$i]}" \
    -tint 100 \
    "$frame"-"$i".gif
done

# Combine the frames into a GIF
gif="${filename%.*}-party.gif"
convert \
  -background none \
  -set dispose Background \
  -delay 1x10 \
  -loop 0 \
  "${frame}"-*.gif \
  "$gif"

# Clean up
rm "$scaled" "${frame}"-*.gif

# We did it y'all
echo "Created $gif. Enjoy!"
