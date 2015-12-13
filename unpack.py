#!/usr/bin/python3

import zipfile
import argparse
import os

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("zip", nargs='+')

    args = ap.parse_args()

    for fn in args.zip:
        zf = zipfile.ZipFile(fn)

        for i in zf.namelist():
            prefix, _, suffix = i.partition('/')

            if not suffix:
                continue

            if suffix.endswith('.txt') and ('/' not in suffix):
                suffix = suffix.replace(".txt", "." + prefix + ".txt")

            print(suffix)

            if suffix.endswith("/"):
                if not os.path.isdir(suffix):
                    os.mkdir(suffix)
            else:
                with zf.open(i, 'r') as f:
                    data = f.read()

                with open(suffix, 'wb') as f:
                    f.write(data)


        zf.close()


if __name__ == "__main__":
    main()
