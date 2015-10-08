#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This script is Copyright (C) 2015 Tenable Network Security, Inc.

import connect
import glob

def get_policies_sc4(sc4):
    token = sc4['token']
    cookie = str(sc4['sessionID'])
    result = connect.sc4_connect('policy',
                                 'init',
                                 url=url,
                                 token=token,
                                 cookie=cookie)
    if result is None:
            print "There are no SC4 Policies for this server instance"
            return None
    print "\n\t {ID, Name, Description}"
    for v in result['policies']:
        print "\t {"+str(v['id'])+","+str(v['name'])+","+str(v['description'])+"}"
    return result


def get_policies_sc5(sc5):

    result = sc5.get('/policy')
    if result is None:
            print "There are no SC5 Policies for this server instance"
    print "\n\t {ID, Name, Description}"
    for v in result.json().get('response').get('manageable'):
        print "\t {"+v.get('id')+","+v.get('name')+","+v.get('description')+"}"
    return result


def export_policies_sc4(sc4):
    return


def export_policies_sc5(sc5):
    return


def import_policies_sc4(sc4):
    return


def import_policies_sc5(sc5):
    return

