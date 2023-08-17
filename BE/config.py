import os.path
import json
import os

if os.path.isfile('./conf/conf.json') is False:
    with open('./conf/conf.json', 'w') as newconf:
        conf = {}
        json.dump(conf, newconf, indent=4)

with open('./conf/conf.json', 'r') as mainconf:
    conf = json.load(mainconf)


