from sdg.open_sdg import open_sdg_build
import requests
import json

data = {}

with open('px_api.json', 'r') as f:
    data = json.load(f)

assert "indicators" in data
indicators = data["indicators"]

output_dir = "data"

if "output_dir" in data:
   output_dir = data["output_dir"]

for indicator in indicators:
  assert "csv_file" in indicator
  assert "url" in indicator
  assert "request" in indicator

  csvname = indicator["csv_file"]
  url = indicator["url"]
  request_data = indicator["request"]

  response = requests.post(url, json=request_data)
  csv_data = response.text
  csv_header = ""

  if "csv_header" in indicator:
     csv_header = indicator["csv_header"]
  else:
     csv_header = "Year,Value"
  
  lines = csv_data.splitlines()[1:]
  output_str = csv_header

  for line in lines:
     line_out = line.replace('"', '')
     output_str += '\n' + line_out
  
  out_path = output_dir + "/" + csvname

  with open(out_path, 'w') as f:
     f.write(output_str)
  
  print("Processed " + csvname)

open_sdg_build(config='config_data.yml')
