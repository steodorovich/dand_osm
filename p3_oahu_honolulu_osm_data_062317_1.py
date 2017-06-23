
# coding: utf-8

# In[1]:

# Import required Python modules

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
# opening file in filename
filename = open("c:\honolulu_hawaii.osm", "r")


# In[2]:

# Create dictionary to count the number of unique element types

tags = {}
for event, elem in ET.iterparse(filename):
    if elem.tag in tags: 
        tags[elem.tag] += 1
    else:
        tags[elem.tag] = 1
        
pprint.pprint(tags)


# In[3]:

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


# In[4]:

# Create a regex for the street names as street_type_re 
# Create a default dictionary of standardized names
# Audit the file to find alternate names

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_types = defaultdict(set)
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Highway", "Way", "Freeway", "Crossing", "Mall", "Loop", "Circle"]

filename = open("c:\honolulu_hawaii.osm", "r")
def audit_street_type(street_types, street_name, regex, expected):
    m = regex.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")
def audit(filename, regex):
    for event, elem in ET.iterparse(filename, events=("start",)):
        if elem.tag == "way" or elem.tag == "node":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'], regex, expected)
    pprint.pprint(dict(street_types))
audit(filename, street_type_re)


# In[5]:

# Standardize street names via a mapping dictionary.
# First we create one for name endings (mapping1),
# Second for directional abbreviation at the beginning of street names (mapping2)

filename = open("c:\honolulu_hawaii.osm", "r")

filename = open("c:\honolulu_hawaii.osm", "r")
mapping1 = {
            "Boulavard": "Boulevard",
            "D": "Drive",
            "street": "Street",
            "Rd": "Road",
            "Rd.": "Road",
            "RD": "Road",
            "Pkwy": "Parkway",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "Glen": "Glendale",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard",
            "street": "Street",
            "St": "Street",
            "Glen": "Glendale",
            "Cir": "Circle",
            "Cir.": "Circle",
            "Dr": "Drive",
            "Dr.": "Drive",
            "Ctr": "Centre",
            "Wy": "Way",
            "Fwy": "Freeway",
            "Fwy.": "Freeway"
            }

mapping2 =  {"E"  : "East",
             "E." : "East",
             "N"  : "North",
             "N." : "North",
             "S"  : "South",
             "S." : "South",
             "W"  : "West",
             "W." : "West"}


# In[6]:

# Update the street names to standardize

def update_name(name, mapping1, regex):
    m = regex.search(name)
    if m:
        street_type = m.group()
        if street_type in mapping1:
            name = re.sub(regex, mapping1[street_type], name)
    
    return name

street_type_re  = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_type_pre = re.compile(r'^[NSEW]\b\.?', re.IGNORECASE)


# In[7]:

# Identify unique cases not handled by the "update_name" function 

for street_type, ways in street_types.iteritems(): 
        for name in ways:
            if "Suite"  in name:
                name = name.split(", Suite")[0].strip()
            if "#" in name:
                name = name.split(" #")[0].strip()
            if "," in name:
                name = name.split(", ")[0].strip()
            if "Suite" in name:
                name = name.split(" Suite")[0].strip()
            if "Building" in name:
                name = name.split(" Building")[0].strip()
            if "Ste" in name:
                name = name.split(" Ste")[0].strip()
            if "St" in name:
                name = name.split(" St")[0].strip()
            name_improv_first = update_name(name, mapping1, street_type_re)
            name_improv_sec = update_name(name_improv_first, mapping2, street_type_pre)
            
            print name, "=>", name_improv_first, "=>", name_improv_sec


# In[8]:

# Standardize phone numbers to the XXX XXX XXXX format

filename = open("c:\honolulu_hawaii.osm", "r")
phone_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
phone_types = defaultdict(set)
expected_zip = {}

def audit_phone_num(phone_types, phone_num, regex, expected_phone):
    m = regex.search(phone_num)
    if m:
        phone_type = m.group()
        if phone_type not in expected_zip:
             phone_types[phone_type].add(phone_num)

def is_phone_num(elem):
    return (elem.attrib['k'] == "phone")

def audit(filename, regex):
    for event, elem in ET.iterparse(filename, events=("start",)):
        if elem.tag == "way" or elem.tag == "node":
            for tag in elem.iter("tag"):
                if is_phone_num(tag):
                    audit_phone_num(phone_types, tag.attrib['v'], regex, expected_zip)
    pprint.pprint(dict(phone_types))
audit(filename, phone_type_re)


# In[10]:

