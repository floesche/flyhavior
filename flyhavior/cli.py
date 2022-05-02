"""Console script for flyhavior."""
import argparse
import sys
import datetime

from flyhavior import Flyhavior
from PostProcessor import PostProcessor


def main():
    """Console script for flyhavior."""
    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    parser.add_argument("--flyflix", help="flyflix file")
    parser.add_argument("--fictrac", help="fictrac file")
    parser.add_argument("--output", help="output filename")
    parser.add_argument("--post", help="Do post-processing like creating views and calculating aggregates.", action="store_true")
    args = parser.parse_args()

    print(f"Started: {datetime.datetime.now()}")

    if args.flyflix and args.fictrac:
        f = Flyhavior(args.flyflix, args.fictrac, args.output)
        f.run()
    
    if args.post:
        post = PostProcessor('data/test.db')
        post.fix_data()
        post.create_a_condition()
        post.alter_v_move()
        post.vacuum()
    print(f"Ended: {datetime.datetime.now()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
