#!/bin/bash

# This script was pulled from https://gist.github.com/alisdair/ffc7c884ee36ac132131f37e3803a1fe and
# is shared here as a convenience.
#!/bin/bash

# Generate a `:*-intensifies:` Slack emoji, given a reasonable image
# input. I recommend grabbing an emoji from https://emojipedia.org/

set -euo pipefail

# Number of frames of shaking
count=10
# Max pixels to move while shaking
delta=4

if [ $# -eq 0 ]; then
  echo "Usage: $0 input.png"
  exit 1
fi

input=$1
cd "$(dirname "$input")"

filename=$(basename -- "$input")

# Add 10% padding to width and height, then scale to 128x128
width=$(identify -format "%w" "$filename")
height=$(identify -format "%h" "$filename")
new_width=$(( width + width / 10 ))
new_height=$(( height + height / 10 ))
extended="${filename%.*}-extended.png"
convert \
  -gravity center \
  -background none \
  -extent ${new_width}x${new_height} \
  -geometry 128x128 \
  "$filename" \
  "$extended"

# Generate some shaky frames
frame="${filename%.*}-frame"
n=0
while [ "$n" -lt "$count" ]; do
  # Generate some random shake
  x=$((RANDOM % (delta * 2) - delta))
  y=$((RANDOM % (delta * 2) - delta))

  # Ensure coordinates are of the form +3 or -4
  [ "$x" -ge 0 ] && x="+$x"
  [ "$y" -ge 0 ] && y="+$y"

  # Shake the image!
  convert "$extended" -page "${x}${y}" -background none -flatten "$frame"-"$n".gif

  n=$((n + 1))
done

# Combine the frames into a GIF
gif="${filename%.*}-intensifies.gif"
convert -background none -set dispose Background -delay 1x30 -loop 0 "${frame}"-*.gif "$gif"

# Clean up
rm "$extended" "${frame}"-*.gif

# We did it y'all
echo "Created $gif. Enjoy!"