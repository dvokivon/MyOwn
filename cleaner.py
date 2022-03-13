import requests

def checker():
    global url,sl
    a=list(url)
    if a[-1]!='/':
        sl='/'
    else:
        sl=''
    return sl

def search_for_matches(vers_pr,name_pr):
    dict=components_response.json()
    for i in range (len(dict['items'])):
        if dict['items'][i]['version'].find(vers_pr)>=0:
            if name_pr != '':
                if dict['items'][i]['name'].find(name_pr)>=0:
                    ids_to_delete.append(dict['items'][i]['id'])
            else: ids_to_delete.append(dict['items'][i]['id'])
    continuationToken = dict['continuationToken']
    print(continuationToken)
    return continuationToken, dict
    
url = input('host: ')
user = input('login: ')
passw = input('password: ')
repo = input('choose repository to clean: ')
vers_pr = input('version: ')
name_pr =input('name: ')
ids_to_delete=[]
checker()
components_response = requests.get(url+sl+'service/rest/v1/components?repository='+repo,auth=(user, passw))
search_for_matches(vers_pr,name_pr)
print('next page')
while True:
    components_response = requests.get(url+sl+'service/rest/v1/components?repository='+repo,auth=(user, passw),params={'continuationToken':continuationToken})
    search_for_matches(vers_pr,name_pr)  
    print('next page')
    if continuationToken == None:
        break
print(ids_to_delete)
for id in ids_to_delete:
    requests.delete(url+'service/rest/v1/components/'+id, auth=(user, passw))
    print('i`ve deleted ', id)