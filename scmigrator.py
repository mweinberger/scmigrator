#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This script is Copyright (C) 2015 Tenable Network Security, Inc.

from extra import *


def check_version():

    import securitycenter
    version = securitycenter.__version__.split(".")
    if version[0] > 2:
        return
    elif version[0] == 2:
        if version[1] > 1:
            return
        elif version[1] == 1:
            if version[2] >= 7:
                return

    print "This script requires pySecurityCenter 2.1.7 or above"
    exit()


def sc4_menus(sc4):

    while True:
        switch = raw_input("\nAvailable SC4 Menu Options: \n1. Back to Main Menu \n"
                           "------Assets------ \n"
                           "  2. List Assets \n"
                           "  3. Export Assets \n"
                           "  4. Import Assets \n"
                           "------Policies------ \n"
                           "  5. List Policies \n"
                           "  6. Export Policies \n"
                           "  7. Import Policies \n"
                           "------Reports------ \n"
                           "  8. List Reports \n"
                           "  9. Export Reports \n"
                           "  10. Import Reports \n"
                           "------Dashboards------ \n"
                           "  11. List Dashboards \n"
                           "  12. Export Dashboards \n"
                           "  13. Import Dashboards \n"
                           "------Special------ \n"
                           "  14. Export EVERYTHING \n"
                           "  15. Import EVERYTHING \n"
                           ":")
        if switch == "1":
            return
        elif switch == "2":
            items.get_sc4(sc4, 'asset')
        elif switch == "3":
            items.export_sc4(sc4, 'asset')
        elif switch == "4":
            items.import_sc4(sc4, 'asset')
        elif switch == "5":
            items.get_scsc4(sc4, 'policy')
        elif switch == "6":
            items.export_sc4(sc4, 'policy')
        elif switch == "7":
            items.import_sc4(sc4, 'policy')
        elif switch == "8":
            items.get_sc4(sc4, 'report')
        elif switch == "9":
            items.export_sc4(sc4, 'report')
        elif switch == "10":
            items.import_sc4(sc4, 'report')
        elif switch == "11":
            items.get_sc4(sc4, 'dashboard')
        elif switch == "12":
            items.export_sc4(sc4, 'dashboard')
        elif switch == "13":
            items.import_sc4(sc4, 'dashboard')
        elif switch == "14":
            items.export_sc4(sc4, 'asset', all=True)
            items.export_sc4(sc4, 'policy', all=True)
            items.export_sc4(sc4, 'report', all=True)
            items.export_sc4(sc4, 'dashboard', all=True)
        elif switch == "15":
            items.import_sc4(sc4, 'asset', all=True)
            items.import_sc4(sc4, 'policy', all=True)
            items.import_sc4(sc4, 'report', all=True)
            items.import_sc4(sc4, 'dashboard', all=True)


def sc5_menus(sc5):

    while True:
        switch = raw_input("\nAvailable SC5 Menu Options: \n1. Back to Main Menu \n"
                           "------Assets------ \n"
                           "  2. List Assets \n"
                           "  3. Export Assets \n"
                           "  4. Import Assets \n"
                           "------Policies------ \n"
                           "  5. List Policies \n"
                           "  6. Export Policies \n"
                           "  7. Import Policies \n"
                           "------Reports------ \n"
                           "  8. List Reports \n"
                           "  9. Export Reports \n"
                           "  10. Import Reports \n"
                           "------Dashboards------ \n"
                           "  11. List Dashboards \n"
                           "  12. Export Dashboards \n"
                           "  13. Import Dashboards \n"
                           "------Special------ \n"
                           "  14. Export EVERYTHING \n"
                           "  15. Import EVERYTHING \n"
                           ":")
        if switch == "1":
            return
        elif switch == "2":
            items.get_sc5(sc5, 'asset')
        elif switch == "3":
            items.export_sc5(sc5, 'asset')
        elif switch == "4":
            items.import_sc5(sc5, 'asset')
        elif switch == "5":
            items.get_sc5(sc5, 'policy')
        elif switch == "6":
            items.export_sc5(sc5, 'policy')
        elif switch == "7":
            items.import_sc5(sc5, 'policy')
        elif switch == "8":
            items.get_sc5(sc5, 'reportDefinition')
        elif switch == "9":
            items.export_sc5(sc5, 'reportDefinition')
        elif switch == "10":
            items.import_sc5(sc5, 'reportDefinition')
        elif switch == "11":
            items.get_sc5(sc5, 'dashboard')
        elif switch == "12":
            items.export_sc5(sc5, 'dashboard')
        elif switch == "13":
            items.import_sc5(sc5, 'dashboard')
        elif switch == "14":
            items.export_sc5(sc5, 'asset', all=True)
            items.export_sc5(sc5, 'policy', all=True)
            items.export_sc5(sc5, 'reportDefinition', all=True)
            items.export_sc5(sc5, 'dashboard', all=True)
        elif switch == "15":
            items.import_sc5(sc5, 'asset', all=True)
            items.import_sc5(sc5, 'policy', all=True)
            items.import_sc5(sc5, 'reportDefinition', all=True)
            items.import_sc5(sc5, 'dashboard', all=True)


