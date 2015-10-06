__author__ = 'mweinberger'


def sc4_connect(module, action, input={}, url='', token='', cookie='', filename='', filecontent=''):

    import requests
    requests.packages.urllib3.disable_warnings()
    data = {'module': module,
            'action': action,
            'input': json.dumps(input),
            'token': token,
            'request_id': 1}
    headers = {'Cookie': 'TNS_SESSIONID='+cookie}
    try:
        if action == 'upload':
            content = requests.post(url,
                                    params=data,
                                    files={'Filedata': (filename, filecontent)},
                                    verify=False,
                                    headers=headers,
                                    timeout=3)
            return content.json()['response']['filename']
        else:
            response = requests.post(url,
                                     params=data,
                                     verify=False,
                                     headers=headers,
                                     timeout=3)
            if str(action) == "export":
                return response.content
            if str(response.json()['error_code']) is not "0":
                print '\n'+response.json()['error_msg']+'Not logged in to SC4'
                return None
            return response.json()['response']
    except Exception, e:
        print "\nError: " + str(e)
        return None


def login_sc4():

    import getpass
    try:
        scInstance = raw_input("\nPlease enter the IP of your SecurityCenter 4.x instance: ")
        sc4User = raw_input("Please enter the SecurityCenter 4.x username: ")
        sc4Pass = getpass.getpass("Please enter the SecurityCenter 4.x password: ")
        input = {'username': sc4User, 'password': sc4Pass}
        url = 'https://'+scInstance+'/request.php'
        sc4 = sc4_connect('auth',
                          'login',
                          input,
                          url)
        return sc4, sc4User, url
    except Exception, e:
        print "\nError: " + str(e)
        return None


def login_sc5():

    import securitycenter
    try:
        scInstance = raw_input("\nPlease enter the IP of your Security Center instance: ")
        sc5 = securitycenter.SecurityCenter5(scInstance)
    except Exception, e:
        print "\nError: " + str(e)
        print "SC instance not found"
        return None, None
    try:
        sc5User = raw_input("Please enter the SecurityCenter username: ")
        sc5Pass = getpass.getpass("Please enter the SecurityCenter password: ")
        sc5.login(sc5User, sc5Pass)
        return sc5, sc5User
    except Exception, e:
        print "\nError: " + str(e)
        print "Login credentials not valid"
        return None, None


def logout(sc4, sc5):
    try:
        sc4.logout()
    except AttributeError:
        None
    try:
        sc5.logout()
    except AttributeError:
        None
    return

