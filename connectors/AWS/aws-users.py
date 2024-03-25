#!/usr/bin/env python3
#
import boto3, json, requests, datetime

def get_users():
    try:
        iam = boto3.client("iam")
        users = iam.list_users()
        #print(users)
        user_list=list()
        custom_list=list()
        for key in users['Users']:
            user_list.append(key['UserName'])
            #custom_list.append(key['Arn'])  (if you want the ARN as a custom field)
            custom_list.append('')
        HTTPStatusCode=users['ResponseMetadata']['HTTPStatusCode']
        return user_list, custom_list, HTTPStatusCode
    except Exception as err:
      return str(err), "", 0


################################################################
USER_PATROL_GUID=""
USER_PATROL_SOURCE_GUID=""
today = datetime.datetime.now()
today_date = today.strftime("%Y-%m-%d")
#today_date = "2024-03-16"

json_middle=''
user_list_result, custom_list_result, HTTPStatusCode = get_users()
if HTTPStatusCode == 200:
    for i in range(0, len(user_list_result)):
        json_middle = json_middle + '{ "username" : "' + user_list_result[i] + '", "custom" : "' + custom_list_result[i] + '" },'
else:
    print(user_list_result)
    exit()


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
#print(jsondata)

url = "https://userpatrol.com/api"
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
res = requests.post(url, data=jsondata, headers=headers)
print(res)
