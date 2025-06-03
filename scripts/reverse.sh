#!/bin/bash

# Generate a reversed gif.

set -euo pipefail

if [ $# -eq 0 ]; then
  echo "Usage: $0 input.gif"
  exit 1
fi

input=$1
cd "$(dirname "$input")"

filename=$(basename -- "$input")
gif="${filename%.*}-reversed.gif"
convert "$input" -coalesce -reverse -quiet -layers OptimizePlus  -loop 0 "$gif"

# We did it y'all
echo "Created $gif. Enjoy!"