# -*- coding: utf-8 -*-


"""
Print a description of a MIDI file.
"""
#import midi
import codecs
import os,re,sys
import tempfile
import shutil



def pat_replace(stext,rtext,file):
    """
    porpose : ファイル内の文字列を（その場で）置換する
    usage   : pat_replace("置換前パターン","置換後文字列",'target-file') --> replaced file
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


############################################################
#if len(sys.argv) != 2:
    #print "Usage: {0} <midifile>".format(sys.argv[0])
#    sys.exit(2)

temp_dir_name = "temp-midi-extraction"
if not os.path.exists(temp_dir_name):
    os.makedirs(temp_dir_name)

#midifile = sys.argv[1]
#pattern = midi.read_midifile(midifile)

#track_list = []
track_list = os.listdir(temp_dir_name)
#for (i,ele) in enumerate(pattern):
#    save_path = "tmep_midi" + str(i) +".txt"
#    track_list.append(save_path)
#    sys.stdout = open(save_path,"w")
#    print pattern[i]

print(track_list)

for ele in track_list:
    #lines2 = []
    #read_file = codecs.open(temp_dir_name+"/"+ele, 'r', 'shift_jis')
    #lines = read_file.readlines() #読み込み
    #for line in lines:
    #    line = line.replace("(",",") #テキスト置換
    #    lines2.append(line) #別リストにする
    pat_replace(r'\(',r",",temp_dir_name+"/"+ele)
    pat_replace(r'tick=',r" ",temp_dir_name+"/"+ele)
    pat_replace(r'midi\.',r" ",temp_dir_name+"/"+ele)
    pat_replace(r'channel=',r" ",temp_dir_name+"/"+ele)
    pat_replace(r'data=\[\]',r"data=[0,0]",temp_dir_name+"/"+ele)
    pat_replace(r'data=\[',r" ",temp_dir_name+"/"+ele)
    pat_replace(r'\]\),',r" ",temp_dir_name+"/"+ele)
#イベント,tick,channel,notenum,velocity
#midi_data = pretty_midi.PrettyMIDI(midifile) #midiファイルを読み込みます
##for ele in midi_data.get_piano_roll():
#    for ele_ele in ele:
#        print(ele_ele) #ピアノロールを出力します
#    print "---------------"

#print(midi_data.synthesize()) #サイン波を使って、波形を出力します。
