from dataclasses import dataclass

from app.playlists.commands import SongToPlaylist


@dataclass
class PlaylistEntity:

    def __init__(self, song_id: int, playlist_id: int):
        self.song_id = song_id
        self.playlist_id = playlist_id

    async def subscribe_to_playlist(self) -> "SongToPlaylist":
        return SongToPlaylist(song_id=self.song_id,
                              playlist_id=self.playlist_id)
