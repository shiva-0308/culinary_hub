from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secrets.token_hex(32)"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    mobile = db.Column(db.Integer, nullable=False)
    whatsapp = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)


class LandingButton(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    button_value = db.Column(db.String(30), nullable=False)  # Add button value field
    name = db.Column(db.String(30), nullable=False)
    mobile = db.Column(db.Integer, nullable=False)
    whatsapp = db.Column(db.Integer, nullable=False)


@app.route('/')
def home():
    return render_template('landing.html')


@app.route('/submit_button', methods=['POST'])
def submit_button():
    if request.method == 'POST':
        # Check if user is logged in
        if 'user_id' not in session:
            flash('User not logged in.')
            return redirect(url_for('home'))  # Redirect to the home page if user not logged in

        # Get user details from User table
        user = User.query.get(session['user_id'])
        if not user:
            flash('User not found.')
            return redirect(url_for('home'))  # Redirect to the home page if user not found

        # Extract button value from form data
        button_value = request.form['button_value']

        # Save button data along with user information
        new_button_data = LandingButton(
            user_id=user.id,
            button_value=button_value,
            name=user.name,
            mobile=user.mobile,
            whatsapp=user.whatsapp
        )
        db.session.add(new_button_data)
        db.session.commit()

        return redirect(url_for('success'))  # Redirect to the success page after button submission


@app.route('/success')
def success():
    return "Thank you for your submission!"


if __name__ == '__main__':
    app.debug = True
    with app.app_context():
        db.create_all()
    app.run(debug=True)
