import os

def install():
    os.system('pip install instabase==0.0.3')

install()

from instabase.apps import Client

app_name, app_version = 'US Bank Statements', '3.0.0'
file_url = 'https://apps.instabase.com/static/assets/images/cloud-developers/us-bs/sample-us-bs-1.jpeg'

client = Client()
# resp = client.extract_from_input_url(file_url, app_name, app_version)
# print(resp)

with open(dir_path+'tests/instabase/apps/data/test_data_bank_statement.pdf','rb') as f:
	print(f.read()) 