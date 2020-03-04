from .shared import db

class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    handle = db.Column(db.String(50))
    openness = db.Column(db.Integer)
    conscientiousness = db.Column(db.Integer)
    extraversion = db.Column(db.Integer)
    agreeableness = db.Column(db.Integer)
    neuroticism = db.Column(db.Integer)
    playlist = db.Column(db.String(255))
    error = db.Column(db.Boolean)
    finished = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return '<Recommendation %s>' % self.handle
