import csv
import os
import sys
import warnings
import shutil

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=RuntimeWarning)
    from pydub import AudioSegment

def create_audio(experiment, audio_path, stimfile_path, minstim):
    '''This function creates AAAB and ABAA files and stores them in a folder called 'tmp' within
        the original audio folder.
        experiment: This is the name for the current experiment as indicated by the user.
        audio_path: This is the path where the original audio files are stored.
        stimfile_path: This is where the stimulus csv file will be saved.
        minstim: This is the standard stimulus to which all audio will be compared. By default,
                 this would be the first audio file.
        '''
    audpath = audio_path
    csvpath = stimfile_path
    #os.chdir(audpath)
    audio_list = [os.path.join(audpath, file) for file in os.listdir(audpath) if file.endswith('.wav')][(minstim-1):]
    base = AudioSegment.from_file(audio_list[0], format="wav")
    short_silence = AudioSegment.silent(duration=250)
    long_silence = AudioSegment.silent(duration=500)
    AA = base + short_silence + base
    
    if os.path.exists(os.path.join(audpath, 'tmp')):
        shutil.rmtree(os.path.join(audpath, 'tmp'))
    os.mkdir(os.path.join(audpath, 'tmp'))
    
    with open(csvpath, 'w', newline='') as input_csv:
        writer = csv.writer(input_csv, delimiter=',')
        writer.writerow(['Filename', 'Level', 'CorrectResponse', 'Original Base Filename', 'Original Comparison Filename'])
        for aud in audio_list:
            comparison = AudioSegment.from_file(aud, format="wav")
            AB = base + short_silence + comparison
            AAAB = AA + long_silence + AB
            ABAA = AB + long_silence + AA
            level_num = audio_list.index(aud) + 1
            AAAB_path = os.path.join(audpath, 'tmp', 
                                     '{}_level{}_{}'.format(experiment, level_num, 'AAAB.wav'))
            ABAA_path = os.path.join(audpath, 'tmp', 
                                    '{}_level{}_{}'.format(experiment, level_num, 'ABAA.wav'))
            AAAB.export(AAAB_path, format='wav')
            ABAA.export(ABAA_path, format='wav')
            writer.writerow([os.path.basename(AAAB_path), level_num, 2, audio_list[0], aud])
            writer.writerow([os.path.basename(ABAA_path), level_num, 1, audio_list[0], aud])