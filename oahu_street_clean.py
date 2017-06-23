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
            name_improv_first = update_name(name, mapping, street_type_re)
            name_improv_sec = update_name(name_improv_first, mapping2, street_type_pre)
            
            print name, "=>", name_improv_first, "=>", name_improv_sec