for phone_type, ways in phone_types.iteritems():
    for name in ways:
        if "+1 " in name:
            name = name.split("+1 ")[1].strip('+1 ')
        if "+" in name:
            name = name.split("+")[1].strip('+')
        if ";" in name:
            name = name.split(";")[0].strip()
        if name.startswith ("1-"): 
            name = name.strip("1-")
        if name.startswith ("1 "):
            name = name.strip("1 ")
        if "-" in name:
            name = name.replace("-", " ")
        if "(" in name:
            name = name.replace("(", "")
        if ")" in name:
            name = name.replace(")", "")
        if "." in name:
            name = name.replace(".", " ")
        if name.startswith("01"):
            name = name.strip("01")
        if name.startswith("Phone number "):
            name = name.strip("Phone number")
        if name.startswith("1 "):
            name = name.strip("1 ")
        if len(name) < 12:
            only_numbers = re.sub(r'\D', "", name)
            name = only_numbers[0:3] + " " + only_numbers[3:6] + " " + only_numbers[6:]
        if name.startswith(" "):
            name = name.replace(" ", "")
        if "x1" in name:
            name = name.strip("x1")
        print name


# In[11]:

# Standardize zip codes

filename = open("c:\honolulu_hawaii.osm", "r")
zip_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
zip_types = defaultdict(set)
expected_zip = {}

def audit_zip_codes(zip_types, zip_name, regex, expected_zip):
    m = regex.search(zip_name)
    if m:
        zip_type = m.group()
        if zip_type not in expected_zip:
             zip_types[zip_type].add(zip_name)

def is_zip_name(elem):
    return (elem.attrib['k'] == "addr:postcode")

def audit(filename, regex):
    for event, elem in ET.iterparse(filename, events=("start",)):
        if elem.tag == "way" or elem.tag == "node":
            for tag in elem.iter("tag"):
                if is_zip_name(tag):
                    audit_zip_codes(zip_types, tag.attrib['v'], regex, expected_zip)
    pprint.pprint(dict(zip_types))

audit(filename, zip_type_re)


# In[12]:

# Convert all zip codes to a standard 5 digit display
# by removing any entries with more than 5 digits,
# removing the "+4" extensions,
# and clean any that contain "HI"

for zip_type, ways in zip_types.iteritems(): 
        for name in ways:
            if "-" in name:
                name = name.split("-")[0].strip()
            if "HI" in name:
                name = name.split("HI")[1].strip('HI ')
            print name


# In[13]:

# Check for problematic tags

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


# In[14]:

# Import the necessary packages

# import xml data into a csv file for later integration into sql database
# first load necessary packages
import csv
import codecs
import re
import xml.etree.cElementTree as ET

import cerberus

import schema


# In[15]:

# create the csv files

OSM_PATH = "c:\honolulu_hawaii.osm"
NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


# In[16]:

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


# In[17]:

process_map(OSM_PATH)


# In[18]:

# Store schema in a .py file in order for int() and float() coercion functions.

SCHEMA = {
    'node': {
        'type': 'dict',
        'schema': {
            'id': {'required': True, 'type': 'integer', 'coerce': int},
            'lat': {'required': True, 'type': 'float', 'coerce': float},
            'lon': {'required': True, 'type': 'float', 'coerce': float},
            'user': {'required': True, 'type': 'string'},
            'uid': {'required': True, 'type': 'integer', 'coerce': int},
            'version': {'required': True, 'type': 'string'},
            'changeset': {'required': True, 'type': 'integer', 'coerce': int},
            'timestamp': {'required': True, 'type': 'string'}
        }
    },
    'node_tags': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'key': {'required': True, 'type': 'string'},
                'value': {'required': True, 'type': 'string'},
                'type': {'required': True, 'type': 'string'}
            }
        }
    },
    'way': {
        'type': 'dict',
        'schema': {
            'id': {'required': True, 'type': 'integer', 'coerce': int},
            'user': {'required': True, 'type': 'string'},
            'uid': {'required': True, 'type': 'integer', 'coerce': int},
            'version': {'required': True, 'type': 'string'},
            'changeset': {'required': True, 'type': 'integer', 'coerce': int},
            'timestamp': {'required': True, 'type': 'string'}
        }
    },
    'way_nodes': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'node_id': {'required': True, 'type': 'integer', 'coerce': int},
                'position': {'required': True, 'type': 'integer', 'coerce': int}
            }
        }
    },
    'way_tags': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'id': {'required': True, 'type': 'integer', 'coerce': int},
                'key': {'required': True, 'type': 'string'},
                'value': {'required': True, 'type': 'string'},
                'type': {'required': True, 'type': 'string'}
            }
        }
    }
}


# In[19]:

NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']
def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""
    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements
    poscounter = 0 #for way nodes position
    
    if element.tag == 'node':
        for field in NODE_FIELDS:
            node_attribs[field] = element.attrib[field]
        for tag in element.iter('tag'):
            tag_dict = {}
            tag_dict['id'] = element.attrib['id'] #id (NODE_TAGS_FIELDS)
            
            #key and type (NODE_TAGS_FIELDS)
            if PROBLEMCHARS.match(tag.attrib["k"]):
                pass
            elif ':' in tag.attrib['k']:
                tag_dict['type'] = tag.attrib['k'].split(':')[0]
                tag_dict['key'] = tag.attrib["k"].split(':',1)[1]
            else:
                tag_dict['type'] = 'regular'
                tag_dict['key'] = tag.attrib['k']
                
            #value (NODE_TAGS_FIELDS)
            tag_dict['value'] = tag.attrib['v']
            
            tags.append(tag_dict)
        return {'node': node_attribs, 'node_tags': tags}
        
    elif element.tag == 'way':
        for field in WAY_FIELDS:
            way_attribs[field] = element.attrib[field]
        for nd in element.iter('nd'):
            nd_dict = {}
            nd_dict['id'] = element.attrib['id']
            nd_dict['node_id'] = nd.attrib['ref']
            nd_dict['position'] = poscounter
            poscounter += 1
            way_nodes.append(nd_dict)
        for tag in element.iter('tag'):
            tag_dict = {}
            tag_dict['id'] = element.attrib['id'] #id
            #key and type
            if PROBLEMCHARS.match(tag.attrib["k"]):
                pass
            elif ':' in tag.attrib['k']:
                tag_dict['type'] = tag.attrib['k'].split(':')[0]
                tag_dict['key'] = tag.attrib["k"].split(':',1)[1]
            else:
                tag_dict['type'] = 'regular'
                tag_dict['key'] = tag.attrib['k']
            #value
            tag_dict['value'] = tag.attrib['v']
            
            tags.append(tag_dict)    
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# In[20]:

# HELPER FUNCTIONS    
    
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""
    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()
def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_strings = (
            "{0}: {1}".format(k, v if isinstance(v, str) else ", ".join(v))
            for k, v in errors.iteritems()
        )
        raise cerberus.ValidationError(
            message_string.format(field, "\n".join(error_strings))
        )
class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""
    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })
    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# In[21]:

# MAIN FUNCTION
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""
    with codecs.open(NODES_PATH, 'w') as nodes_file,          codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file,          codecs.open(WAYS_PATH, 'w') as ways_file,          codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file,          codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:
        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)
        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()
        validator = cerberus.Validator()
        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)
                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])

process_map(OSM_PATH, validate=False)


# In[22]:

# import sqlite3
import sqlite3
import csv
from pprint import pprint
sqlite_file = 'OpenStreetMap_Oahu.db'    # name of the sqlite database file
# Connect to the database
conn = sqlite3.connect(sqlite_file)
# Get a cursor object
cur = conn.cursor()
def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]
def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')
        
def UnicodeDictReader(utf8_data, **kwargs):
    csv_reader = csv.DictReader(utf8_data, **kwargs)
    for row in csv_reader:
        yield {key: unicode(value, 'utf-8') for key, value in row.iteritems()}


# In[23]:

# Create the table, specifying the column names and data types:
cur.execute('''
    CREATE TABLE nodes_tags(id INTEGER, key TEXT, value TEXT,type TEXT)
''')
cur.execute('''
    CREATE TABLE nodes(id INTEGER, lat REAL, lon REAL, user TEXT, uid INTEGER, 
    version INTEGER, changeset INTEGER, timestamp TIMESTAMP)
''')
cur.execute('''
    CREATE TABLE ways(id INTEGER, user TEXT, uid INTEGER, changeset INTEGER, timestamp TIMESTAMP)
''')
cur.execute('''
    CREATE TABLE ways_tags(id INTEGER, key TEXT, value TEXT, type TEXT) 
''')
cur.execute('''
    CREATE TABLE ways_nodes(id INTEGER, node_id INTEGER, position INTEGER)
''')
# commit the changes
conn.commit()


# In[24]:

# Read in the csv file as a dictionary, format the data as a list of tuples

with open('nodes_tags.csv','rb') as fin:
    dr = UnicodeDictReader(fin) # comma is default delimiter
    to_db = [(i['id'], i['key'],i['value'], i['type']) for i in dr]
