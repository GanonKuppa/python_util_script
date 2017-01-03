# -*- coding: utf-8 -*-

"""
コマンドライン引数を伴うスクリプトのテンプレート
"""
import sys

def main():
    if len(sys.argv) != 2:
        print( "Usage: python template_argv.py file_path")
        sys.exit(2)
    file_path = sys.argv[1]
    print(file_path)

if __name__ == '__main__':
    main()
