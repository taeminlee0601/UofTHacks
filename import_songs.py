# import_songs.py
import csv
from db_manager import add_track

def load_songs_from_file(file_path):
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            add_track(row['Title'], row['Artist'], row['URI'])

if __name__ == "__main__":
    load_songs_from_file('songs.csv')
