import os

directory = 'C:\\Users\\jezip\\Telegram-bot\\songdebug'

def list_mp3_files(directory):
    mp3_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.mp3'):
                mp3_files.append(file)
    return mp3_files

mp3_files = list_mp3_files(directory)

if mp3_files:
    for mp3_file in mp3_files:
        print(mp3_file)
else:
    print('damn, theres an error somewhere')