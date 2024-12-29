from tkinter import *
import tkinter as tk
from tkinter import filedialog
from pygame import mixer
import os
import time
from mutagen.mp3 import MP3


class MP:
    def __init__(self, window):
        self.window = window
        window.geometry("600x450")
        window.title("Dynamic Music Player")
        window.resizable(0, 0)
        window.config(bg="#f0f0f0")

        mixer.init()

        self.play_restart = tk.StringVar()
        self.pause_resume = tk.StringVar()
        self.play_restart.set("Play")
        self.pause_resume.set("Pause")
        self.music_file = False
        self.playing_state = False
        self.song_length = 0
        self.song_elapsed = 0

        playlist_frame = Frame(window, bg="white", bd=2, relief=GROOVE)
        playlist_frame.place(x=20, y=20, width=380, height=300)
        self.playlist = Listbox(
            playlist_frame,
            selectmode=SINGLE,
            bg="#e0f7fa",
            fg="black",
            font=("Arial", 12),
            width=35,
            height=15,
        )
        self.playlist.pack(padx=5, pady=5)

        control_frame = Frame(window, bg="#f8f9fa")
        control_frame.place(x=420, y=20, width=150, height=300)

        # Controls
        load_button = Button(
            control_frame,
            text="Load Songs",
            bg="#81c784",
            fg="white",
            font=("Arial", 10),
            width=12,
            command=self.load,
        )
        load_button.pack(pady=10)

        play_button = Button(
            control_frame,
            textvariable=self.play_restart,
            bg="#4fc3f7",
            fg="white",
            font=("Arial", 10),
            width=12,
            command=self.play,
        )
        play_button.pack(pady=10)

        pause_button = Button(
            control_frame,
            textvariable=self.pause_resume,
            bg="#ffd54f",
            fg="white",
            font=("Arial", 10),
            width=12,
            command=self.pause,
        )
        pause_button.pack(pady=10)

        stop_button = Button(
            control_frame,
            text="Stop",
            bg="#e57373",
            fg="white",
            font=("Arial", 10),
            width=12,
            command=self.stop,
        )
        stop_button.pack(pady=10)

        shuffle_button = Button(
            control_frame,
            text="Shuffle",
            bg="#ba68c8",
            fg="white",
            font=("Arial", 10),
            width=12,
            command=self.shuffle,
        )
        shuffle_button.pack(pady=10)

        repeat_button = Button(
            control_frame,
            text="Repeat",
            bg="#64b5f6",
            fg="white",
            font=("Arial", 10),
            width=12,
            command=self.repeat,
        )
        repeat_button.pack(pady=10)

        # Volume and Song Details
        volume_frame = Frame(window, bg="#f0f0f0")
        volume_frame.place(x=20, y=330, width=550, height=100)

        self.song_title = Label(
            volume_frame,
            text="No song loaded",
            font=("Arial", 12),
            bg="#f0f0f0",
            anchor="w",
        )
        self.song_title.pack(fill=X, padx=10, pady=5)

        self.song_duration = Label(
            volume_frame,
            text="Duration: 00:00",
            font=("Arial", 10),
            bg="#f0f0f0",
            anchor="w",
        )
        self.song_duration.pack(fill=X, padx=10)

        self.song_elapsed_time = Label(
            volume_frame,
            text="Elapsed: 00:00",
            font=("Arial", 10),
            bg="#f0f0f0",
            anchor="w",
        )
        self.song_elapsed_time.pack(fill=X, padx=10)

        volume_label = Label(volume_frame, text="Volume:", font=("Arial", 10), bg="#f0f0f0")
        volume_label.pack(side=LEFT, padx=10)

        self.volume_slider = Scale(
            volume_frame,
            from_=0,
            to=100,
            orient=HORIZONTAL,
            command=self.set_volume,
            length=300,  
            bg="#f0f0f0",
            highlightthickness=0 
        )
        self.volume_slider.set(50)  
        self.volume_slider.pack(side=LEFT, padx=10)

    def load(self):
        files = filedialog.askopenfilenames(filetypes=[("MP3 Files", "*.mp3")])
        for file in files:
            self.playlist.insert(END, os.path.basename(file))
        self.music_files = list(files)

    def play(self):
        try:
            selected_song_index = self.playlist.curselection()[0]
            self.music_file = self.music_files[selected_song_index]
            mixer.music.load(self.music_file)
            mixer.music.play()
            self.play_restart.set("Restart")
            self.pause_resume.set("Pause")
            self.playing_state = False
            self.display_song_details()
        except IndexError:
            print("No song selected!")

    def pause(self):
        if not self.playing_state:
            mixer.music.pause()
            self.playing_state = True
            self.pause_resume.set("Resume")
        else:
            mixer.music.unpause()
            self.playing_state = False
            self.pause_resume.set("Pause")

    def stop(self):
        mixer.music.stop()
        self.play_restart.set("Play")
        self.song_elapsed_time.config(text="Elapsed: 00:00")

    def shuffle(self):
        import random
        self.playlist.selection_clear(0, END)
        random_index = random.randint(0, self.playlist.size() - 1)
        self.playlist.selection_set(random_index)
        self.play()

    def repeat(self):
        if self.music_file:
            mixer.music.play(loops=-1)

    def set_volume(self, volume):
        mixer.music.set_volume(int(volume) / 100)

    def display_song_details(self):
        if self.music_file:
            audio = MP3(self.music_file)
            self.song_length = audio.info.length
            self.song_title.config(text=f"Playing: {os.path.basename(self.music_file)}")
            self.song_duration.config(text=f"Duration: {time.strftime('%M:%S', time.gmtime(self.song_length))}")
            self.update_elapsed_time()

    def update_elapsed_time(self):
        if mixer.music.get_busy():
            self.song_elapsed += 1
            self.song_elapsed_time.config(text=f"Elapsed: {time.strftime('%M:%S', time.gmtime(self.song_elapsed))}")
            self.window.after(1000, self.update_elapsed_time)


# Main Loop
root = Tk()
MP(root)
root.mainloop()