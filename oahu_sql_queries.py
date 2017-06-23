# Counting number of nodes
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()
cur.execute('''
    SELECT COUNT(*) FROM nodes;
''')
all_rows = cur.fetchall()
print('Number of nodes are:{}').format(all_rows)
conn.commit()

# Counting number of ways
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()
cur.execute('''
    SELECT COUNT(*) FROM ways;
''')
all_rows = cur.fetchall()
print('Number of ways are:{}').format(all_rows)
conn.commit()

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

# Top 10 tourist ameneties
import pprint
cur.execute ("SELECT tags.value, COUNT(*) as count FROM (SELECT * FROM nodes_tags UNION ALL \
             SELECT * FROM ways_tags) tags \
             WHERE tags.key LIKE '%tourism'\
             GROUP BY tags.value \
             ORDER BY count DESC LIMIT 10;")
pprint.pprint(cur.fetchall())

# Number of restaurants by metro area
import pprint
cur.execute("SELECT nodes_tags.value, COUNT(*) as num FROM nodes_tags JOIN (SELECT DISTINCT(id) \
            FROM nodes_tags WHERE value = 'restaurant') i ON nodes_tags.id = i.id WHERE nodes_tags.key = 'city'\
            GROUP BY nodes_tags.value ORDER BY num DESC;")
pprint.pprint(cur.fetchall())

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
