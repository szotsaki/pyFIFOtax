import argparse

parser = argparse.ArgumentParser(
    description="Convert Interactive Brokers CSV and Schwab JSON output to XLSX for later processing"
)
parser.add_argument(
    "type",
    type=str,
    choices=["ibkr", "schwab"],
    help="Used broker",
)
parser.add_argument(
    "-i",
    "--input",
    dest="input_filename",
    type=str,
    required=True,
    help="Input file (CSV file from Interactive Brokers or JSON from Schwab)",
)
parser.add_argument(
    "-o",
    "--output",
    dest="xlsx_filename",
    type=str,
    required=True,
    help="Output XLSX file",
)
parser.add_argument(
    "--ibkr-ticker-to-isin",
    dest="ibkr_isin_replace",
    type=bool,
    default=False,
    action=argparse.BooleanOptionalAction,
    help="Replace tickers in the 'symbol' column to ISIN (only for IBKR)",
)


def main(arguments):
    if arguments.type == "ibkr":
        from converters.ibkr import IbkrConverter
        converter = IbkrConverter(arguments)
        converter.process_csv()
        converter.write_to_xlsx()
    elif arguments.type == "schwab":
        from converters.schwab import convert
        convert(arguments)
    else:
        raise ValueError("This type of converter is not recognised")


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
