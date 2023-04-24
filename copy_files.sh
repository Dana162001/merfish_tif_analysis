#!/bin/bash

source_directory="/hpcwork/rwth1209/data/merfish/raw/raw_2023PK1-vimentin-desmin-yap-HuHeart-FFPE/data"
destination_directory="/hpcwork/rwth1209/data/merfish/raw/stack_6_100_tif"

# Generate a list of 100 random numbers
random_numbers=($(shuf -i 1000-2291 -n 100))

# Copy .dax files corresponding to the random numbers
for num in "${random_numbers[@]}"; do
    cp "$source_directory/stack_6_${num}.dax" "$destination_directory"
done

# Copy .inf files corresponding to the random numbers
for num in "${random_numbers[@]}"; do
    cp "$source_directory/stack_6_${num}.inf" "$destination_directory"
done

# Copy .inf files from stack_prestain directory corresponding to the random numbers
for num in "${random_numbers[@]}"; do
    cp "$source_directory/stack_prestain_${num}.inf" "$destination_directory"
done

# Copy .dax files from stack_prestain directory corresponding to the random numbers
for num in "${random_numbers[@]}"; do
    cp "$source_directory/stack_prestain_${num}.dax" "$destination_directory"
done
