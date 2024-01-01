from gspread import service_account, Client, Spreadsheet


class SheetsParser:

    _urls: list[str]
    _client: Client
    _spreadsheets: list[Spreadsheet]

    def __init__(self, urls: list[str],
                 credentials: str = 'credentials.json') -> None:

        self._urls = urls
        self._client = service_account(filename=credentials)
        self._spreadsheets = [self._client.open_by_key('url') for url in urls]
