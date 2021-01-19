import json
# import aegdataset.datajson as datajson

with open('datajson.json', 'r') as f:
    distros_dict = json.load(f)

for distro in distros_dict:
    print(distro['word'])
