#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This script is Copyright (C) 2015 Tenable Network Security, Inc.

import connect
import glob
import os


def get_sc4(sc4, itemtype):

    try:

        alt = get_alt(itemtype)

        if alt == 'dashboards':
            alt2 = 'tabs'
        else:
            alt2 = alt

        url = sc4['url']
        token = sc4['token']
        cookie = str(sc4['sessionID'])
        result = connect.sc4_connect(itemtype,
                                     'init',
                                     url=url,
                                     token=token,
                                     cookie=cookie)
        if result is None:
                print "There are no SC4 %s for this server instance" % alt
                return None
        print "\n\t {ID, Name, Description}"
        for v in result[alt2]:
            print "\t {"+str(v['id'])+","+str(v['name'])+","+str(v['description'])+"}"
        return result
    except Exception, e:
        print "\nError: " + str(e)
        return


def get_sc5(sc5, itemtype):

    try:

        alt = get_alt(itemtype)

        result = sc5.get('/'+itemtype)
        if result is None:
                print "There are no SC5 %s for this server instance" % alt
        print "\n\t {ID, Name, Description}"
        for v in result.json().get('response').get('manageable'):
            print "\t {"+v.get('id')+","+v.get('name')+","+v.get('description')+"}"
        return result
    except Exception, e:
        print "\nError: " + str(e)
        return


def export_sc4(sc4, itemtype, all=None):

    try:

        alt = get_alt(itemtype)
        url = sc4['url']
        token = sc4['token']
        cookie = str(sc4['sessionID'])
        if not os.path.exists('sc4/'+alt):
            os.makedirs('sc4/'+alt)
        response = connect.sc4_connect(itemtype,
                                       'init',
                                       url=url,
                                       token=token,
                                       cookie=cookie)
        if all is True:
            sc4Exportid = 'all'
        else:
            sc4Exportid = raw_input("\nPlease enter the ID of the %s you wish to export "
                                    "(type \"all\" to export all): " % itemtype)
        if alt == 'dashboards':
            alt2 = 'tabs'
        else:
            alt2 = alt
        if sc4Exportid == 'all':
            for v in response[alt2]:
                input = {'id': v['id']}
                print "Exporting %s %s" % (itemtype, v['id'])
                if itemtype == 'dashboard':
                    input = {'id': v['id'], 'exportType': 'full'}
                    action = 'exportTab'
                elif itemtype == 'policy':
                    action = 'exportNessusPolicy'
                data = connect.sc4_connect(itemtype,
                                           action,
                                           input,
                                           url=url,
                                           token=token,
                                           cookie=cookie)
                with open('sc4/'+alt+'/'+v['id']+'.xml', 'w') as f:
                    f.write(data)
            return
        else:
            for v in response[alt2]:
                if v['id'] == sc4Exportid:
                    input = {'id': v['id']}
                    print "Exporting %s %s" % (itemtype, v['id'])
                    action = 'export'
                    if itemtype == 'dashboard':
                        input = {'id': v['id'], 'exportType': 'full'}
                        action = 'exportTab'
                    elif itemtype == 'policy':
                        action = 'exportNessusPolicy'
                    data = connect.sc4_connect(itemtype,
                                               action,
                                               input,
                                               url=url,
                                               token=token,
                                               cookie=cookie)
                    with open('sc4/'+alt+'/'+v['id']+'.xml', 'w')as f:
                        f.write(data)
            return
    except Exception, e:
        print "\nError: " + str(e)
        return


def export_sc5(sc5, itemtype, all=None):

    try:

        alt = get_alt(itemtype)

        if not os.path.exists('sc5/'+alt):
            os.makedirs('sc5/'+alt)
        if all is True:
            sc5Exportid = 'all'
        else:
            sc5Exportid = raw_input("\nPlease enter the ID of the %s you wish to export"
                                    " (type \"all\" to export all): ") % itemtype
        if sc5Exportid == 'all':
            assets = sc5.get('/'+itemtype)
            for v in assets.json().get('response').get('manageable'):
                print "Exporting %s %s" % (itemtype, v.get('id'))
                if itemtype == 'reportDefinition' or itemtype == 'dashboard':
                    sc5Export = sc5.post(itemtype+'/'+v.get('id')+'/export', json={'exportType': 'full'})
                else:
                    sc5Export = sc5.get(itemtype+'/'+v.get('id')+'/export')
                with open('sc5/'+alt+'/'+v.get('id')+'.xml', 'w') as f:
                    f.write(sc5Export.content)
            return
        else:
            print "Exporting %s %s" % (itemtype, sc5Exportid)
            if itemtype == 'reportDefinition' or itemtype == 'dashboard':
                sc5Export = sc5.post(itemtype+'/'+v.get('id')+'/export', json={'exportType': 'full'})
            else:
                sc5Export = sc5.get(itemtype+'/'+sc5Exportid+'/export')
            with open('sc5/'+alt+'/'+sc5Exportid+'.xml', 'w') as f:
                f.write(sc5Export.content)
            return
    except Exception, e:
        print "\nError: " + str(e)
        return


