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
