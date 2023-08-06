import argparse
import googlesheets2csv

# https://github.com/python/cpython/blob/main/Lib/argparse.py
class CustomFormatter(argparse.RawTextHelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings:
            default = self._get_default_metavar_for_positional(action)
            (metavar,) = self._metavar_formatter(action, default)(1)
            return metavar

        else:
            parts = []

            # if the Optional doesn't take a value, format is:
            #    -s, --long
            if action.nargs == 0:
                parts.extend(action.option_strings)

            # if the Optional takes a value, format is:
            #    -s ARGS, --long ARGS
            else:
                default = self._get_default_metavar_for_optional(action)
                args_string = self._format_args(action, default)
                for option_string in action.option_strings:
                    parts.append(option_string)

                return "%s %s" % (", ".join(parts), args_string)

            return ", ".join(parts)


parser = argparse.ArgumentParser(
    prog="googlesheets2csv",
    description="Export google spreadsheet to csv, you can filter data with SQL statement.",
    epilog="",
    formatter_class=CustomFormatter,
)

parser.add_argument(
    "-v",
    "--version",
    action="version",
    version="%(prog)s " + googlesheets2csv.__version__,
)


parser.add_argument(
    "-c",
    "--credential_file",
    required=True,
    metavar="",
    type=str,
    help="Google Cloud service account JSON file with credentials",
)

parser.add_argument(
    "-sn",
    "--spreadsheet_name",
    required=True,
    metavar="",
    type=str,
    help="spreadsheet name which you want to access",
)

parser.add_argument(
    "-wn",
    "--worksheet_name",
    required=True,
    metavar="",
    type=str,
    help="worksheet name which you want to access",
)

parser.add_argument(
    "-sql",
    metavar="",
    type=str,
    default="",
    help='You can filter data with SQL statement.(default "SELECT * FROM your_worksheet_name")',
)

parser.add_argument(
    "output",
    metavar="output",
    type=str,
    help="Output csv file path",
)


def parse_args(args=None):
    return parser.parse_args(args)


def main(args=None):
    parsed_args = parse_args(args)
    googlesheets2csv.to_csv(
        parsed_args.credential_file,
        parsed_args.spreadsheet_name,
        parsed_args.worksheet_name,
        parsed_args.sql,
        parsed_args.output,
    )
