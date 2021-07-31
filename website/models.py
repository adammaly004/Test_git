
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask import flash, request


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)


class Save:
    def __init__(self, type):
        self.type = type

        if self.type == "tempo":
            self.save_tempo()

        elif self.type == "speed":
            self.save_speed()

        elif self.type == "long":
            self.save_long()

        elif self.type == "trot":
            self.save_trot()

        elif self.type == "intervals":
            self.save_intervals()

    def save_tempo(self):
        flash(self.type)
        trot_before = request.form.get("trot-before")
        trot_after = request.form.get("trot-after")
        main_kilometres = request.form.get("main-kilometres")
        pace = request.form.get("pace")
        abc = request.form.get("abc")
        warm_up = request.form.get("warm")
        time = request.form.get("time")

        total_kilometres = int(trot_before) + \
            int(main_kilometres) + int(trot_after)

        print(
            f"Before: {trot_before}, Type: {self.type}, After: {trot_after}, Kilometres: {main_kilometres}, Pace: {pace}, Abc: {abc}, Warm up: {warm_up}, Time: {time}, Total: {total_kilometres}")

    def save_speed(self):
        flash(self.type)

    def save_long(self):
        flash(self.type)

    def save_trot(self):
        flash(self.type)

    def save_intervals(self):
        flash(self.type)
