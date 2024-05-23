import json,os,sys,string,time,datetime,requests,html
import urllib
from urllib.parse import urlparse
from urllib.parse import parse_qs


OKTA_URLBASE="https://dev-000000-admin.okta.com"
OKTA_TOKEN=""
USER_PATROL_GUID=""
USER_PATROL_SOURCE_GUID=""


def call_okta(action, url):
    headers = {'Content-type': 'application/json', 'Accept': 'application/json', 'Authorization': 'SSWS ' + OKTA_TOKEN}
    try:
        if action == 'get':
            result = requests.get(url, headers=headers)

        result.raise_for_status()
        parsed_json = json.loads(result.text)
        return(parsed_json)
    except:
        return("Error")



def fetch_okta_users():
    url = "{}/api/v1/users".format(OKTA_URLBASE)
    headers = {'Content-type': 'application/json', 'Accept': 'application/json', 'Authorization': 'SSWS ' + OKTA_TOKEN}

    okta_users = []
    done = False

    after_token = None
    while not done:
        params = {
            'limit': 200,
        }

        if after_token:
            params['after'] = after_token

        list_users_response = requests.get(url=url,params=params,headers=headers)

        if list_users_response.status_code != 200:
            raise Exception("Got HTTP {} listing users",
                            list_users_response.status_code)

        list_users_response_body = list_users_response.json()
        okta_users.extend(list_users_response_body)
        if 'next' in list_users_response.links:
            next_url = list_users_response.links['next']['url']
            after_token = parse_qs(urlparse(next_url).query)['after'][0]
        else:
            done = True

        time.sleep(1)

    #print(okta_users)
    return okta_users



#############################################################################
#
# main
#

json_middle = ''
user_list = fetch_okta_users()
#print(user_list)

for user_info in user_list:
    email = user_info['profile']['email']
    fname = user_info['profile']['firstName']
    lname = user_info['profile']['lastName']
    name = fname + ' ' + lname
    json_middle = json_middle + '{ "username" : "' + email + '", "custom" : "' + name + '" },'


json_top='''
{
   "tenant_guid" : "<tenant_guid>",
   "source_guid" : "<source_guid>",
   "users" : [
'''

json_top = json_top.replace("<tenant_guid>", USER_PATROL_GUID)
json_top = json_top.replace("<source_guid>", USER_PATROL_SOURCE_GUID)

json_end='''
      ]
}
'''

json_middle = json_middle[:-1]
jsondata = json_top + json_middle + json_end

#print(jsondata)

url = "https://userpatrol.com/api"
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
res = requests.post(url, data=jsondata, headers=headers)
print(res)
