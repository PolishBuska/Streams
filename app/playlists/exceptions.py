
class PlaylistAlreadyExist(Exception):
    ...


class M2MRelationExists(Exception):
    """
    Raised when trying to add a song that already exist to the playlist
    """
    ...


class LikeAlreadyExist(Exception):
    """
    Raised when trying give a like to a song that already exist
    """
    ...
