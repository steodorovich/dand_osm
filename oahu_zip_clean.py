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

