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
                           "------Assets------"
                           "  2. List Assets \n"
                           "  3. Export Assets \n"
                           "  4. Import Assets \n"
                           "------Policies------"
                           "  5. List Policies \n"
                           "  6. Export Policies \n"
                           "  7. Import Policies \n"
                           "------Reports------"
                           "  8. List Reports \n"
                           "  9. Export Reports \n"
                           "  10. Import Reports \n"
                           "------Dashboards------"
                           "  11. List Dashboards \n"
                           "  12. Export Dashboards \n"
                           "  13. Import Dashboards \n")
        if switch == "1":
            return
        elif switch == "2":
            assets.get_assets_sc4(sc4)
        elif switch == "3":
            assets.export_assets_sc4(sc4)
        elif switch == "4":
            assets.import_assets_sc4(sc4)
        elif switch == "5":
            policies.get_policies_sc4(sc4)
        elif switch == "6":
            policies.export_policies_sc4(sc4)
        elif switch == "7":
            policies.import_policies_sc4(sc4)
        elif switch == "8":
            reports.get_reports_sc4(sc4)
        elif switch == "9":
            reports.export_reports_sc4(sc4)
        elif switch == "10":
            reports.import_reports_sc4(sc4)
        elif switch == "11":
            dashboards.get_dashboards_sc4(sc4)
        elif switch == "12":
            dashboards.export_dashboards_sc4(sc4)
        elif switch == "13":
            dashboards.import_dashboards_sc4(sc4)


def sc5_menus(sc5):

    while True:
        switch = raw_input("\nAvailable SC5 Menu Options: \n1. Back to Main Menu \n"
                           "------Assets------"
                           "  2. List Assets \n"
                           "  3. Export Assets \n"
                           "  4. Import Assets \n"
                           "------Policies------"
                           "  5. List Policies \n"
                           "  6. Export Policies \n"
                           "  7. Import Policies \n"
                           "------Reports------"
                           "  8. List Reports \n"
                           "  9. Export Reports \n"
                           "  10. Import Reports \n"
                           "------Dashboards------"
                           "  11. List Dashboards \n"
                           "  12. Export Dashboards \n"
                           "  13. Import Dashboards \n")
        if switch == "1":
            return
        elif switch == "2":
            assets.get_assets_sc5(sc5)
        elif switch == "3":
            assets.export_assets_sc5(sc5)
        elif switch == "4":
            assets.import_assets_sc5(sc5)
        elif switch == "5":
            policies.get_policies_sc5(sc5)
        elif switch == "6":
            policies.export_policies_sc5(sc5)
        elif switch == "7":
            policies.import_policies_sc5(sc5)
        elif switch == "8":
            reports.get_reports_sc5(sc5)
        elif switch == "9":
            reports.export_reports_sc5(sc5)
        elif switch == "10":
            reports.import_reports_sc5(sc5)
        elif switch == "11":
            dashboards.get_dashboards_sc5(sc5)
        elif switch == "12":
            dashboards.export_dashboards_sc5(sc5)
        elif switch == "13":
            dashboards.import_dashboards_sc5(sc5)


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
            sc4_menus(sc4)
        elif switch == "4":
            sc5_menus(sc5)
        elif switch == "5":
            print "Exiting..."
            break

connect.logout()
exit()
