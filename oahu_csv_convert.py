# Import the necessary packages

# import xml data into a csv file for later integration into sql database
# first load necessary packages
import csv
import codecs
import re
import xml.etree.cElementTree as ET

import cerberus

import schema

# create the csv files

OSM_PATH = "c:\honolulu_hawaii.osm"
NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# Look for problematic tag names

filename = open("c:\honolulu_hawaii.osm", "r")
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
def key_type(element, keys):
    if element.tag == "tag":
        k = element.attrib['k']
        if re.search(lower, k):
            keys["lower"] += 1
        elif re.search(lower_colon, k):
            keys["lower_colon"] += 1
        elif re.search(problemchars, k):
            keys["problemchars"] += 1
        else:
            keys["other"] += 1
            
    return keys
def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
    return keys
process_map(filename)

process_map(OSM_PATH)

