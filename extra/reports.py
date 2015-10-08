#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This script is Copyright (C) 2015 Tenable Network Security, Inc.

import connect
import glob


def get_reports_sc4(sc4):

    try:
        url = sc4['url']
        token = sc4['token']
        cookie = str(sc4['sessionID'])
        result = connect.sc4_connect('report',
                                     'init',
                                     url=url,
                                     token=token,
                                     cookie=cookie)
        if result is None:
                print "There are no SC4 reports for this server instance"
                return None
        print "\n\t {ID, Name, Description}"
        for v in result['reports']:
            print "\t {"+str(v['id'])+","+str(v['name'])+","+str(v['description'])+"}"
        return result
    except Exception, e:
        print "\nError: " + str(e)
        return


def get_reports_sc5(sc5):

    try:
        result = sc5.get('/report')
        if result is None:
                print "There are no SC5 reports for this server instance"
        print "\n\t {ID, Name, Description}"
        for v in result.json().get('response').get('manageable'):
            print "\t {"+v.get('id')+","+v.get('name')+","+v.get('description')+"}"
        return result
    except Exception, e:
        print "\nError: " + str(e)
        return


def export_reports_sc4(sc4, all=None):

    try:
        token = sc4['token']
        cookie = str(sc4['sessionID'])
        if not os.path.exists('sc4/reports'):
            os.makedirs('sc4/reports')
        reports = connect.sc4_connect('report',
                                     'init',
                                     url=url,
                                     token=token,
                                     cookie=cookie)
        if all is True:
            sc4Exportid = "all"
        else:
            sc4Exportid = raw_input("\nPlease enter the ID of the report you wish to export"
                                    " (type \"all\" to export all): ")
        if sc4Exportid == "all":
            for v in reports['reports']:
                input = {'id': v['id']}
                data = connect.sc4_connect('report',
                                           'export',
                                           input,
                                           url=url,
                                           token=token,
                                           cookie=cookie)
                with open('sc4/reports/'+v['id']+".xml", 'w') as f:
                    f.write(data)
            return
        else:
            for v in reports['reports']:
                if v['id'] == sc4Exportid:
                    input = {'id': v['id']}
                    data = connect.sc4_connect('report',
                                               'export',
                                               input,
                                               url=url,
                                               token=token,
                                               cookie=cookie)
                    with open('sc4/reports/'+v['id']+".xml", 'w')as f:
                        f.write(data)
            return
    except Exception, e:
        print "\nError: " + str(e)
        return


def export_reports_sc5(sc5, all=None):

    try:
        if not os.path.exists('sc5/reports'):
            os.makedirs('sc5/reports')
        if all is True:
            sc5Exportid = "all"
        else:
            sc5Exportid = raw_input("\nPlease enter the ID of the report you wish to export"
                                    " (type \"all\" to export all): ")
        if sc5Exportid == "all":
            reports = sc5.get('/report')
            for v in reports.json().get('response').get('manageable'):
                sc5Export = sc5.get('report/'+v.get('id')+'/export')
                with open('sc5/reports/'+v.get('id')+".xml", 'w') as f:
                    f.write(sc5Export.content)
            return
        else:
            sc5Export = sc5.get('report/'+sc5Exportid+'/export')
            with open('sc5/reports/'+sc5Exportid+".xml", 'w') as f:
                f.write(sc5Export.content)
            return
    except Exception, e:
        print "\nError: " + str(e)
        return


def import_reports_sc4(sc4, all=None):

    try:
        if not os.path.exists('sc4/reports'):
            if not os.path.exists('sc5/reports'):
                print "There are no reports to import"
        token = sc4['token']
        cookie = str(sc4['sessionID'])
        if all is True:
            sc4Import = "all"
        else:
            sc4Import = raw_input("\nPlease enter the ID and version of the report you wish to import, "
                          "type \"all\" to import all (Example: sc4/1 or sc5/2): ")
        print ""
        if sc4Import == "all":
            reports = glob.glob("sc4/reports/*.xml")
            reports.append(glob.glob("sc5/reports/*.xml"))
            for v in reports:
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
                connect.sc4_connect('report',
                                    'import',
                                    input={'filename': content},
                                    url=url,
                                    token=token,
                                    cookie=cookie)
            return
        else:
            sc4Import = sc4Import.split("\\")
            file_name = sc4Import[0]+'/reports/'+sc4Import[1]+'.xml'
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
            connect.sc4_connect('report',
                                'import',
                                input={'filename': content},
                                url=url,
                                token=token,
                                cookie=cookie)
        return
    except Exception, e:
        print "\nError: " + str(e)
        return


def import_reports_sc5(sc5, all=None):

    try:
        if not os.path.exists('sc4/reports'):
            if not os.path.exists('sc5/reports'):
                print "There are no reports to import"
        if all is True:
            sc5Import = "all"
        else:
            sc5Import = raw_input("\nPlease enter the ID and version of the report you wish to import, "
                              "type \"all\" to import all (Example: sc4/1 or sc5/2): ")
        print ""
        if sc5Import == "all":
            reports = glob.glob("sc4/reports/*.xml")
            reports.append(glob.glob("sc5/reports/*.xml"))
            for v in reports:
                print "Importing "+v
                with open(v, 'rb') as in_file:
                    file_content = in_file.read()
                files = {'Filedata': (v, file_content)}
                fupload = sc5.post('file/upload', files=files)
                name = fupload.json()['response']['filename']
                sc5.post('report/import', json={"filename": name})
            return
        else:
            sc5Import = sc5Import.split("\\")
            file_name = sc5Import[0]+'/reports/'+sc5Import[1]+'.xml'
            print "\nImporting "+file_name
            with open(file_name, 'rb') as in_file:
                file_content = in_file.read()
            files = {'Filedata': (file_name, file_content)}
            fupload = sc5.post('file/upload', files=files)
            name = fupload.json()['response']['filename']
            sc5.post('report/import', json={"filename": name})
    except Exception, e:
        print "\nError: " + str(e)
        return
