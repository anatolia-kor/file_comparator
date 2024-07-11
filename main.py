import pandas as pd
import gspread
import pathlib
from oauth2client.service_account import ServiceAccountCredentials


class Google(object):

    def __init__(self):
        self.cl = None

    def authorizing(self):
        scope = [r'https://spreadsheets.google.com/feeds',
                 r'https://www.googleapis.com/auth/spreadsheets',
                 r'https://www.googleapis.com/auth/drive.file',
                 r'https://www.googleapis.com/auth/drive']
        dir_path = pathlib.Path.cwd()
        json_path = pathlib.Path(dir_path, 'google_logging', 'my-finance-402205-9313c07a7fb8.json')
        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
        self.cl = gspread.authorize(credentials)

    def get_transactions_as_df(self):
        spreadsheet_name, wsheet_name = 'Crypto', 'Транзакции'
        spreadsheet = self.cl.open(spreadsheet_name)
        existing_wsheets = [x.title for x in spreadsheet.worksheets()]
        if wsheet_name in existing_wsheets:
            wsheet = spreadsheet.worksheet(wsheet_name)
        else:
            raise Exception
        all_values = wsheet.get_all_values()[3:]
        whole_sheet_pd = pd.DataFrame.from_records(all_values[2:], columns=['1', '2', 'count_in',
                                                                            '3', 'ticker_in', '4',
                                                                            'count_out', '5', 'ticker_out',
                                                                            '6', '7', '8', '9', '10', '11',
                                                                            '12', '13', '14', '15', '16'])
        not_formated_pd = whole_sheet_pd.drop(columns=[str(i+1) for i in range(16)])
        not_formated_pd.loc[not_formated_pd['count_in']].map(self.to_float_func)

    @staticmethod
    def to_float_func(x):
        return float(x.replace(',', '.') if type(x) is str else 0 if x == 'None' else x)






def main():
    goo = Google()
    goo.authorizing()
    goo.get_transactions_as_df()
    a=4


if __name__ == '__main__':
    main()
