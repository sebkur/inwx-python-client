#!/usr/bin/python3

from INWX.Domrobot import ApiClient

username = 'USERNAME'
password = 'PASSWORD'
domain = 'enter-your-domain.com'

api_client = ApiClient(api_url=ApiClient.API_LIVE_URL, debug_mode=True)

login_result = api_client.login(username, password)

if login_result['code'] == 1000:
    # check if domain is available
    domain_check_result = api_client.call_api(api_method='domain.check', method_params={'domain': domain})

    if domain_check_result['code'] == 1000:
        checked_domain = domain_check_result['resData']['domain'][0]

        if checked_domain['avail']:
            print(domain + ' is still available!')
        else:
            print('Unfortunately, ' + domain + ' is already registered.')

    else:
        raise Exception('Api error while checking domain status. Code: ' + str(domain_check_result['code'])
                        + '  Message: ' + domain_check_result['msg'])

    # try to add a record
    add_result = api_client.call_api(api_method='nameserver.createRecord', method_params={'domain': domain, 'type': 'TXT', 'content': 'foo'})
    if add_result['code'] == 1000:
        print("added record successfully")
    else:
        print("adding record failed")

    # log out
    api_client.logout()
else:
    raise Exception('Api login error. Code: ' + str(login_result['code']) + '  Message: ' + login_result['msg'])
