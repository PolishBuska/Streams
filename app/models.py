from sqlalchemy import (ForeignKey,
                        Column,
                        TIMESTAMP,
                        func, UniqueConstraint,
                        )
from sqlalchemy.orm import (Mapped,
                            mapped_column,
                            relationship)

from app.core.db import Base


class Roles(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str]


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    nickname: Mapped[str]
    password: Mapped[str]
    role_id: Mapped[int] = mapped_column(ForeignKey('role.id'))
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=func.now())


class Genre(Base):
    __tablename__ = "genre"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    desc: Mapped[str]
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=func.now())


class Song(Base):
    __tablename__ = "song"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(unique=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"),
                                           nullable=False)
    author = relationship("User",
                          backref="Songs")
    description: Mapped[str]
    link: Mapped[str]
    filename: Mapped[str]
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=func.now())
    playlists = relationship('PlaylistToSong',
                             back_populates='song',
                             lazy="joined")


class Playlist(Base):
    __tablename__ = "playlist"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"),
                                           nullable=False)
    author = relationship("User",
                          backref="Playlists", lazy="joined")

    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=func.now())
    songs = relationship('PlaylistToSong',
                         back_populates='playlist',
                         lazy="joined")


class PlaylistToSong(Base):
    __tablename__ = "playlist_to_song"
    __table_args__ = (UniqueConstraint('playlist_id', 'song_id', name='uix_1'),)
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    playlist_id: Mapped[int] = mapped_column(ForeignKey("playlist.id", ondelete="CASCADE"), nullable=False)
    song_id: Mapped[int] = mapped_column(ForeignKey("song.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    # relationships
    song = relationship('Song',
                        back_populates='playlists',
                        lazy="joined")
    playlist = relationship('Playlist',
                            back_populates='songs',
                            lazy="joined")


class LikedSongs(Base):
    __tablename__ = "liked_songs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"),
                                         nullable=False)
    user = relationship("User", back_populates='user', lazy="joined", foreign_keys=[user_id])
    song_id: Mapped[int] = mapped_column(ForeignKey("song.id", ondelete="CASCADE"),
                                         nullable=False)
    song = relationship("Song", back_populates='song', lazy="joined", foreign_keys=[song_id])

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
