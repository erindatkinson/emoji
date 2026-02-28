#!/bin/bash

# This script was pulled from https://gist.github.com/lafentres/7a264fa5e4c83cf59012929b5d234ae2 and is
# here as a convenience.

# Credit to https://gist.github.com/alisdair/ffc7c884ee36ac132131f37e3803a1fe for the excellent original 
# script that this one is based on. This script modifies the original to create the spin effect. 

# Generate a `:*-spin:` Slack emoji, given a reasonable image
# input. I recommend grabbing an emoji from https://emojipedia.org/

set -euo pipefail

if [ $# -eq 0 ]; then
  echo "Usage: $0 input.png"
  exit 1
fi

input=$1
cd "$(dirname "$input")"

filename=$(basename -- "$input")

# Add enough to the width and height to make sure nothing
# gets cut off when the image is rotated
width=$(identify -format "%w" "$filename")
height=$(identify -format "%h" "$filename")
a_squared=$(bc <<< "$width ^ 2")
b_squared=$(bc <<< "$height ^ 2")
c_squared=$(( a_squared + b_squared ))
c=$(bc <<< "sqrt($c_squared)")
new_width=$(( c + 1 ))
new_height=$(( c + 1 ))
extended="${filename%.*}-extended.png"
convert \
  -gravity center \
  -background none \
  -extent ${new_width}x${new_height} \
  "$filename" \
  "$extended"

# Generate rotated frames
frame="${filename%.*}-frame"
count=24
n=1
convert "$extended" "$frame"-0.gif
while [ "$n" -lt "$count" ]; do
  # Rotate the image!
  convert \
    -gravity center \
    -background none \
    -distort SRT +15 \
    "$frame"-"$(( n - 1 ))".gif \
    -flatten \
    "$frame"-"$n".gif

  n=$((n + 1))
done

# Combine the frames into a GIF and scale it to 128x128
combined="${filename%.*}-spin-combined.gif"
convert \
  -gravity center \
  -background none \
  -geometry 128x128 \
  -set dispose Background \
  -delay 1x10 \
  $(for i in $(seq 0 23); do echo ${frame}-${i}.gif; done) \
  -loop 0 \
  "$combined"

# Trim the extra empty space off the GIF
gif="${filename%.*}-spin.gif"
convert \
  "$combined" \
  -trim \
  -layers trim-bounds \
  "$gif"

# Clean up
rm "$extended" "$combined" "${frame}"-*.gif

# We did it y'all
echo "Created $gif. Enjoy!"
