"""Console script for flyhavior."""
import argparse
import sys

from flyhavior import Flyhavior


def main():
    """Console script for flyhavior."""
    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    parser.add_argument("--flyflix", help="flyflix file")
    parser.add_argument("--fictrac", help="fictrac file")
    parser.add_argument("--output", help="output filename")
    args = parser.parse_args()

    print("Arguments: " + str(args._))
    print("Replace this message by putting your code into "
          "flyhavior.cli.main")
    f = Flyhavior(args.flyflix, args.fictrac, args.output)
    f.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
