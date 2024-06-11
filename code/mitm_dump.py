import mitmproxy
from mitmproxy import http
import json
import time
import os
import re
from dotenv import load_dotenv
import logging

load_dotenv()
dump_dir = os.environ["DUMP_DIR"]
avd = os.environ["AVD"]

def target_list():
  return {".*whispers/nearby.*":os.path.join(dump_dir, avd)}

def response(flow: http.HTTPFlow) -> None:
  url = flow.request.url
  matches = target_list()
  if matches is not None:
    for patternURL, dumpFolder in matches.items():  
      if not os.path.exists(dumpFolder):
        os.makedirs(dumpFolder)
      if re.match(patternURL, url) is not None:
        dumpFile = dumpFolder + '/' + str(int(round(time.time()*1000)))
        try:
          with open(dumpFile,'a') as f:
            f.write(str(flow.request.method) + ' ' + str(flow.request.url) + '\n')
            for k, v in flow.request.headers.items():
                f.write(str(k) + ': ' + str(v) + '\n')
            f.write('\n' + str(flow.request.content.decode('utf-8')) + '\n')
            f.write('---\n')
            for k, v in flow.response.headers.items():
                f.write(str(k) + ': ' + str(v) + '\n')
            f.write('\n' + str(flow.response.content.decode('utf-8')) + '\n')
        except Exception as e:
          print(e)
      