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
            #custom_list.append(key['Arn'])  # (if you want the ARN as a custom field)
            custom_list.append('')  # set custom field to blank
        HTTPStatusCode=users['ResponseMetadata']['HTTPStatusCode']
        return user_list, custom_list, HTTPStatusCode
    except Exception as err:
      return str(err), "", 0

def get_user_dates(iamuser):
    try:
        iam = boto3.resource('iam')
        user = iam.User(iamuser)
        create_date = user.create_date
        # use the account creation date if the user has never logged in.
        password_last_used = user.password_last_used or user.create_date
        create_date=str(create_date)[:10]
        password_last_used=str(password_last_used)[:10]
        return create_date, password_last_used
    except Exception as err:
      return "1970-01-01", "1970-01-01"

################################################################
USER_PATROL_GUID=""
USER_PATROL_SOURCE_GUID=""

json_middle=''
user_list_result, custom_list_result, HTTPStatusCode = get_users()
if HTTPStatusCode == 200:
    for i in range(0, len(user_list_result)):
        iamuser=user_list_result[i]
        create_date, password_last_used = get_user_dates(iamuser)
        json_string = json.dumps({'username': iamuser, 'create_date' : create_date , 'last_login_date': password_last_used})
        json_middle += json_string + ','
else:
    print(user_list_result)
    exit()


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
