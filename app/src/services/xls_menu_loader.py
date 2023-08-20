import enum
from typing import TypeVar

import apiclient
import httplib2
import xlrd
from oauth2client.service_account import ServiceAccountCredentials

from app.src.config import settings


class LoaderStatus(enum.Enum):
    not_loaded = 0
    loaded = 1
    error = 2


class _XlsRow(list):
    """
    Класс строки для _XlsLoader. Нужно в связи с особенностью возврата из Sheet.
    Возвращаются данные по гриду и может отсутствовать не обязательный столбец со скидкой.
    Идея в том, чтобы сделать псевдосписок, который вернет значение по правильному индексу и пустышку по не правильному.
    """

    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except IndexError:
            return ''


class _XlsLoader:
    """
    Базовый загрузчик. У потомков нужно перекрывать _load
    """

    def __init__(self, source: str):
        self._source = source
        self._status: LoaderStatus = LoaderStatus.not_loaded
        self._error_message: str = ''
        self._pos = -1

        self._data: list[_XlsRow] = []
        return

    @property
    def status(self):
        return self._status

    @property
    def message(self):
        if self._status == LoaderStatus.not_loaded:
            return 'data not loaded'
        elif self._status == LoaderStatus.loaded:
            return 'data loaded'
        elif self._status == LoaderStatus.error:
            return f'processing error: {self._error_message}'

    def _load(self) -> list[_XlsRow]:
        return [_XlsRow('')]

    def load(self) -> None:
        try:
            self._data = self._load()
            self._status = LoaderStatus.loaded
        except Exception as e:
            print(e)  # write to log
            self._status = LoaderStatus.error
            self._error_message = str(e)

    def __getitem__(self, item):
        return self._data[item]

    def __iter__(self):
        return self

    def __next__(self):
        if self._pos < len(self._data) - 1:
            self._pos += 1
            return self._data[self._pos]
        else:
            self._pos = -1
            raise StopIteration


TXlsLoader = TypeVar('TXlsLoader', bound=_XlsLoader)


class XlsFileLoader(_XlsLoader):
    def _load(self) -> list[_XlsRow]:
        wb = xlrd.open_workbook(self._source)
        ws = wb.sheet_by_index(0)
        return [_XlsRow(ws.row_values(row)) for row in range(0, ws.nrows)]


class XlsSheetLoader(_XlsLoader):
    def _load(self) -> list[_XlsRow]:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            settings.EXCHANGE_SHEET_TOKEN,
            [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive',
            ]
        )
        http_auth = credentials.authorize(httplib2.Http())
        service = apiclient.discovery.build('sheets', 'v4', http=http_auth)
        spreadsheet = service.spreadsheets().get(
            spreadsheetId=self._source,
            includeGridData=True,
        ).execute()

        ws = spreadsheet['sheets'][0]['data'][0]
        return [_XlsRow(item.get('formattedValue', '') for item in line['values']) for line in ws['rowData']]
