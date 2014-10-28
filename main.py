
import json, os, configparser
import external.requests as requests

try:
  config = configparser.ConfigParser()
  config.read('settings.ini')
  s = config['Configuration']
except:
  s = {}

SERVER_ADDR = s.get('SERVER_ADDR', 'http://localhost')
PAGES_PATH = s.get('PAGES_PATH', '/')
OUTPUT_PATH = s.get('OUTPUT_PATH', 'output/')
TEST_CASES_FILE = s.get('TEST_CASES_FILE', 'testCases.json')
USE_SESSION = s.get('USE_SESSION', False) == 'True'
# == is to convert string 'True' to bool. We
# do not getboolean because s may be a dict


if not os.path.exists(OUTPUT_PATH):
  os.mkdir(OUTPUT_PATH)

if USE_SESSION:
  requests = requests.Session()

jsonString = open(TEST_CASES_FILE, 'r').read()

allPages = json.loads(jsonString)


def sendGet(url, params, fout):
  r = requests.get(url, params = params)
  
  print('GET '+url, r.status_code, sep = '\n')
  print('GET : ' + url, r.status_code, r.headers, r.text, sep = '\n  ',
        end = '============================\n', file = fout)


def sendPost(url, data, fout):
  if 'GETquery' in data:
    params = data['GETquery']
    del data['GETquery']
  else:
    params = {}
  
  r = requests.post(url, params = params, data = data)
  
  print('POST '+url, r.status_code, sep = '\n')
  print('POST : ' + url, r.status_code, r.headers, r.text, sep = '\n  ',
        end = '============================\n', file = fout)


for page in allPages:
  path = SERVER_ADDR + PAGES_PATH + page['file']
  output = open(OUTPUT_PATH + page['file'] + '.txt', 'w')
  
  for get in page['get']:
    sendGet(path, get, output)
  
  for post in page['post']:
    sendPost(path, post, output)
  
  output.close()
