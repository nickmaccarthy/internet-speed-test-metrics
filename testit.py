import speedtest
from pprint import pprint 
import datetime
import time 
import json 
import yaml 
import logging 
import os 
import sys 

logging.basicConfig(format="%(asctime)s - %(name)s - [ %(levelname)s ] - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

SHOME = os.path.abspath(os.path.join(os.path.dirname(__file__)))

def load_config(path=os.path.join(SHOME, 'config.yml')):
    with open(path, 'r') as f:
        try:
            doc = yaml.load(f)
            return doc 
        except Exception as e:
            logger.exception('Unable to open yaml config at: {}, reason: {}'.format(path, e))
config = load_config()

output_file = config.get('output_file', 'output.json')

def run_test():
    res = {}
    try: 
        s = speedtest.Speedtest()
        s.get_servers()
        s.get_best_server()
        s.download()
        s.upload()
        res.update(s.results.dict())
        res['@timestamp'] = res['timestamp'] 
        res['internet-accessable'] = 'yes'
    except Exception as e:
        ts = datetime.datetime.utcnow()
        ts = ts.isoformat()
        res['@timestamp'] = ts 
        res['message'] = 'not able to get to internet'
        res['internet-accessable'] = 'no'
        res['upload'] = 0
        res['download'] = 0
        res['bytes_sent'] = 0
        res['bytes_received'] = 0 

    
    pprint(res)

    with open(output_file, 'a+') as f:
        f.write("%s\n" % (json.dumps(res))) 


if __name__ == "__main__":
    while True:
        run_test()
        time.sleep(config.get('run_interval', 120))