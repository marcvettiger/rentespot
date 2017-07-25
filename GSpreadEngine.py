import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GSpreadEngine:

    scope = ['https://spreadsheets.google.com/feeds']
    sheets = {}

    def __init__(self):
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name('resources/client_secret.json', self.scope)
        self.client = gspread.authorize(self.credentials)

    def create_sheet(self, sheet_name):
        new_sheet = self.client.create(sheet_name)
        new_sheet.share("marc.vettiger@gmail.com", perm_type='user', role='writer')
        self.sheets[sheet_name] = new_sheet
        return True

    def get_sheet(self, sheet_name='Rente Point DataBase'):
        return self.client.open(sheet_name).sheet1

    def write_range(self, sheet_name, sheet_data):
        logging.info("Opening Google Spread sheet: %s " % sheet_name)
        sheet = self.client.open(sheet_name).sheet1

        logging.info("resize sheet to fit the data")
        # sheet_data  is a list of lists representing a matrix of data, headers being the first row.
        # first make sure the worksheet is the right size
        sheet.resize(len(sheet_data), len(sheet_data[0]))
        cell_matrix = []
        row_number = 1

        logging.info("Preparing the data to align with selected cell range")
        for row in sheet_data:
            # max 24 table width, otherwise a two character selection should be used, I didn't need this.
            cell_range = 'A{row}:{letter}{row}'.format(row=row_number, letter=chr(len(row) + ord('a') - 1))
            # get the row from the worksheet
            #TODO: This is too damn slow!!
            cell_list = sheet.range(cell_range)
            column_number = 0
            for cell in row:
                cell_list[column_number].value = row[column_number]
                column_number += 1

            # add the cell_list, which represents all cells in a row to the full matrix
            cell_matrix = cell_matrix + cell_list
            row_number += 1
            # output the full matrix all at once to the worksheet.
        logging.info("Writing cell matrix to Google spread sheet")
        sheet.update_cells(cell_matrix)
        logging.info("Writing cell matrix to Google spread sheet - done")

#
## Some test functions


def test_write_range():
    test_data = [['first', 'second', 'third'],
                 ['erste', 'zweite','dritte'],
                 ]
    gspread_engine = GSpreadEngine()
    gspread_engine.write_range('Rente Point DataBase', test_data)

def test_create_sheet():

    new_sheet_name = "newSheetTest"
    gspread_engine = GSpreadEngine()
    naa = gspread_engine.create_sheet(new_sheet_name)

    if naa is True:
        print('worked')
    else:
        print('Didnt work')








if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(module)s - %(funcName)s(): %(message)s',
                        filename='log/main.log',
                        filemode='w')
    #test_write_range()
    #test_create_sheet()

