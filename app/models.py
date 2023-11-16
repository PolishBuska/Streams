from sqlalchemy import (ForeignKey,
                        Column,
                        TIMESTAMP,
                        func,
                        )
from sqlalchemy.orm import (Mapped,
                            mapped_column,
                            relationship)

from app.db import Base


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
