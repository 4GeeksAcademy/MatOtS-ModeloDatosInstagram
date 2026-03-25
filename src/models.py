from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    userName: Mapped[str] = mapped_column(
        String(120), nullable=False)
    firstJName: Mapped[str] = mapped_column(
        String(120), nullable=False)
    lastName: Mapped[str] = mapped_column(
        String(120), nullable=False)
    
    posts: Mapped[List["Post"]] = relationship(back_populates="user")

    comment: Mapped["Comment"] = relationship(back_populates="user")
    like: Mapped["Like"] = relationship(back_populates="user")

    followers: Mapped[List["Follower"]] = relationship(back_populates="user")
    followeds: Mapped[List["Follower"]] = relationship(back_populates="user")


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    text: Mapped[str] = mapped_column(String(240))
    media: Mapped[str] = mapped_column(String(500))

    user: Mapped["User"] = relationship(back_populates="posts")

    collabs: Mapped[List["Collaborator"]] = relationship(back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship(back_populates="post")
    likes: Mapped["Like"] = relationship(back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "text": self.text,
            "media": self.media
        }


class Collaborator(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    collab_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped[int] = mapped_column(ForeignKey("user.id"))

    posts: Mapped[List["Post"]] = relationship(back_populates="collabs")

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(240))
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    # 1 usuario - 1 comentario
    user: Mapped["User"] = relationship(back_populates="comment")

    # 1 post - varios comentarios
    post: Mapped["Post"] = relationship(back_populates="comments")

    def serialize(self):
        return {
            "comment_text": self.comment_text
        }


class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    following_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    userFollower: Mapped[List["User"]] = relationship(secondary="follow_user", back_populates="followers")
    userFollowed: Mapped[List["User"]] = relationship(secondary="following_user", back_populates="followeds")



class Like(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    # 1 post - varios likes
    post: Mapped["Post"] = relationship(back_populates="likes")

    # 1 like - 1 user
    user: Mapped["User"] = relationship(back_populates="like")
