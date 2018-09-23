#!/usr/bin/env python
# encoding: utf-8
'''
    predict 

Usage:
    predict.py <model_file> <ipc_channel_name>

Options:
    -o <option>    some option
    -h --help      show this help message and exit.
'''
from docopt import docopt
import pandas as pd
import numpy as np
from predict_pb2 import pick
from predict_pb2 import features
#retrieving arguments
args = docopt(__doc__, version='1.0.0rc2')

import zmq 
chan='ipc:///tmp/'+str(args['<ipc_channel_name>'])+".ipc"
ctx = zmq.Context.instance()
sock = ctx.socket(zmq.REP)
sock.bind(chan)

import signal
import sys
import inspect
import time

def sigterm_handler(_signo, _stack_frame):
  sock.close()
  sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)

from sklearn.externals import joblib
p = joblib.load(args['<model_file>']) 

while True:
  r = sock.recv()
  feat=features()
  feat.ParseFromString(r)
  a=list(feat.ListFields()[0][1])
  choice=pd.DataFrame(p.predict(np.array(a).reshape(1, -1)))
  c = int(choice.idxmin(axis=1)[0])
  pck=pick()
  pck._=c
  otp=pck.SerializeToString()
  sock.send(otp)

# sock.close()
