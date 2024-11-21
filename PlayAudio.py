import subprocess

mp3_file = "/data/data/com.termux/files/home/uploads/audio.mp3"
subprocess.run(['termux-media-player', 'play', mp3_file], check=True)
