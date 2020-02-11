from constants import MUSIC_LIBRARY_PATH
from main import sendCommand, jasminResponse
from bs4 import BeautifulSoup as soup
import youtube_dl
import vlc
import urllib2
import os

def playSong():
    
    path = MUSIC_LIBRARY_PATH
    jasminResponse("What song should I play?")
    song_choice = sendCommand()
    
    if song_choice:
        song_found = 0
        url = "https://www.youtube.com/results?search_query=" + song_choice.replace(' ', '+')
        final_url = ''
        response = urllib2.urlopen(url)
        html = response.read()
        parsed_html = soup(html,"lxml")
        video_list = parsed_html.findAll(attrs={'class':'yt-uix-tile-link'})

        if len(video_list) > 0:

            final_url = 'https://www.youtube.com' + video_list[0]['href']

            if (final_url).startswith("https://www.youtube.com/watch?v="):
                song_found = 1
        
        os.chdir(path)
        ydl_opts = {}

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([final_url])
        
        player = vlc.MediaPlayer(path)
        player.play()

        if song_found == 0:
            jasminResponse("I didn't find the song you are looking for.")
            playSong()

# Remove existing files functionality
#
def flushOldFiles(folder=MUSIC_LIBRARY_PATH):

    for selected_file in os.listdir(folder):
        file_path = os.path.join(folder, selected_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

