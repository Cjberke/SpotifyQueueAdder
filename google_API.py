from googleapiclient.discovery import build
from google.oauth2 import service_account

class FormReader:
    SERVICE_ACCOUNT_FILE = 'google_keys.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
              'https://www.googleapis.com/auth/drive']
    
    def __init__(self, spreadsheetID):
        self.SPREADSHEET_ID = spreadsheetID
        self.creds = service_account.Credentials.from_service_account_file(FormReader.SERVICE_ACCOUNT_FILE, 
                                                                           scopes=FormReader.SCOPES)

    def start_service(self):
        self.service = build('sheets', 'V4', credentials=self.creds)
        self.sheet = self.service.spreadsheets()
    
    def get_range(self, range_read):
        range = self.sheet.values().get(spreadsheetId=self.SPREADSHEET_ID, 
                                             range=range_read).execute()
        return(range['values'])



if __name__ == '__main__':
    test = FormReader('17TFMRl9K5FDr3AoIkBs_d7A-mvqkipG0vtnbhlCXwFY')
    test.start_service()
    print(test.get_range('Form Responses 1!B2:B54'))