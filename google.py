#!/usr/bin/env python3

import gspread
import common
import os
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE_NAME   = 'CS301-7e15aaa9056e.json'
SPREADSHEET_NAME        = 'DiscussionPosts'

# This function logs in to Google serives and gets the reference to
# the desired Google Spreadsheet.
def getSheet():
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(\
        CREDENTIALS_FILE_NAME, scope)
    gc = gspread.authorize(credentials)
    return gc.open(SPREADSHEET_NAME).sheet1

# This is called by the blackboard script to insert the student
# data for a particular entry
def insertData(total, item):
    wks = getSheet()
    day = wks.find(item)
    if not day:
        print("Could not find entry for " + item)
        return 1
    for key in total:
        per = wks.find(key)
        wks.update_cell(day.row, per.col, str(total[key][0]) + ":" +\
                str(total[key][1]))

# TODO: Total up the results for the spreadsheet
def totalData():
    pass

# This should be called when independently running
# to establish the layout of the sheet
# 
# On your Gdrive you should already have the spreadsheet
# made that this is accessing
#
# DON'T RUN THIS IF ALREADY USING SHEET
def initializeSheet():
    wks = getSheet()
    last = chr(len(common.STUDENTS)-1 + ord('B'))

    # Place the names in the correct cells
    name_range = wks.range('B1:'+last+'1')
    disc_range = wks.range('A2:A'+str(common.DISC_COUNT+1))
    for i, cell in enumerate(name_range):
        cell.value = common.STUDENTS[i]
    wks.update_cells(name_range)
    # TODO: Fix for new common.DISCUSSIONS setup
    values = list(common.DISCUSSIONS.keys())
    for i, cell in enumerate(disc_range):
        cell.value = values[i]
    wks.update_cells(disc_range)

if __name__ == '__main__':
    initializeSheet()
