import logging
import logging.config
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas

logging.config.fileConfig('cfg/logger.conf')
logger = logging.getLogger()


SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name('resources/client_secret.json', SCOPE)


def new(spreadsheet_name):
    client = gspread.authorize(CREDENTIALS)
    spread = client.create(spreadsheet_name)
    spread.sheet1.resize(1, 1)
    spread.share("marc.vettiger@gmail.com", perm_type='user', role='writer')
    spread.share("sandro.jeanmairet@gmail.com", perm_type='user', role='writer')
    return spread


def append(spreadsheet_name, sheet_data):
    client = gspread.authorize(CREDENTIALS)
    #TODO: Improve this against exception Unauthorized
    worksheet = client.open(spreadsheet_name).sheet1

    logger.info("Appending data to spreadsheet: %s ", spreadsheet_name)
    row_count = worksheet.row_count
    logger.debug("Row count of sheet: %s " % row_count)

    row_start = 1 + row_count
    row_len = len(sheet_data)
    row_end = row_start + row_len - 1

    col_start = 1
    col_len = len(sheet_data[0])
    col_end = col_start + col_len - 1
    col_end_letter = chr(col_end + ord('a') - 1).upper()

    logger.debug("Row start: %s" % row_start)
    logger.debug("Row len: %s" % row_len)
    logger.debug("Row end: %s" % row_end)

    logger.debug("Col start: %s" % row_start)
    logger.debug("Col len: %s" % col_len)
    logger.debug("Col end: %s" % col_end)
    logger.debug("Col end letter %s" % col_end_letter)

    cell_range = 'A{row_start}:{letter}{row_end}'.format(row_start=row_start, letter=col_end_letter, row_end=row_end)
    logger.debug("Cell range: %s ", cell_range)

    logger.debug("Resize worksheet to size %s by %s " % (row_end, col_end))
    worksheet.resize(row_end, col_end)

    cell_list = worksheet.range(cell_range)

    # Flatten our data
    zdata = [x
             for row in sheet_data
             for x in row]

    # Fill the cells with data
    for value, cell in zip(zdata, cell_list):
        cell.value = value

    # Upload it
    worksheet.update_cells(cell_list)
    logger.info("Appending data to spreadsheet - done")



def get_data_set_from_spreadDB(spreadsheet_name):
    client = gspread.authorize(CREDENTIALS)
    #TODO: Improve this against exception Unauthorized
    worksheet = client.open(spreadsheet_name).sheet1
    logger.info("Downloading data from spreadsheet DB")
    db_list = worksheet.get_all_values()

    # TODO: Google Spreadsheet returns just 'String' type data, so we have to cast it here.
    # Should be replaced by database handler later
    for i in db_list:
        i[0] = int(i[0]) if i[0] != '' else None
        i[2] = float(i[2]) if i[2] != '' else None

    data_set = db_list
    return data_set







##
#
# Test function
#
##

def runappend():
    logger.info("Testing append function")
    test_data = [
        ['first', 'second', 'third','xabc', 'xdef', 'xghi'],
        ['erste', 'zweite','dritte','xabc', 'xdef', 'xghi'],
        ['abc', 'def', 'ghi','xabc', 'xdef', 'xghi'],
        ['jkl', 'mno', 'pqr','xabc', 'xdef', 'xghi'],
        ['xxx', 'yyy', 'zzz','xabc', 'xdef', 'xghi'],
    ]

    append('TestSheet', test_data)




if __name__ == '__main__':
    runappend()
