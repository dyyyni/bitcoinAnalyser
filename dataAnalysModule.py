import json

def jprint(activeData):
# create a formatted string of the Python JSON object
    text = json.dumps(activeData, sort_keys=True, indent=4)
    print(text)