# ------------------------------------------------------------------------------
# Main Program
# ------------------------------------------------------------------------------

sc4 = None
sc5 = None
sc4User = ""
sc5User = ""

print "\n\nWelcome to the SecurityCenter Asset Migrator \n"\
      "This program will allow you to import and export assets from SC4 and SC5\n"\
      "A few things are of note:\n"\
      "1. SecurityCenter 5 does not allow you to import two assets with the same name.  "\
      "If you want to do this anyway change the name in your local .xml file.\n"\
      "2. Selecting \"all\" for either sc4 or sc5 imports will upload all .xml files in your local directory.  "\
      "It will however stop on failues, you may want to move or remove the files that have already finished importing "\
      "before continuing the import.\n"\
      "3. To export or import between two SC instances of the same version, simply log in to the first one and "\
      "export followed by logging in to the second one and importing."
print "Please report any bugs or odd behavior to Michael Weinberger (mweinberger@tenable.com)\n"

check_version()

while True:

    if sc4 is None and sc5 is None:
        switch = raw_input("\nAvaliable Menu Options: \n1. Log in to SC4 \n2. Log in to SC5 \n3. Exit \n: ")
        if switch == "1":
            sc4, sc4User, url = connect.login_sc4()
        elif switch == "2":
            sc5, sc5User = connect.login_sc5()
        elif switch == "3":
            print "Exiting..."
            break
    elif sc4 is None:
        switch = raw_input("\nAvaliable Menu Options: \n1. Log in to SC4 \n"
                           "2. Log in to other SC5 (Currently logged in as "+sc5User+")\n"
                           "3. SC5 Options \n"
                           "4. Exit \n: ")
        if switch == "1":
            sc4, sc4User, url = connect.login_sc4()
        elif switch == "2":
            sc5, sc5User = connect.login_sc5()
        elif switch == "3":
            sc5_menus(sc5)
        elif switch == "4":
            print "Exiting..."
            break

    elif sc5 is None:
        switch = raw_input("\nAvaliable Menu Options: \n1. Log in to other SC4 (Currently logged in as "+sc4User+")\n"
                           "2. Log in to SC5 \n"
                           "3. SC4 Options \n"
                           "4. Exit \n: ")
        if switch == "1":
            sc4, sc4User, url = connect.login_sc4()
        elif switch == "2":
            sc5, sc5User = connect.login_sc5()
        elif switch == "3":
            sc4['url'] = url
            sc4_menus(sc4)
        elif switch == "4":
            print "Exiting..."
            break
    else:
        switch = raw_input("\nAvaliable Menu Options: \n1. Log in to other SC4 (Currently logged in as "+sc4User+")\n"
                           "2. Log in to other SC5 (Currently logged in as "+sc5User+")\n"
                           "3. SC4 Options \n"
                           "4. SC5 Options \n"
                           "5. Exit \n: ")
        if switch == "1":
            sc4, sc4User, url = connect.login_sc4()
        elif switch == "2":
            sc5, sc5User = connect.login_sc5()
        elif switch == "3":
            sc4['url'] = url
            sc4_menus(sc4)
        elif switch == "4":
            sc5_menus(sc5)
        elif switch == "5":
            print "Exiting..."
            break

connect.logout(sc4, sc5)
exit()
