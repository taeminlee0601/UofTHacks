import pygame
import os

class Player:
    def __init__(self):
        pygame.mixer.init()
        self.tracks = []
        self.current_track_index = -1

    def add_track(self, track):
        if not os.path.exists(track):
            print(f"The file {track} does not exist.")
            return False
        self.tracks.append(track)
        return True

    def load_track(self, index):
        if index < 0 or index >= len(self.tracks):
            print("Invalid track number.")
            return False
        self.current_track_index = index
        track = self.tracks[index]
        pygame.mixer.music.load(track)
        print(f"Loaded {track}")
        return True

    def play(self):
        if self.current_track_index != -1:
            pygame.mixer.music.play()
            print(f"Playing {self.tracks[self.current_track_index]}")
        else:
            print("No track loaded.")

    def stop(self):
        pygame.mixer.music.stop()
        print("Playback stopped.")
