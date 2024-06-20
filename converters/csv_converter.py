import csv
import os

import pandas as pd
from babel.numbers import parse_decimal


class CSVConverter:
    def __init__(self, args, input_files: dict):
        self._input_files = input_files
        self._xlsx_filename = args.xlsx_filename

        self._current_file = 0

        self._buy_events = []
        self._sell_events = []
        self._dividend_events = []
        self._forex_events = []

        self.df_deposits = pd.DataFrame(
            columns=[
                "date",
                "symbol",
                "quantity",
                "buy_price",
                "fees",
                "currency",
                "Product",
            ]
        )
        self.df_sales = pd.DataFrame(
            columns=[
                "date",
                "symbol",
                "quantity",
                "sell_price",
                "fees",
                "currency",
                "Product",
            ]
        )
        self.df_dividends = pd.DataFrame(
            columns=[
                "date",
                "symbol",
                "amount",
                "tax_withholding",
                "currency",
                "Product",
            ]
        )
        self.df_forex = pd.DataFrame(
            columns=["date", "foreign_amount", "source_fees", "source_currency", "target_currency"]
        )
        self.df_rsu = pd.DataFrame(
            columns=[
                "date",
                "symbol",
                "amount",
                "gross_quantity",
                "net_quantity",
                "fair_market_value",
                "currency",
                "Product",
            ]
        )
        self.df_espp = pd.DataFrame(
            columns=[
                "date",
                "symbol",
                "buy_price",
                "fair_market_value",
                "quantity",
                "currency",
                "Product",
            ]
        )

        self.row = ""
        self.processed_trades = 0
        self.processed_dividends = 0
        self.processed_forex = 0
        self.processed_instrument_information = 0

    def process_csv(self):
        for filename, encoding in self._input_files.items():
            with open(filename, encoding=encoding) as csv_file:
                self._current_file += 1
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    self.row = row
                    self._process_trades()
                    self._process_forex()
                    self._process_deposits_withdrawals()
                    self._process_dividends()
                    self._process_withholding_tax()
                    self._process_interest()
                    self._process_instrument_information()

        for df in [
            self.df_deposits,
            self.df_sales,
            self.df_dividends,
            self.df_forex,
            self.df_rsu,
            self.df_espp,
        ]:
            df.sort_values("date", inplace=True)

        print(f"Total processed trades: {self.processed_trades}")
        print(f"Total processed dividends: {self.processed_dividends}")
        print(f"Total processed Forex trades: {self.processed_forex}")
        print(f"Replaced symbols: {self.processed_instrument_information}")

    def write_to_xlsx(self):
        with pd.ExcelWriter(self._xlsx_filename, engine="xlsxwriter") as writer:
            self._write_sheet("buy_orders", self.df_deposits, writer)
            self._write_sheet("dividends", self.df_dividends, writer)
            self._write_sheet("sell_orders", self.df_sales, writer)
            self._write_sheet("currency_conversions", self.df_forex, writer)
            self._write_sheet("rsu", self.df_rsu, writer)
            self._write_sheet("espp", self.df_espp, writer)

        print(f"Results were written to '{os.path.basename(self._xlsx_filename)}'")

    @staticmethod
    def _write_sheet(name: str, df: pd.DataFrame, writer: pd.ExcelWriter):
        df.to_excel(writer, sheet_name=name, index=False, float_format="%.2f")
        worksheet = writer.sheets[name]
        worksheet.autofit()  # Adjust column widths to their maximum lengths

    @staticmethod
    def _parse_number(string: str):
        return float(parse_decimal(string, locale="en_US", strict=True))

    @staticmethod
    def _wrong_header(header: str):
        raise ValueError(
            "Input CSV is not in the expected format. Either this script needs adaptation or "
            f"a wrong type of CSV was downloaded. {header.title()} header is incorrect"
        )

    def _check_header(self, check_header: bool, expected_headers: list, header_type: str):
        if check_header:
            if not self.row == expected_headers:
                self._wrong_header(header_type)

            return True

        return False

    def _process_trades(self):
        raise NotImplementedError()

    def _process_forex(self):
        raise NotImplementedError()

    def _process_deposits_withdrawals(self):
        raise NotImplementedError()

    def _process_dividends(self):
        raise NotImplementedError()

    def _process_withholding_tax(self):
        raise NotImplementedError()

    def _process_interest(self):
        raise NotImplementedError()

    def _process_instrument_information(self):
        raise NotImplementedError()