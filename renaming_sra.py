#!/usr/bin/env python3

import sys, os, shutil, re, gzip


def renaming_sra(files):

    for file in files:
        dir_name = '_'.join(file.split("_")[:2])

        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        shutil.move(file,dir_name + "/" + file)



if __name__ == '__main__':
    files = sys.argv[1:]
    print("Files read\n")
    for file in files:
        print(file)

    renaming_sra(files)
