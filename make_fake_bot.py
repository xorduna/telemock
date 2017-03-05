import requests

names = ['xavi', 'elies', 'joan', 'nuria', 'diana', 'arnau']

lastnames = ['campo', 'orduna', 'galisteo', 'just', 'cid']

numeric_lastnames = range(101, 500)

botname = '@telemock'

telemock_endpoint = "http://localhost:5000"

for name in names:
    #for lastname in lastnames:
    #    username = '@'+name+lastname
    #    requests.post(telemock_endpoint+'/user', json={'username': username, 'first_name': name, 'last_name': lastname})
    #    requests.post(telemock_endpoint+'/chat', json={'botname': botname, 'username': username })
    for lastname in numeric_lastnames:
        username = '@'+name+str(lastname)
        print(username)
        requests.post(telemock_endpoint+'/user', json={'username': username, 'first_name': name, 'last_name': str(lastname)})
        requests.post(telemock_endpoint+'/chat', json={'botname': botname, 'username': username })