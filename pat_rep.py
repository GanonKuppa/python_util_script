# -*- coding: utf-8 -*-

"""
ファイル内の文字列を置換
"""

import os,re,sys
import tempfile
import shutil

def pat_replace(stext,rtext,file):
    """
    porpose : ファイル内の文字列を（その場で）置換する
    usage   : pat_replace("置換前パターン","置換後文字列",'target-file')
              置換前パターンはreモジュールのパターンに準ずる
    """
    tmpfd,tmpname = tempfile.mkstemp(dir='.')
    try:
        output_file   = os.fdopen(tmpfd, 'w')
        input_file = open(file)
    except IOError:
        print( '"%s" cannot be opened.' % file)
    else:
        for line in input_file:
            pat = re.compile(stext)
            a = pat.sub(rtext, line)
            output_file.write(a)
    finally:
        output_file.close()
        input_file.close()

    shutil.copyfile(tmpname,file)
    os.remove(tmpname)

def main():
    if len(sys.argv) != 4:
        print( "Usage: python pat_rep.py stext rtext file_path")
        sys.exit(2)
    stext = sys.argv[1]
    rtext = sys.argv[2]
    file_path = sys.argv[3]

    pat_replace(stext,rtext,file_path)
    print( stext + " --> " + rtext + " in " + file_path)

if __name__ == '__main__':
    main()
