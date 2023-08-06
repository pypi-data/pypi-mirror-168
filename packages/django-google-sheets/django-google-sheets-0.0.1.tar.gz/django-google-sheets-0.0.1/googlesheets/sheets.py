import gspread
from django.conf import settings
import os


class Sheets:
    def __init__(self):
        url = f'{settings.BASE_DIR}/service_account.json'
        gc = gspread.service_account(url)
        self.sh = gc.open_by_key(settings.SHEETS_KEY)
        self.worksheet = self.sh.worksheet(settings.SHEETS_WORK)
        self.SHEETS_WORK = settings.SHEETS_WORK

    def ler(self,range=None,worksheet=None):
        if worksheet == None:
            return self.worksheet.get_all_values()
        else:
            worksheet = self.sh.worksheet(worksheet)
            return worksheet.get_all_values()

    def adicionar(self,add,worksheet=None):
        if worksheet == None:
            self.sh.values_append(f'{self.SHEETS_WORK}!A1', params={'valueInputOption': 'RAW'}, body={'values': [add]})
        else:
            self.sh.values_append(f'{worksheet}!A1', params={'valueInputOption': 'RAW'}, body={'values': [add]})
            return self.ler(worksheet=worksheet)
        return self.ler()

    def updata(self,add,antigo,worksheet=None):
        x = 1
        y = None
        if worksheet == None:
            pks = self.worksheet.col_values(1)
        else:
            worksheet = self.sh.worksheet(worksheet)
            pks = worksheet.col_values(1)
        for i in pks:
            if int(i) == int(antigo):
                y = x
            x += 1
        if y == None:
            self.adicionar(add,worksheet)
            return False
        else:
            self.worksheet.update(f'A{y}', [add])
            return True

    def delete(self,antigo,worksheet=None):
        x = 1
        y = None
        if worksheet == None:
            pks = self.worksheet.col_values(1)
        else:
            worksheet = self.sh.worksheet(worksheet)
            pks = worksheet.col_values(1)
        for i in pks:
            if int(i) == int(antigo):
                y = x
            x += 1
        if y == None:
            return False
        else:
            self.worksheet.delete_row(y)
            return True

google_sheets = Sheets()