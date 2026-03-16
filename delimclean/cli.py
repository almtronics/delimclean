from pathlib import Path
import argparse
import pandas as pd
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("delimclean")
except PackageNotFoundError:
    __version__ = "0.0.0"

def parse_sep(value: str) -> str:
    v = value.strip().lower()

    aliases = {
        "t": "\t",
        "tab": "\t",
        "tabs": "\t",
        "tsv": "\t",

        "c": ",",
        "csv": ",",
        "comma": ",",
        "commas": ",",
        ",": ",",

        "s": ";",
        "semi": ";",
        "semicolon": ";",
        "semicol": ";",
        ";": ";",
    }

    if v in aliases:
        return aliases[v]

    if len(value) == 1:
        return value

    raise argparse.ArgumentTypeError(
        f"Unknown separator '{value}'. "
        "Use t/tab/tsv, c/comma/csv, s/semi/semicolon, or a single custom character."
    )


def positive_col(value: str) -> int:
    n = int(value)
    if n < 1:
        raise argparse.ArgumentTypeError("Column numbers must be 1 or greater.")
    return n


def get_files(path: Path, pattern: str):
    if path.is_file():
        return [path]
    if path.is_dir():
        return [p for p in path.glob(pattern) if p.is_file()]
    return []


def main():
    parser = argparse.ArgumentParser(
        prog="delimclean",
        description="Clean delimited files by skipping rows and keeping columns.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "path",
        help="Input file or folder"
    )
    parser.add_argument(
        "--skiprows",
        type=int,
        default=0,
        help="Number of rows to skip at the top of the file"
    )
    parser.add_argument(
        "--keepcols",
        type=positive_col,
        nargs="+",
        required=True,
        help="Column numbers to keep, starting from 1"
    )
    parser.add_argument(
        "--sep",
        type=parse_sep,
        default=",",
        help="Separator: t/tab/tsv, c/comma/csv, s/semi/semicolon, or a single custom character like |"
    )
    parser.add_argument(
        "--pattern",
        default="*",
        help="File pattern when input is a folder, for example *.txt"
    )
    parser.add_argument(
        "--suffix",
        default="_clean",
        help="Suffix added to each output filename"
    )
    parser.add_argument(
        "--names",
        nargs="+",
        help="Optional output column names"
    )
    parser.add_argument(
        "--no-header",
        action="store_true",
        help="Treat the inputfile as having no header row"
    )
    parser.add_argument(
    "--version",
    action="version",
    version=f"%(prog)s {__version__}",
    help="Show the installed version"
    )
    parser.add_argument(
    "--outdir",
    default="output",
    help="Output folder for cleaned files"
    )

    args = parser.parse_args()

    path = Path(args.path)
    sep = args.sep
    keepcols = [c - 1 for c in args.keepcols]

    files = get_files(path, args.pattern)
    if not files:
        print("No files found.")
        return

    for file in files:
        try:
            if args.no_header:
                df = pd.read_csv(file, sep=sep, skiprows=args.skiprows, header=None)
            else:
                df = pd.read_csv(file, sep=sep, skiprows=args.skiprows)

            df = df.iloc[:, keepcols]

            if args.names:
                if len(args.names) != len(df.columns):
                    raise ValueError("Number of --names must match number of kept columns.")
                df.columns = args.names

            raw_outdir = Path(args.outdir)
            if raw_outdir.is_absolute():
                out_dir = raw_outdir
            else:
                if path.is_dir():
                    out_dir = path / raw_outdir
                else:
                    out_dir = path.parent / raw_outdir

            out_dir.mkdir(parents=True, exist_ok=True)
            out_file = out_dir / f"{file.stem}{args.suffix}.csv"

            write_header = (not args.no_header) or bool(args.names)
            df.to_csv(out_file, index=False, header=write_header)

            print(f"Wrote: {out_file}")

        except Exception as e:
            print(f"Failed: {file} -> {e}")


if __name__ == "__main__":
    main()
