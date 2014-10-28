
import json, os
import external.requests as requests

SERVER_ADDR = 'http://localhost'
PAGES_PATH = '/pa/'
OUTPUT_PATH = 'output/'
TEST_CASES_FILE = 'testCases.json'
USE_SESSION = False


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
