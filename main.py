# main.py
from player import Player
from db_manager import get_tracks, add_track, delete_track
import os

def print_menu(tracks):
    print("\nBoombox Playlist")
    for i, (track_id, title, artist, uri) in enumerate(tracks):
        track_info = f"{title} by {artist}"
        print(f"{i + 1}: {track_info}")
    print("0: Exit")
    print("A: Add a New Track")  # Add an option to add a new track
    print("D: Delete a Track")  # Add an option to delete a track

def add_new_track():
    title = input("Enter the title of the track: ")
    artist = input("Enter the artist of the track: ")
    file_path = input("Enter the URI of the track: ")
    
    if os.path.exists(file_path):  # Check if the file exists at the specified path
        if add_track(title, artist, file_path):  # Update the add_track function to accept file_path
            print("Track added successfully.")
        else:
            print("Failed to add the track.")
    else:
        print(f"The file at {file_path} does not exist.")

def delete_existing_track(tracks):
    track_number = input("Enter the number of the track to delete: ")
    if track_number.isdigit():
        track_number = int(track_number)
        if 1 <= track_number <= len(tracks):
            selected_track = tracks[track_number - 1]
            delete_track(selected_track[0])  # Delete the track by its track_id
            print("Track deleted successfully.")
        else:
            print("Invalid track number. Please enter a valid track number.")
    else:
        print("Invalid input. Please enter a valid track number.")

def main():
    player = Player()
    
    while True:
        tracks = get_tracks()  
        print_menu(tracks)
        
        choice = input("Select a number that corresponds to a track to play, 'A' to add a new track, 'D' to delete a track, or '0' to exit: ")
        
        if choice.lower() == 'add':
            add_new_track()
        elif choice.lower() == 'd':
            delete_existing_track(tracks)
        elif choice.isdigit():
            track_number = int(choice)
            if track_number == 0:
                break
            elif 1 <= track_number <= len(tracks):
                selected_track = tracks[track_number - 1]
                track_uri = selected_track[3]
                
                player.add_track(track_uri)  
                if player.load_track(track_number - 1):
                    player.play()
                    input("Press Enter to stop playback...")
                    player.stop()
                else:
                    print("Failed to load the track.")
            else:
                print("Invalid selection. Please enter a valid track number.")
        else:
            print("Invalid selection. Please enter a number, 'add', 'D', or '0'.")

if __name__ == "__main__":
    main()
