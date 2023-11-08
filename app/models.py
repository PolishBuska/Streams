from sqlalchemy import (ForeignKey,
                        Column,
                        TIMESTAMP,
                        func)
from sqlalchemy.orm import (Mapped,
                            mapped_column,
                            relationship)

from app.db import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    nickname: Mapped[str]
    password: Mapped[str]
    role_id: Mapped[int]
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
    cover_link: Mapped[str]
    title: Mapped[int]
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"),
                                           nullable=False)
    author = relationship("User",
                          backref="Songs")
    description: Mapped[str]
    link: Mapped[str]
    filename: Mapped[str]
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False,
                        server_default=func.now())
