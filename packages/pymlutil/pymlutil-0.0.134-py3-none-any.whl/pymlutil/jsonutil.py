import os
import json
import yaml
import subprocess
import sys
import io
import selectors
from datetime import datetime

def WriteDictJson(outdict, path):

    jsonStr = json.dumps(outdict, indent=2, sort_keys=False)
    with open(path,"w") as f:
        f.write(jsonStr)
    return True

def ReadDictJson(filepath):
    jsondict = None
    try:
        with open(filepath) as json_file:
            jsondict = json.load(json_file)
        if not jsondict:
            print('Failed to load {}'.format(filepath))
    except:
        print('Failed to load {}'.format(filepath))
    return jsondict

def Dict2Json(outdict):
    jsonStr = json.dumps(outdict, sort_keys=False, indent=4)      
    return jsonStr

def Json2Dict(json_file):
    jsondict = json.load(json_file)
    return jsondict

def ReadDictYaml(filepath):
    yamldict = {}
    try:
        with open(filepath) as yaml_file:
            yamldict = yaml.safe_load(yaml_file)
        if not yamldict:
            print('Failed to load {}'.format(filepath))
    except ValueError:
        print('Failed to load {} error {}'.format(filepath, ValueError))
    return yamldict

def WriteDictYaml(outdict, path):
    yamlStr = yaml.dump(outdict, indent=2, sort_keys=False)
    with open(path,"w") as f:
        f.write(yamlStr)
    return True

def ReadDict(filepath):
    ext = os.path.splitext(filepath)[1]
    if ext=='.yaml':
        readDict = ReadDictYaml(filepath)
    elif ext=='.json':
        readDict = ReadDictJson(filepath)
    else:
        readDict = None
    return readDict

def WriteDict(outdict, filepath):
    ext = os.path.splitext(filepath)[1]
    if ext=='.yaml':
        readDict = WriteDictYaml(outdict, filepath)
    elif ext=='.json':
        readDict = WriteDictJson(outdict, filepath)
    else:
        readDict = None
    return readDict

def str2bool(v):
    if isinstance(v, bool):
        return v
    if isinstance(v, int):
        return not(v==0)
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

# https://stackoverflow.com/questions/2231227/python-subprocess-popen-with-a-modified-environment
def cmd(command, check=True, shell=True, timeout=None, capture_output=False):
    initial = datetime.now()
    print('$ {}'.format(command))
    result = subprocess.run(command, shell=shell, capture_output=capture_output, check=check, timeout=timeout)

    dt = (datetime.now()-initial).total_seconds()
    if capture_output is True:
        if result.stdout: print(result.stdout.decode("utf-8"))
        if result.stdout: print(result.stderr.decode("utf-8"))
    print('result {} in {}s'.format(result.returncode, dt))
    return result.returncode, result.stderr, result.stdout

# def cmd(command, check=True, shell=True, timeout=None):
#     # Start subprocess
#     # bufsize = 1 means output is line buffered
#     # universal_newlines = True is required for line buffering
#     process = subprocess.Popen(command,
#                                bufsize=1,
#                                stdout=subprocess.PIPE,
#                                stderr=subprocess.STDOUT,
#                                universal_newlines=True)

#     # Create callback function for process output
#     buf = io.StringIO()
#     def handle_output(stream, mask):
#         # Because the process' output is line buffered, there's only ever one
#         # line to read when this function is called
#         line = stream.readline()
#         buf.write(line)
#         sys.stdout.write(line)

#     # Register callback for an "available for read" event from subprocess' stdout stream
#     selector = selectors.DefaultSelector()
#     selector.register(process.stdout, selectors.EVENT_READ, handle_output)

#     # Loop until subprocess is terminated
#     while process.poll() is None:
#         # Wait for events and handle them with their registered callbacks
#         events = selector.select()
#         for key, mask in events:
#             callback = key.data
#             callback(key.fileobj, mask)

#     # Get process return code
#     return_code = process.wait()
#     selector.close()

#     if check and return_code != 0:
#         raise Exception("{} failed {}".format(command, return_code)) 

    # Store buffered output
    output = buf.getvalue()
    buf.close()

    return (return_code, None, process.stdout)