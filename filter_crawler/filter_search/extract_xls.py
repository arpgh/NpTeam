import os
import sys

PROJECT_PATH = "/home/bumblebee/NepalTeam/filter_crawler"
sys.path.append(PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'filter_crawler.settings'

import xlrd
from filter_search.models import FilterSearch

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
xls_filename = "filter_search.xlsx"
file_path = ROOT_PATH + "/" + xls_filename

try:
    workbook = xlrd.open_workbook(file_path)
except IOError as e:
    print "Error occurred. Msg: ", repr(e)
    print "Exiting program !!!"
    sys.exit()

worksheet = workbook.sheet_by_name('Tree')

num_rows = worksheet.nrows
num_cols = worksheet.ncols

row_info = []
row_info_prev = []

for row_index in range(1, num_rows):
    row_info = worksheet.row(row_index)
    videos = worksheet.cell_value(row_index, num_cols-1)
    row_info[num_cols-1] = int(videos) if isinstance(videos, float) else None
    for col_index in range(num_cols-1):
        if not worksheet.cell_value(row_index, col_index):
            row_info[col_index] = row_info_prev[col_index]
        else:
            row_info[col_index] = worksheet.cell_value(row_index, col_index)
            for rest_col_index in range(col_index+1, num_cols-1):
                row_info[rest_col_index] = None
            row_info_prev = row_info
            break
    row_info_prev = row_info
    print row_info
    print "=================================="
    
    try:
        data = FilterSearch(level1=row_info[0], level2=row_info[1], level3=row_info[2], level4=row_info[3], level5=row_info[4], videos=row_info[5])
        data.save()
    except Exception as e:
        print "Error while inserting in db. Msg: ", repr(e)
print "data saved in db"


            
            
