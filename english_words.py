#!/usr/bin/env python3
import sys


def main(args=sys.argv):
    # check arguments
    if len(args) == 1:
        print("Add it to the first argument.")
        sys.exit()


if __name__ == "__main__":
    main()