def import_sc4(sc4, itemtype, all=None):

    try:
        
        alt = get_alt(itemtype)

        if not os.path.exists('sc4/'+alt):
            if not os.path.exists('sc5/'+alt):
                print "There are no %s to import" % itemtype
        url = sc4['url']
        token = sc4['token']
        cookie = str(sc4['sessionID'])
        if all is True:
            sc4Import = 'all'
        else:
            sc4Import = raw_input("\nPlease enter the ID and version of the %s you wish to import, "
                                  "type \"all\" to import all (Example: sc4/1 or sc5/2): ") % type
        print ""
        if sc4Import == 'all':
            files = glob.glob('sc4/'+alt+'/*.xml')
            files = files + glob.glob('sc5/'+alt+'/*.xml')
            for v in files:
                print "Importing "+v
                with open(v, 'rb') as in_file:
                    file_content = in_file.read()
                content = connect.sc4_connect('file',
                                              'upload',
                                              url=url,
                                              token=token,
                                              cookie=cookie,
                                              filename=v,
                                              filecontent=file_content)
                action = 'import'
                if itemtype == 'dashboard':
                    action = 'importTab'
                elif itemtype == 'policy':
                    action = 'importNessusPolicy'
                connect.sc4_connect(itemtype,
                                    action,
                                    input={'filename': content},
                                    url=url,
                                    token=token,
                                    cookie=cookie)
            return
        else:
            sc4Import = sc4Import.split('\\')
            file_name = sc4Import[0]+'/'+alt+'/'+sc4Import[1]+'.xml'
            print "\nImporting "+file_name
            with open(file_name, 'rb') as in_file:
                file_content = in_file.read()
            content = connect.sc4_connect('file',
                                          'upload',
                                          url=url,
                                          token=token,
                                          cookie=cookie,
                                          filename=file_name,
                                          filecontent=file_content)
            action = 'import'
            if itemtype == 'dashboard':
                action = 'importTab'
            elif itemtype == 'policy':
                action = 'importNessusPolicy'
            connect.sc4_connect(itemtype,
                                action,
                                input={'filename': content},
                                url=url,
                                token=token,
                                cookie=cookie)
        return
    except Exception, e:
        print "\nError: " + str(e)
        return


def import_sc5(sc5, itemtype, all=None):

    try:
        
        alt = get_alt(itemtype)
        
        if not os.path.exists('sc4/'+alt):
            if not os.path.exists('sc5/'+alt):
                print "There are no assets to import"
        if all is True:
            sc5Import = 'all'
        else:
            sc5Import = raw_input("\nPlease enter the ID and version of the %s you wish to import, "
                                  "type \"all\" to import all (Example: sc4/1 or sc5/2): " % itemtype)
        print ""
        if sc5Import == 'all':
            files = glob.glob('sc4/'+alt+'/*.xml')
            files = files + glob.glob('sc5/'+alt+'/*.xml')
            for v in files:
                print "Importing "+v
                with open(v, 'rb') as in_file:
                    file_content = in_file.read()
                files = {'Filedata': (v, file_content)}
                fupload = sc5.post('file/upload', files=files)
                name = fupload.json()['response']['filename']
                try:
                    if itemtype == 'dashboard':
                        sc5.post(itemtype+'/import', json={'filename': name, 'order': '1'})
                    else:
                        sc5.post(itemtype+'/import', json={'filename': name})
                except Exception, e:
                    print "\nError: " + str(e)
            return
        else:
            sc5Import = sc5Import.split('/')
            file_name = sc5Import[0]+'/'+alt+'/'+sc5Import[1]+'.xml'
            print "\nImporting "+file_name
            with open(file_name, 'rb') as in_file:
                file_content = in_file.read()
            files = {'Filedata': (file_name, file_content)}
            fupload = sc5.post('file/upload', files=files)
            name = fupload.json()['response']['filename']
            sc5.post(itemtype+'/import', json={"filename": name})
            return
    except Exception, e:
        print "\nError: " + str(e)
        return


def get_alt(itemtype):
    if itemtype == 'asset':
        alt = 'assets'
    elif itemtype == 'policy':
        alt = 'policies'
    elif itemtype == 'reportDefinition' or itemtype == 'report':
        alt = 'reports'
    elif itemtype == 'dashboard':
        alt = 'dashboards'
    else:
        print "improper type"
        return
    return alt
