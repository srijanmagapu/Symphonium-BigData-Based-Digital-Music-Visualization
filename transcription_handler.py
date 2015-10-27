from music_transcriber import MusicTranscriber
import os
import time

MUSIC_FILES_DIR = 
LILYPOND_DIR = '/
SHEET_NOTES_DIR = '/var/www/transcriber_website/static/sheet_notes'
MIDI_DIR = '
ONSET_FRAMES_DIR = '/

if __name__ == '__main__':
    while(True):
        music_files = os.listdir(MUSIC_FILES_DIR)
        print music_files
        if len(music_files) == 0:
            print 'NO MUSIC FILES'
            time.sleep(0.5)
        else:
      
            transcriber.transcribe()
            print('MUSIC FILE NAME: %s') % music_file
            os.rename(music_file[:-3] + 'pdf', SHEET_NOTES_DIR + '/' + music_file[:-3] + 'pdf')
            os.rename(music_file[:-3] + 'midi', MIDI_DIR + '/' + music_file[:-3] + 'midi')
            os.remove(MUSIC_FILES_DIR + '/' + music_file)
            os.remove(LILYPOND_DIR + '/' + music_file[:-3] + 'ly')
            command = "timidity "
            command += (MIDI_DIR + '/' + music_file[:-3] + 'midi')
            command += (' -Ow -o ' + MIDI_DIR + '/' + music_file[:-3] + 'wav')
            print command
            os.system(command)
