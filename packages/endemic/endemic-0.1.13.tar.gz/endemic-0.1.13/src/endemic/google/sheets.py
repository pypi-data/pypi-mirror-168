from ..logging.interface import LoggerInterface


class GoogleSheetAPI:
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

    def __init__(self, logger: LoggerInterface, pygsheets_class):
        self.__logger = logger

        self.__pygsheets = pygsheets_class

        self.__google = None
        self.__google_credential_json = None
        self.__drive_folder_id = None

    def connect(self):

        if not self.google_credential_file_json:
            raise ValueError('Credential file path is None')

        self.__google = self.__pygsheets.authorize(service_file=self.__google_credential_json)

        return True

    def create_spreadsheet(self, title):
        self.__logger.debug('Create spreadsheet')

        return self.google.create(title, None, self.drive_folder_id)

    def list_sheets_ids(self):

        return self.google.spreadsheet_ids()

    def list_sheets_titles(self):

        return self.google.spreadsheet_titles()

    def list_sheets_meta(self):

        result_list = self.google.drive.spreadsheet_metadata()

        result = []
        if self.drive_folder_id:
            for item in result_list:
                if 'parents' in item:
                    if self.drive_folder_id in item['parents']:
                        result.append({'id': item['id'], 'name': item['name']})
            return result
        return result_list

    def share_doc(self, sh, email):
        self.__logger.debug('Share spreadsheet')

    def open_spreadsheet_by_id(self, key_id):
        self.__logger.debug('Open spreadsheet by key ')
        try:
            return self.google.open_by_key(key_id)
        except self.__pygsheets.exceptions.SpreadsheetNotFound:
            return None

    def open_spreadsheet_by_title(self, title):
        self.__logger.debug('Open spreadsheet by title ')

        spread_id = self.search_spreadsheet_by_title(title)
        self.__logger.debug('Key id is {}'.format(spread_id))
        if spread_id:
            return self.open_spreadsheet_by_id(spread_id)
        return None

    def search_spreadsheet_by_title(self, title):

        self.__logger.debug('Search spreadsheet by title')

        spread_id = None
        if self.drive_folder_id:
            spreads = self.list_sheets_meta()
            self.__logger.debug('List in folder {}'.format(spreads))
            for item in spreads:
                if title == item['name']:
                    spread_id = item['id']
                    break

        return spread_id

    def find_worksheet_by_title(self, sh, title):
        try:
            return self.google.spreadsheet_cls.worksheet_by_title(sh, title)
        except self.__pygsheets.exceptions.WorksheetNotFound:
            return None

    def create_worksheet_by_name(self, sh, title, cols, rows):
        try:
            return self.google.spreadsheet_cls.add_worksheet(sh, title, rows, cols)
        except self.__pygsheets.exceptions.WorksheetNotFound:
            self.__logger.exception('Worksheet not created')
            return False

    def find_cell_by_value(self, sheet, value):
        self.__logger.debug('find cell by value')

    def add_value_cell_by_coordinates(self, sheet, row, col, value):
        self.__logger.debug('add value to cell')
        try:
            sheet.update_value((row, col), value)
        except Exception:
            return False
        return True

    def merge_cells(self, sheet, row_start, row_end, col_start, col_end, merge_type='MERGE_ROWS'):
        self.__logger.debug('merge cell')
        address_start = self.__pygsheets.worksheet.Address((row_start, col_start))
        address_end = self.__pygsheets.worksheet.Address((row_end, col_end))
        print(address_start, address_end)

        datarange = self.__pygsheets.worksheet.DataRange(worksheet=sheet, start=address_start, end=address_end)
        datarange.merge_cells(merge_type)

    def set_cell_width(self, sheet, column_start, column_end, width):
        self.__logger.debug('Change columns width')
        sheet.adjust_column_width(column_start, column_end, width)

    @property
    def google_credential_file_json(self) -> str:
        return self.__google_credential_json

    @google_credential_file_json.setter
    def google_credential_file_json(self, value: str):
        self.__google_credential_json = value

    @property
    def drive_folder_id(self) -> str:
        return self.__drive_folder_id

    @drive_folder_id.setter
    def drive_folder_id(self, value: str):
        self.__drive_folder_id = value

    @property
    def google(self):
        return self.__google

    @google.setter
    def google(self, value):
        if isinstance(value, self.__pygsheets.client.Client):
            self.__google = value
        else:
            raise ValueError('Not string')
