from flask_sqlalchemy import SQLAlchemy

# Assuming you have already initialized the Flask app and configured SQLAlchemy
db = SQLAlchemy()

class Faq(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Faq(id={self.id}, question='{self.question}', answer='{self.answer}')"
