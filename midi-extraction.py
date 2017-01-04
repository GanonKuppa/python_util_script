# -*- coding: utf-8 -*-

"""
midiファイルの内容をcsv化して出力

event,tick,channel,notenum,velocity
tickは絶対時間
"""
import midi
import codecs
import os,re,sys
import tempfile
import shutil
import time
import pandas as pd
import csv

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

def line_delete_back(line_num,file):
    tmpfd,tmpname = tempfile.mkstemp(dir='.')
    try:
        output_file   = os.fdopen(tmpfd, 'w')
        input_file = open(file)
    except IOError:
        print( '"%s" cannot be opened.' % file)
    else:
        num_lines = sum(1 for line in input_file)
        input_file.close()
        input_file = open(file)
        for i,line in enumerate(input_file):
            if i !=  num_lines -1  - int(line_num)+ 1:
                a = line
                output_file.write(a)
    finally:
        output_file.close()
        input_file.close()

    shutil.copyfile(tmpname,file)
    os.remove(tmpname)


############################################################



def main():
    if len(sys.argv) != 2:
        print "Usage: {0} <midifile>".format(sys.argv[0])
        sys.exit(2)

    temp_dir_name = "temp-midi-extraction"
    if not os.path.exists(temp_dir_name):
        os.makedirs(temp_dir_name)

    midifile = sys.argv[1]
    pattern = midi.read_midifile(midifile)

    track_list = []

    save_path = temp_dir_name + "/tmep_midi" +".txt"
    sys.stdout = open(save_path,"w")
    print(pattern)

    for (i,ele) in enumerate(pattern):
        save_path = temp_dir_name + "/tmep_midi" + str(i) +".csv"
        track_list.append(save_path)
        sys.stdout = open(save_path,"w")
        print(pattern[i])

    sys.stdout = sys.__stdout__


    for ele in track_list:
        #ほしいデータが並んだcsvファイルに変換
        line_delete(1,ele)
        line_delete_back(1,ele)
        pat_replace(r'\(',r",",ele)
        pat_replace(r'tick=',r" ",ele)
        pat_replace(r'midi\.',r" ",ele)
        pat_replace(r'channel=',r" ",ele)
        pat_replace(r'data=\[\]',r"data=[0,0]",ele)
        pat_replace(r'data=\[',r" ",ele)
        pat_replace(r'\]\),',r" ",ele)
        pat_replace(r'\[',r" ",ele)
        pat_replace(r' ',r"",ele)

        #tickを絶対時間に変換
        ab_tick = 0
        f = open(ele, 'rb')
        dataReader = csv.reader(f)
        new_lines = []
        for row in dataReader:
            ab_tick = int(row[1]) +ab_tick
            row[1] = str(ab_tick)
            new_lines.append(row)

        name,ext = os.path.splitext( os.path.basename(ele) )
        tr_ab_name = temp_dir_name + "/" + name + "_ab"+ext
        with open( tr_ab_name, 'w') as f:
            writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
            writer.writerows(new_lines) # 2次元配列も書き込める
        #NoteOn/Offイベント以外を除去
        name,ext = os.path.splitext( os.path.basename(tr_ab_name) )
        tr_onOff_name = temp_dir_name + "/" + name + "_onOff"+ext
        f = open(tr_ab_name, 'rb')
        dataReader = csv.reader(f)
        new_lines = []
        for row in dataReader:
            if  "NoteO" in row[0]:
                new_lines.append(row)

        with open( tr_onOff_name, 'w') as f:
            writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
            writer.writerows(new_lines) # 2次元配列も書き込める


if __name__ == '__main__':
    main()


    """
    noteoneventを

    """
