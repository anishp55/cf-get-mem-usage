import requests

def getAuth(user,password, loginUrl):
    querystring = {
                        "username": user,  #get from UI
                        "password": password, #get from UI
                        "response_type":"token",
                        "grant_type":"password",
                        "client_id": "cf"
                }

    headers = {
        'authorization': "Basic Y2Y6",
        'accept': "application/json;charset=utf-8"
        }
    
    response = requests.post(
                                loginUrl,
                                headers=headers,
                                params=querystring,
                                verify=False
                             )
    
    tokens = response.json()
    tokens['scope'] = tokens['scope'].split()

    return (tokens)

def createAuthHeader(accessToken):
    return(
        {
            'content-type': "application/json",
            'Authorization': 'bearer ' + accessToken
        }
    )

def getOrgsSummary(header,apiUrl,endpoint="/v2/organizations"):
    orgCount = 0
    bail = True
    pageCounter = 1
    orgDetails = []
    while bail:
        querystring = {
            "order-direction": "asc",
            "page": pageCounter,
            "results-per-page": 100  # allow setting through ui (must be less than 100)
        }

        response = requests.get(
                                    apiUrl.format(endpoint),
                                    headers=header,
                                    params=querystring,
                                    verify=False
                                )
        for orgs in response.json()['resources']:
            usageSummary = requests.get(
                                         apiUrl.format(orgs['metadata']['url']+'/summary'),
                                         headers=header,
                                         verify=False
            )
            #get memory usuage for the org
            orgMemUsage = 0
            for items in usageSummary.json()['spaces']:
                orgMemUsage = orgMemUsage + items['mem_dev_total'] + items['mem_prod_total']
            orgCount = orgCount + 1
            quotaInfo = getQuotaDefinition(header= header, apiUrl=apiUrl,
                                           quotaDefinitionUrl = orgs['entity']['quota_definition_url'])
            orgDetails.append(
                                {
                                    "org-name" : orgs['entity']['name'],
                                    "quota-name" : quotaInfo['name'],
                                    "mem-usage" : float(orgMemUsage/1024),
                                    "mem-limit" : float(quotaInfo['memory_limit'])/1024
                                }
                            )

        if( pageCounter == response.json()['total_pages'] ) :
            bail = False
        pageCounter = pageCounter + 1
    
    return orgDetails


def getQuotas(header,apiUrl):
    response = requests.get(
                             apiUrl.format("/v2/quota_definitions"),
                             headers=header,
                             verify=False
                           )
    return (response.json()['resources'])

def getQuotaDefinition(header,quotaDefinitionUrl,apiUrl):
    response = requests.get(
                                 apiUrl.format(quotaDefinitionUrl),
                                 headers=header,
                                 verify=False
                )
    return (response.json()['entity'])