import requests,json
from requests.exceptions import HTTPError

ORG="[MY_ORG]"
TEAM="[TEAM NAME]"
ACCESS_TOKEN='[API TOKEN]'

USER_PATROL_GUID=""
USER_PATROL_SOURCE_GUID=""

today = datetime.datetime.now()
today_date = today.strftime("%Y-%m-%d")

URL="https://api.github.com/orgs/" + ORG + "/teams/" + TEAM + "/members"
headers = {'Accept': 'application/json','Authorization': 'Bearer ' + ACCESS_TOKEN}

try:
    response = requests.get(URL, headers=headers)
    response.raise_for_status()
    jsonResponse = response.json()
except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
    exit()
except Exception as err:
    print(f'Other error occurred: {err}')
    exit()

json_middle=''

# Iterate through the JSON array
for item in jsonResponse:
    login=item["login"]
    #print(login + ' : ' + TEAM)
    json_middle = json_middle + '{ "username" : "' + login + '", "custom" : "' + TEAM + '" },'

json_top='''
{
   "tenant_guid" : "<tenant_guid>",
   "source_guid" : "<source_guid>",
   "date_added" : "<date_added>",
   "users" : [
'''

json_top = json_top.replace("<tenant_guid>", USER_PATROL_GUID)
json_top = json_top.replace("<source_guid>", USER_PATROL_SOURCE_GUID)
json_top = json_top.replace("<date_added>", today_date)

json_end='''
      ]
}
'''

json_middle = json_middle[:-1]
jsondata = json_top + json_middle + json_end

url = "https://userpatrol.com/api"
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
res = requests.post(url, data=jsondata, headers=headers)
print(res)
