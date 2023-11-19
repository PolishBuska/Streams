from dataclasses import dataclass


@dataclass
class SongToPlaylist:
    song_id: int
    playlist_id: int
