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

