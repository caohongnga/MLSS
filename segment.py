#https://github.com/pyannote/pyannote-audio
#conda create -n pyannote python=3.8
#conda activate pyannote
#conda install pytorch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 -c pytorch
#pip install pyannote.audio

import argparse
import os
from datetime import datetime
from pyannote.audio import Pipeline
parser = argparse.ArgumentParser(description='Segment unannotated audio for semi-supervised learning')
parser.add_argument("--input_path", default="/media/chnga/DATA1/cs/IMDA - National Speech Corpus/Same Room Audio/CHN/" 
, type=str, help="Specify the direcotry path for input audios.")
parser.add_argument("--output_path", default="/media/chnga/DATA1/cs/SameRoomSegment/", type=str, help="Specify the direcotry path for output segments.")
args = parser.parse_args()

def main():
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization")
    input_path=args.input_path
    output_path = args.output_path
    dt = datetime.now()
    str_date_time = dt.strftime("%Y-%m-%d, %H:%M:%S")
    print(str_date_time)
    time_file=open(output_path + "time.text", "a", encoding='utf-8')
    time_file.write("start time: "+str_date_time + "\n")
    time_file.close()
    count=0 #Number of file
    count_line=0 #Number of segments
    results = []
    for r, d, f in os.walk(input_path):
        for file in f:
            if file[-4:].lower() == '.wav':
                input_file=os.path.join(r, file)
                diarization = pipeline(input_file)
                for turn, _, speaker in diarization.itertracks(yield_label=True):
                    results.append(f"{file[:-4]} {turn.start:.3f}   {turn.end:.3f}	speaker_{speaker}   {(turn.end-turn.start):3f}")
                    count_line =count_line + 1
                count = count + 1
    output_file = os.path.join(output_path, 'segments.txt')
    textfile = open(output_file, "w", encoding="utf-8")
    for element in results:
        textfile.write(element + "\n")
    textfile.close()
    print("count file",count)
    print("count line",count_line)
    dt = datetime.now()
    str_date_time = dt.strftime("%Y-%m-%d, %H:%M:%S")
    print(str_date_time)
    time_file = open(output_path + "time.text", "a", encoding='utf-8')
    time_file.write("stop time: " + str_date_time + "\n")
    time_file.write("stop time: " + str_date_time + "\n")
    time_file.close()
if __name__ == "__main__":
    main()
