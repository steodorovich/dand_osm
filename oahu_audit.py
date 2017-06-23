# Import required Python modules

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
# opening file in filename
filename = open("c:\honolulu_hawaii.osm", "r")

# Create dictionary to count the number of unique element types

tags = {}
for event, elem in ET.iterparse(filename):
    if elem.tag in tags: 
        tags[elem.tag] += 1
    else:
        tags[elem.tag] = 1
        
pprint.pprint(tags)

# Find the number of unique users who've edited the map of O'ahu
# Create empty set, then add any element with attribute 'uid'
# Call the len function

filename = open("c:\honolulu_hawaii.osm", "r")
def process_map(filename):
    users = set()
    for i, element in ET.iterparse(filename):
        for elem in element:
            if 'uid' in elem.attrib:
                users.add(elem.attrib['uid'])
    return users
users = process_map(filename)
len(users)
