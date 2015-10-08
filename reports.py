import connect


def get_reports_sc4(sc4):
    token = sc4['token']
    cookie = str(sc4['sessionID'])
    result = connect.sc4_connect('reports',
                                 'init',
                                 url=url,
                                 token=token,
                                 cookie=cookie)
    if result is None:
            print "There are no SC4 Assets for this server instance"
            return None
    print "\n\t {ID, Name, Description}"
    for v in result['assets']:
        print "\t {"+str(v['id'])+","+str(v['name'])+","+str(v['description'])+"}"
    return result


def get_reports_sc5(sc5):

    result = sc5.get('/asset')
    if result is None:
            print "There are no SC5 Assets for this server instance"
    print "\n\t {ID, Name, Description}"
    for v in result.json().get('response').get('manageable'):
        print "\t {"+v.get('id')+","+v.get('name')+","+v.get('description')+"}"
    return result


def export_reports_sc4(sc4):
    return


def export_reports_sc5(sc5):
    return


def import_reports_sc4(sc4):
    return


def import_reports_sc5(sc5):
    return
