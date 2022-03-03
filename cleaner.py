import requests
url = input('host: ')
user = input('login: ')
passw = input('password: ')
repo = input('choose repository to clean: ')
vers_pr = input('version: ')
name_pr =input('name: ')
ids_to_delete=[]
components_response = requests.get(url+'service/rest/v1/components?repository='+repo,auth=(user, passw))
dict=components_response.json()
for i in range (len(dict['items'])):
    if dict['items'][i]['version'].find(vers_pr)>=0:
        if name_pr != '':
            if dict['items'][i]['name'].find(name_pr)>=0:
                ids_to_delete.append(dict['items'][i]['id'])
        else: ids_to_delete.append(dict['items'][i]['id'])
continuationToken = dict['continuationToken']
print(continuationToken)
while True:
    components_response = requests.get(url+'service/rest/v1/components?repository='+repo,auth=(user, passw),params={'continuationToken':continuationToken})
    dict=components_response.json()
    for i in range (len(dict['items'])):
        if dict['items'][i]['version'].find(vers_pr)>=0:
            if name_pr != '':
                if dict['items'][i]['name'].find(name_pr)>=0:
                    ids_to_delete.append(dict['items'][i]['id'])
            else: ids_to_delete.append(dict['items'][i]['id'])
    print('следующая страница')
    continuationToken = dict['continuationToken']
    if continuationToken == None:
        break
print(ids_to_delete)
for id in ids_to_delete:
    requests.delete(url+'service/rest/v1/components/'+id, auth=(user, passw))
    print('Удалил)', id)