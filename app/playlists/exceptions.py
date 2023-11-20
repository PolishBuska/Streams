
class PlaylistAlreadyExist(Exception):
    ...


class M2MRelationExists(Exception):
    """
    Raised when trying to add a song that already exist to the playlist
    """
    ...
