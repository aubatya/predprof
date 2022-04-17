from app import db


class Det(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x_coor = db.Column(db.Float, nullable=False)
    y_coor = db.Column(db.Float, nullable=False)
    

    def __init__(self, id, x, y) -> None:
        self.id, self.x_coor, self.y_coor= (
            id,
            x,
            y
        )

    def __repr__(self) -> str:
        return f"{self.id}"

class Anom(db.Model):
    id = db.Column(db.String, primary_key=True)
    x_coor = db.Column(db.Float, nullable=False)
    y_coor = db.Column(db.Float, nullable=False)
    inten = db.Column(db.Float, nullable=False)

    def __init__(self, id, x, y, i) -> None:
        self.id, self.x_coor, self.y_coor, self.inten= (
            id,
            x,
            y,
            i
        )

    def __repr__(self) -> str:
        return f"{self.id}"


db.create_all()
