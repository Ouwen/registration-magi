#!/usr/bin/python

from medpy.io import load
import csv
import sys
import copy

output = open('/output/batch_script.sh', 'w')
output.write('#!/bin/bash')

filename_dictionary = {
    'pre-contrast filepath': 'pre',
    'post-contrast filepath': 'post',
    'FLAIR filepath': 'FLAIR'
}

def format_docker_string(row, reference_image_key, input_image_key):
    # 0 is the input image filepath
    # 1 is the reference image filepath
    # 2 is the output path
    # 3 is the output base name
    # 4 is the input shorthand ['pre', 'post', 'FLAIR']
    # 5 is the reference shorthand ['pre', 'post', 'FLAIR']
    docker_string = """
docker run --rm -it \\
    -v {0}:/mount{0} \\
    -v {1}:/mount{1} \\
    -v {2}:/output \\
    -e FSLOUTPUTTYPE=NIFTI \\
    ouwen/registration-magi flirt \\
    -in /mount{0} \\
    -ref /mount{1} \\
    -out /output/{3}_{4}_to_{5}_r
"""
    return docker_string.format(
        row[input_image_key],
        row[reference_image_key],
        row['output filepath'],
        row['output base filename'],
        filename_dictionary[input_image_key],
        filename_dictionary[reference_image_key]
    )

def get_min_slices_image_type(row):
     image_slices_dictionary = copy.copy(filename_dictionary)
     for image_type in filename_dictionary.keys():
         image_type_data, image_type_header = load('/mount' + row[image_type])
         x, y, slices = image_type_data.shape
         image_slices_dictionary[image_type] = slices

     return min(image_slices_dictionary, key=image_slices_dictionary.get)

with open(sys.argv[1], 'rb') as csv_file:
  image_reader = csv.DictReader(csv_file, delimiter=',')
  for row in image_reader:
      reference_image_key = get_min_slices_image_type(row)

      for image_type in filename_dictionary.keys():
          if(image_type != reference_image_key):
              output.write(format_docker_string(row, reference_image_key, image_type))
