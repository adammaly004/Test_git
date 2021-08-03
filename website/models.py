
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
    type = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)
    warm_up = db.Column(db.Text, nullable=False)
    abc = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)


class Save:
    def __init__(self, type):
        self.type = type
        if self.type != None:
            self.get()

    def get(self):
        flash(self.type)

        self.trot_before = request.form.get("trot-before")
        self.trot_after = request.form.get("trot-after")

        self.abc = request.form.get("abc")
        self.warm_up = request.form.get("warm")

        self.main_kilometres = request.form.get("main-kilometres")
        self.main_kilometres_time = request.form.get("time-in-tempo")

        self.total_time = request.form.get("time")

        self.total_kilometres = int(self.trot_before) + \
            int(self.main_kilometres) + int(self.trot_after)

        self.pace = self.get_pace(
            self.main_kilometres_time, self.main_kilometres)
        self.total_pace = self.get_pace(self.total_time, self.total_kilometres)

    def get_pace(self, time="00:00:00", kilometres="0"):
        time_list = time.split(":")

        if len(time_list) == 2:
            time_list.append("00")

        time_in_minutes = (
            (int(time_list[0]) * 60) + int(time_list[1]) + (int(time_list[2]) / 60)) / float(kilometres)

        list_seconds = str(time_in_minutes).split(".")
        sec = round(float("0." + list_seconds[1]) * 60)

        if sec < 10:
            sec = "0" + str(sec)

        return f"{list_seconds[0]}:{sec}"

    def save(self):
        new_activity = Activity(
            type=self.type, warm_up=self.warm_up, abc=self.abc)
        db.session.add(new_activity)
        db.session.commit()
