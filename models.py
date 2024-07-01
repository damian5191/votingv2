from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phrase = db.Column(db.String(255), nullable=False)
    normalized_phrase = db.Column(db.String(255), nullable=False)
    player_id = db.Column(db.String(36), nullable=False)
    has_submitted = db.Column(db.Boolean, default=False)

    def __init__(self, phrase, normalized_phrase, player_id):
        self.phrase = phrase
        self.normalized_phrase = normalized_phrase
        self.player_id = player_id
        self.has_submitted = False
