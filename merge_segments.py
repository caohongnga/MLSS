import argparse
import json
import os
parser = argparse.ArgumentParser(description='SEAME Data Processing')
parser.add_argument("--input_path", default="/media/chnga/DUPHONG1/SPEECH/IMDA - National Speech Corpus/CHNGA/check/SameRoomSegment/", type=str, help="Specify the direcotry path for input segment files with .txt extension.")
parser.add_argument("--output_path", default="/media/chnga/DUPHONG1/SPEECH/IMDA - National Speech Corpus/CHNGA/Segment_merge/", type=str, help="Specify the direcotry path for merged segments.")
parser.add_argument("--audio_path", default="/media/chnga/DATA1/SPEECH/SameRoomCHN/", type=str, help="Specify the direcotry path for audio segments will be stored.")
args = parser.parse_args()

def main():
    #Get list of meta file *.txt
    input_path=args.input_path
    output_path = args.output_path
    audio_path = args.audio_path
    threshold=1
    count_file=0
    for r, d, f in os.walk(input_path):
        for file in f:
            input_file = os.path.join(r, file)
            if file[-4:].lower() == '.txt': ##xu ly file wav
                file_open = open(input_file, encoding='utf-8')
                segments = []
                old_start= old_stop = 0
                filename =""
                for line in file_open:
                    seg = line.split()
                    if seg[0] != filename and filename!= "": #new file
                        count_file=count_file+1
                        # luu mau tin cuoi
                        entry = {}
                        entry['filename'] = filename
                        entry['from'] = old_start
                        entry['to'] = old_stop
                        entry['audio_filepath'] = audio_path+filename+".wav"
                        entry['duration'] = old_stop -old_start
                        entry['text'] = "nss"
                        segments.append(entry)
                        # gan gia tri cho file moi
                        old_start = old_stop = 0
                    filename = seg[0]
                    start = float(seg[1])
                    stop = float(seg[2])
                    len = float(seg[4])
                    if old_start == old_stop: #segment dau
                        if len>20: #khong can merge
                            entry = {}
                            entry['filename'] = filename
                            entry['from'] = old_start
                            entry['to'] = old_stop
                            entry['audio_filepath'] = audio_path + filename+ ".wav"
                            entry['duration'] = old_stop - old_start
                            entry['text'] = "nss"
                            segments.append(entry)
                            old_start = old_stop = 0
                        else: #luu tam xet segment tiep theo
                            old_start = start
                            old_stop = stop
                    else: # xet 2 segment ke tiep
                        if stop-old_start>25: # +do dai 2 segment ke tiep >25 khong merge
                            entry = {}
                            entry['filename'] = filename
                            entry['from'] = old_start
                            entry['to'] = old_stop
                            entry['audio_filepath'] = audio_path + filename+ ".wav"
                            entry['duration'] = old_stop - old_start
                            entry['text'] = "nss"
                            segments.append(entry)
                            old_start = start
                            old_stop = stop
                        if (start -old_stop)<threshold: #merge segment
                            old_stop = stop
                        else: #khong merge (khoang dung dai hon threshod)
                            entry = {}
                            entry['filename'] = filename
                            entry['from'] = old_start
                            entry['to'] = old_stop
                            entry['audio_filepath'] = audio_path + filename + ".wav"
                            entry['duration'] = old_stop - old_start
                            entry['text'] = "nss"
                            segments.append(entry)
                            old_start = start
                            old_stop = stop
                #segment cuoi cung
                entry = {}
                entry['filename'] = filename
                entry['from'] = old_start
                entry['to'] = old_stop
                entry['audio_filepath'] = audio_path + filename+ ".wav"
                entry['duration'] = old_stop - old_start
                entry['text'] = "nss"
                segments.append(entry)
                file_open.close()
                test_file = os.path.join(output_path, file)
                with open(test_file, 'w', encoding='utf-8') as fout:
                    for m in segments:
                        fout.write(json.dumps(m, ensure_ascii=False) + '\n')
    print("count_file", count_file)
if __name__ == "__main__":
    main()