with open('nodes.csv', 'rb') as fin2:
    dr2 = UnicodeDictReader(fin2)
    to_db2 = [(i['id'], i['lat'], i['lon'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in dr2]
    
with open('ways.csv', 'rb') as fin3:
    dr3 = UnicodeDictReader(fin3)
    to_db3 = [(i['id'], i['user'], i['uid'], i['changeset'], i['timestamp']) for i in dr3]
    
with open('ways_tags.csv', 'rb') as fin4:
    dr4 = UnicodeDictReader(fin4)
    to_db4 = [(i['id'], i['key'], i['value'], i['type']) for i in dr4]  
    
with open('ways_nodes.csv', 'rb') as fin5:
    dr5 = UnicodeDictReader(fin5)
    to_db5 = [(i['id'], i['node_id'], i['position']) for i in dr5]  
    
    # insert the formatted data
cur.executemany("INSERT INTO nodes_tags(id, key, value,type) VALUES (?, ?, ?, ?);", to_db)
cur.executemany("INSERT INTO nodes(id, lat, lon, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db2)
cur.executemany("INSERT INTO ways(id, user, uid, changeset, timestamp) VALUES (?, ?, ?, ?, ?);", to_db3)
cur.executemany("INSERT INTO ways_tags(id, key, value, type) VALUES (?, ?, ?, ?);", to_db4)
cur.executemany("INSERT INTO ways_nodes(id, node_id, position) VALUES (?, ?, ?);", to_db5)

# commit the changes
conn.commit()
cur.execute('SELECT * FROM nodes_tags')
all_rows = cur.fetchall()
print('1):')
pprint(all_rows)
conn.close()


# In[25]:

# Counting number of nodes
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()
cur.execute('''
    SELECT COUNT(*) FROM nodes;
''')
all_rows = cur.fetchall()
print('Number of nodes are:{}').format(all_rows)
conn.commit()


# In[26]:

# Counting number of ways
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()
cur.execute('''
    SELECT COUNT(*) FROM ways;
''')
all_rows = cur.fetchall()
print('Number of ways are:{}').format(all_rows)
conn.commit()


# In[27]:

# Counting number of unique users
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()
cur.execute('''
SELECT COUNT(DISTINCT(e.uid))          
FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e;
''')
all_rows = cur.fetchall()
print('Number of unique users are:{}').format(all_rows)
conn.commit()


# In[28]:

# TOP 10 contributing users
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()
cur.execute('''
SELECT e.user, COUNT(*) as num
FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
GROUP BY e.user
ORDER BY num DESC
LIMIT 10;
''')
all_rows = cur.fetchall()
print('Number of unique users are:')
pprint(all_rows)
conn.commit()


# In[29]:

# Number users appearing once
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()
cur.execute('''
SELECT COUNT(*) 
FROM
    (SELECT e.user, COUNT(*) as num
     FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
     GROUP BY e.user
     HAVING num=1)  u;
''')
all_rows = cur.fetchall()
print('Number of unique users only appearing once are:')
pprint(all_rows)
conn.commit()


# In[30]:

# Number of users less than 10
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()
cur.execute('''
SELECT COUNT(*) 
FROM
    (SELECT e.user, COUNT(*) as num
     FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
     GROUP BY e.user
     HAVING num<10)  u;
''')
all_rows = cur.fetchall()
print('Number of unique users appearing less than 10 times are:')
pprint(all_rows)
conn.commit()


# In[31]:

# List metro areas of O'ahu
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()
cur.execute('''
SELECT tags.value, COUNT(*) as count 
FROM (SELECT * FROM nodes_tags UNION ALL 
      SELECT * FROM ways_tags) tags
WHERE tags.key LIKE '%city'
GROUP BY tags.value
ORDER BY count DESC;
''')
all_rows = cur.fetchall()
print('1):')
pprint(all_rows)
conn.commit()


# In[32]:

# Top 10 tourist ameneties
import pprint
cur.execute ("SELECT tags.value, COUNT(*) as count FROM (SELECT * FROM nodes_tags UNION ALL              SELECT * FROM ways_tags) tags              WHERE tags.key LIKE '%tourism'             GROUP BY tags.value              ORDER BY count DESC LIMIT 10;")
pprint.pprint(cur.fetchall())


# In[33]:

# Number of restaurants by metro area
import pprint
cur.execute("SELECT nodes_tags.value, COUNT(*) as num FROM nodes_tags JOIN (SELECT DISTINCT(id)             FROM nodes_tags WHERE value = 'restaurant') i ON nodes_tags.id = i.id WHERE nodes_tags.key = 'city'            GROUP BY nodes_tags.value ORDER BY num DESC;")
pprint.pprint(cur.fetchall())


# In[34]:

# Top 10 types of food
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()
cur.execute('''
SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags 
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='restaurant') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='cuisine'
GROUP BY nodes_tags.value
ORDER BY num DESC
Limit 10;
''')
all_rows = cur.fetchall()
print('1):')
pprint.pprint(all_rows)
conn.commit()


# In[ ]:



