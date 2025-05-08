#!/bin/bash

# Find all .py files in the geothai directory and run autopep8 on each
find geothai -type f -name "*.py" | while read -r file; do
    autopep8 --in-place "$file"
    echo "Formatted: $file"
done
