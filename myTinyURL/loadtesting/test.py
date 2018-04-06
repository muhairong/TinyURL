import json

config = {
    'read_weight' : 5,
    'write_weight' : 1,
    'qps' : 10,
    'runtime' : 10,
    'worker_num' : 3,
    'hostname' : 'http://127.0.0.1:8000',
    'convert_url' : '/convert/shorten',
    'index_url' : '/convert/'
}

with open('config.json', 'w') as f:
    json.dump(config, f)


'''
weight [5,1]
qps 10
runtime 10
worker_num 3
hostname http://127.0.0.1:8000
convert_url /convert/shorten
index_url /convert/

import string

def loadConfig():
    f = open('testconfig', 'r')
    for line in f:
        if line.startswith('weight'):
            weight = line.split()[1]
            w = list(map(int, weight.split(',')))
            print(w)
        elif line.startswith('qps'):
            qps = line.split()[1]
            print(qps)
        elif line.startswith('runtime'):
            runtime = line.split()[1]
            print(runtime)
        elif line.startswith('worker_num'):
            worker_num = line.split()[1]
            print(worker_num)
        elif line.startswith('hostname'):
            hostname = line.split()[1]
            print(hostname)
        elif line.startswith('convert_url'):
            convert_url = line.split()[1]
            print(convert_url)
        elif line.startswith('index_url'):
            index_url = line.split()[1]
            print(index_url)
'''