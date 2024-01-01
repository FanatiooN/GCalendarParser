from gspread import service_account, Client, Spreadsheet
from datetime import date, datetime
from pandas import DataFrame
from dotenv import load_dotenv
from Record import Record
import os
import re


class SheetsParser:
    _urls: list[str]
    _client: Client
    _spreadsheets: list[Spreadsheet]

    def __init__(self, urls: list[str], credentials: str = "credentials.json") -> None:
        self._urls = urls
        self._client = service_account(filename=credentials)
        self._spreadsheets = [self._client.open_by_url(url) for url in urls]

    def parseSchedule(self) -> DataFrame:
        records = []

        for spreadsheet in self._spreadsheets:
            worksheet = spreadsheet.get_worksheet(0)
            data = worksheet.get_all_values()

            for line in data:
                if re.match(r"\d{1,2}.\d{1,2}", line[0]):
                    date_str, time, fullname, duration, theme, difficulty = line
                    date_obj = datetime.strptime(date_str, "%d.%m").date()

                    record = Record(
                        date=date_obj,
                        time=time,
                        fullname=fullname,
                        duration=duration,
                        theme=theme,
                        difficulty=difficulty,
                    )

                    records.append(record)

        result = DataFrame(records)
        return result


if __name__ == "__main__":
    load_dotenv()

    urls = [os.environ.get("table_url")]
    parser = SheetsParser(urls=urls)
    print(parser.parseSchedule())
