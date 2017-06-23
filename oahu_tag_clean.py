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
