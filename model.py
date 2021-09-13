"""Models for lab pairs."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Cohort(db.Model):
    """A cohort."""
    __tablename__ = "cohorts"

    cohort_id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=True)
    cohort_number = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String, nullable=True)
    nickname = db.Column(db.String, nullable=True)
    start_date = db.Column(db.String, nullable=True)
    end_date = db.Column(db.String, nullable=True)
    json_url = db.Column(db.String, nullable=True)

    # students = a list of Student objects

    def __repr__(self):
        return f"<Cohort cohort_id={self.cohort_id} title={self.title}>"

class Student(db.Model):
    """A student."""

    __tablename__ = "students"

    student_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    tech_level = db.Column(db.Integer, nullable=True)
    cohort_id = db.Column(db.String, db.ForeignKey("cohorts.cohort_id"))
    discord_name = db.Column(db.String, nullable=True)

    cohort = db.relationship('Cohort', backref='students')
    student_pairs = db.relationship('Student', secondary='lab_pairs',
                                    primaryjoin=('Student.student_id==LabPair.user_id'),
                                    secondaryjoin = ('Student.student_id==LabPair.pair_id'))

    def __repr__(self):
        return f"<Student student_id={self.student_id} discord={self.discord_name}>"

class Lab(db.Model):
    """A lab needing pairs."""

    __tablename__ = "labs"

    lab_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Lab lab_id={self.lab_id} title={self.title}>"

class LabPair(db.Model):
    """A lab pair. (middle table)"""

    __tablename__ = "lab_pairs"

    lab_pair_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("students.student_id"))
    pair_id = db.Column(db.Integer, db.ForeignKey("students.student_id"))
    pair_date = db.Column(db.String, nullable=False)
    lab_id = db.Column(db.Integer, db.ForeignKey("labs.lab_id"))
    bad_experience = db.Column(db.Boolean, nullable=True)

    lab = db.relationship('Lab', backref='lab_pairs')
    # student = db.relationship('Student', backref='lab_pair')

    def __repr__(self):
        return f"<LabPair user_id={self.user_id} pair_id={self.pair_id}>"


def connect_to_db(flask_app, db_uri="postgresql:///lab-pairs", echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app, echo=False)
