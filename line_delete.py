# -*- coding: utf-8 -*-

"""
ファイルの指定行を除去
"""
import os
import sys
import tempfile
import shutil


def line_delete(line_num,file):
    tmpfd,tmpname = tempfile.mkstemp(dir='.')
    try:
        output_file   = os.fdopen(tmpfd, 'w')
        input_file = open(file)
    except IOError:
        print( '"%s" cannot be opened.' % file)
    else:
        for i,line in enumerate(input_file):
            if i != int(line_num)-1:
                a = line
                output_file.write(a)
    finally:
        output_file.close()
        input_file.close()

    shutil.copyfile(tmpname,file)
    os.remove(tmpname)


def main():
    if len(sys.argv) != 3:
        print( "Usage: python line_delete.py line_num file_path")
        sys.exit(2)
    line_num = sys.argv[1]
    file_path = sys.argv[2]
    line_delete(line_num,file_path)
    print("delete line:" + line_num  + " in " + file_path)

if __name__ == '__main__':
    main()
