import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GSpreadEngine:

    scope = ['https://spreadsheets.google.com/feeds']
    sheets = {}

    def __init__(self, spread_name):
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name('resources/client_secret.json', self.scope)
        self.client = gspread.authorize(self.credentials)
        self.spread_name = spread_name

    def create_sheet(self, new_sheet_name, new_rows=1, new_cols=16):
        spread = self.client.open(self.spread_name)
        spread.add_worksheet(title=new_sheet_name, rows=new_rows, cols=new_cols)

    def sheet_exists(self, sheet_name):
        pass

    def write_range(self, spread_name, sheet_name, sheet_data):
        logging.info("Opening Google Spread sheet: %s " % spread_name)
        #spread = self.client.open(spread_name)
        spread = self.client.open(spread_name).worksheet(sheet_name)

        logging.info("resize sheet to fit the data")
        # sheet_data  is a list of lists representing a matrix of data, headers being the first row.
        # first make sure the worksheet is the right size
        spread.resize(len(sheet_data), len(sheet_data[0]))
        cell_matrix = []
        row_number = 1

        logging.info("Preparing the data to align with selected cell range")
        for row in sheet_data:
            # max 24 table width, otherwise a two character selection should be used, I didn't need this.
            cell_range = 'A{row}:{letter}{row}'.format(row=row_number, letter=chr(len(row) + ord('a') - 1))
            # get the row from the worksheet
            #TODO: This is too damn slow!!
            cell_list = spread.range(cell_range)
            column_number = 0
            for cell in row:
                cell_list[column_number].value = row[column_number]
                column_number += 1

            # add the cell_list, which represents all cells in a row to the full matrix
            cell_matrix = cell_matrix + cell_list
            row_number += 1
            # output the full matrix all at once to the worksheet.
        logging.info("Writing cell matrix to Google spread sheet")
        spread.update_cells(cell_matrix)
        logging.info("Writing cell matrix to Google spread sheet - done")

#
## Some test functions


def test_write_range():
    test_data = [['first', 'second', 'third'],
                 ['erste', 'zweite','dritte'],
                 ]
    gspread_engine = GSpreadEngine('Rentepoint Spread')
    gspread_engine.create_sheet('Bitchtest')
    gspread_engine.write_range('Rentepoint Spread', 'Bitchtest', test_data)


def test_create_sheet():
    spread_name = "Rentepoint Spread"
    new_sheet_name = 'Blalalalalal'
    gspread_engine = GSpreadEngine('Rentepoint Spread')
    gspread_engine.create_sheet(new_sheet_name,)




if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(module)s - %(funcName)s(): %(message)s',
                        filename='log/main.log',
                        filemode='w')
    test_write_range()
    #test_create_sheet()

