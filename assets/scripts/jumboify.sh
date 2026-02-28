#!/bin/bash


# This script was pulled from https://gist.github.com/lafentres/c80ef34c759a0a926d856047f9d15f3b and
# is shared here as a convenience.

# Credit to https://gist.github.com/alisdair/ffc7c884ee36ac132131f37e3803a1fe for the excellent original 
# script that this one is based on. This script modifies the original to create the jumbo. 

# Generate a jumbo Slack emoji, given a reasonable image
# input. I recommend grabbing an emoji from https://emojipedia.org/

set -euo pipefail

if [ $# -lt 3 ]; then
  echo "Usage: $0 input.png rows columns"
  exit 1
fi

file_path=$1
cd "$(dirname "$file_path")"
file=$(basename -- "$file_path")
file_name="${file%.*}"
file_extension="${file#*.}"
file_type=$(file "${file}" -b --mime-type)

integer_regex='^[0-9]+$'
rows=$2
if ! [[ $rows =~ $integer_regex ]]; then 
  echo "error: rows must be a number"
  exit 1 
fi

columns=$3
if ! [[ $columns =~ $integer_regex ]]; then 
  echo "error: columns must be a number"
  exit 1 
fi

# Scale image based on desired columns and rows
new_width=$(( 128 * columns ))
new_height=$(( 128 * rows ))
extended="${file_name}-extended.${file_extension}"
convert \
  -quiet \
  -gravity center \
  -background none \
  -scale ${new_width}x${new_height} \
  -extent ${new_width}x${new_height} \
  "${file}" \
  "${extended}"

# Crop it!
crop_height=$(( new_height / rows ))
crop_width=$(( new_width / columns ))
for (( row=0; row < rows; row++ )) do 
  for (( column=0; column < columns; column++ )) do 
    row_offset=$(( row * crop_height ))
    column_offset=$(( column * crop_width ))
    cropped_file="${file_name}-${rows}x${columns}-row$(( row + 1 ))-col$(( column + 1 )).${file_extension}"

    if [[ $file_type == "image/gif" ]]; then 
      gifsicle \
        --colors 128 \
        -Okeep-empty \
        --crop ${column_offset},${row_offset}+${crop_width}x${crop_height} \
        "${extended}" > "${cropped_file}"
    else
      convert \
        -quiet \
        -crop ${crop_width}x${crop_height}+${column_offset}+${row_offset} \
        +repage \
        "${extended}" \
        "${cropped_file}"
    fi

    echo "Created ${cropped_file}"  
  done 
done

# Clean up
rm "${extended}"

# We did it y'all
echo "${file} has been jumboified! Enjoy!"
