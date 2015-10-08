#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This script is Copyright (C) 2015 Tenable Network Security, Inc.

import connect
import glob


def get_assets_sc4(sc4):

    token = sc4['token']
    cookie = str(sc4['sessionID'])
    result = connect.sc4_connect('asset',
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


def get_assets_sc5(sc5):

    result = sc5.get('/asset')
    if result is None:
            print "There are no SC5 Assets for this server instance"
    print "\n\t {ID, Name, Description}"
    for v in result.json().get('response').get('manageable'):
        print "\t {"+v.get('id')+","+v.get('name')+","+v.get('description')+"}"
    return result


def export_assets_sc4(sc4):

    token = sc4['token']
    cookie = str(sc4['sessionID'])
    assets = connect.sc4_connect('asset',
                                 'init',
                                 url=url,
                                 token=token,
                                 cookie=cookie)
    try:
        sc4Exportid = raw_input("\nPlease enter the ID of the asset you wish to export (type \"all\" to export all): ")
        if sc4Exportid == "all":
            for v in assets['assets']:
                input = {'id': v['id']}
                data = connect.sc4_connect('asset',
                                           'export',
                                           input,
                                           url=url,
                                           token=token,
                                           cookie=cookie)
                with open(v['id']+".sc4.xml", 'w') as f:
                    f.write(data)
            return
        else:
            for v in assets['assets']:
                if v['id'] == sc4Exportid:
                    input = {'id': v['id']}
                    data = connect.sc4_connect('asset',
                                               'export',
                                               input,
                                               url=url,
                                               token=token,
                                               cookie=cookie)
                    with open(v['id']+".sc4.xml", 'w')as f:
                        f.write(data)
            return
    except Exception, e:
        print "\nError: " + str(e)
        return


def export_assets_sc5(sc5):

    try:
        sc5Exportid = raw_input("\nPlease enter the ID of the asset you wish to export (type \"all\" to export all): ")
        if sc5Exportid == "all":
            assets = sc5.get('/asset')
            for v in assets.json().get('response').get('manageable'):
                sc5Export = sc5.get('asset/'+v.get('id')+'/export')
                with open(v.get('id')+".sc5.xml", 'w') as f:
                    f.write(sc5Export.content)
            return
        else:
            sc5Export = sc5.get('asset/'+sc5Exportid+'/export')
            with open(sc5Exportid+".sc5.xml", 'w') as f:
                f.write(sc5Export.content)
            return
    except Exception, e:
        print "\nError: " + str(e)
        return


def import_assets_sc4(sc4):

    token = sc4['token']
    cookie = str(sc4['sessionID'])
    sc4Import = raw_input("\nPlease enter the ID and version of the asset you wish to import, "
                          "type \"all\" to import all (Example: 1.sc4 or 2.sc5): ")
    print ""
    try:
        if sc4Import == "all":
            assets = glob.glob("*.xml")
            for v in assets:
                print "Importing"+v
                with open(v, 'rb') as in_file:
                    file_content = in_file.read()
                content = connect.sc4_connect('file',
                                              'upload',
                                              url=url,
                                              token=token,
                                              cookie=cookie,
                                              data=file_content)
                connect.sc4_connect('asset',
                                    'import',
                                    input={'filename': content},
                                    url=url,
                                    token=token,
                                    cookie=cookie)
            return
        else:
            file_name = sc4Import+'.xml'
            print "\nImporting"+file_name
            with open(file_name, 'rb') as in_file:
                file_content = in_file.read()
            content = connect.sc4_connect('file',
                                          'upload',
                                          url=url,
                                          token=token,
                                          cookie=cookie,
                                          filename=file_name,
                                          filecontent=file_content)
            connect.sc4_connect('asset',
                                'import',
                                input={'filename': content},
                                url=url,
                                token=token,
                                cookie=cookie)
        return
    except Exception, e:
        print "\nError: " + str(e)
        return


def import_assets_sc5(sc5):

    sc5Import = raw_input("\nPlease enter the ID and version of the asset you wish to import, "
                          "type \"all\" to import all (Example: 1.sc4 or 2.sc5): ")
    print ""
    if sc5Import == "all":
        assets = glob.glob("*.xml")
        for v in assets:
            print "Importing"+v
            try:
                with open(v, 'rb') as in_file:
                    file_content = in_file.read()
                files = {'Filedata': (v, file_content)}
                fupload = sc5.post('file/upload', files=files)
                name = fupload.json()['response']['filename']
                sc5.post('asset/import', json={"filename": name})
            except Exception, e:
                print "\nError: " + str(e)
        return
    else:
        try:
            file_name = sc5Import+'.xml'
            print "\nImporting"+file_name
            with open(file_name, 'rb') as in_file:
                file_content = in_file.read()
            files = {'Filedata': (file_name, file_content)}
            fupload = sc5.post('file/upload', files=files)
            name = fupload.json()['response']['filename']
            sc5.post('asset/import', json={"filename": name})
        except Exception, e:
            print "\nError: " + str(e)
        return