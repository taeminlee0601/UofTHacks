# db_manager.py
import sqlite3

conn = sqlite3.connect('songs.db')
cursor = conn.cursor()

# Ensure the table structure matches the expected columns: id, title, artist, uri
cursor.execute('''
CREATE TABLE IF NOT EXISTS songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    uri TEXT NOT NULL UNIQUE
)
''')
conn.commit()

def add_track(title, artist, uri):
    try:
        cursor.execute('INSERT INTO songs (title, artist, uri) VALUES (?, ?, ?)', (title, artist, uri))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # URI is not unique
        return False

def get_tracks():
    cursor.execute('SELECT id, title, artist, uri FROM songs')  # Ensure you select only the necessary columns
    return cursor.fetchall()

def delete_track(track_id):
    # Delete a track from the database by its track_id
    cursor.execute('DELETE FROM songs WHERE id = ?', (track_id,))
    conn.commit()