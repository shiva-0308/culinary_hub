
from flask import Flask, render_template, redirect, url_for, request, jsonify, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from datetime import datetime
import secrets
import sqlite3
import logging
import smtplib
from sqlalchemy import and_
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import random
import string

# Configure logging
logging.basicConfig(filename='server_logs.txt', level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Set the secret key here
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modific
db = SQLAlchemy(app)


# Function to generate a random OTP
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

# Function to send OTP via email
def send_otp_email(email, otp):
    sender_email = "mail2userfromculinaryhub@gmail.com"
    password = "xfsw cnyn ldwf tqec"

    message = MIMEText(f'Your OTP is: {otp}')
    message['Subject'] = 'Login OTP'
    message['From'] = sender_email
    message['To'] = email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.send_message(message)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
    




# Import the Faq model
from models  import Faq


# Define User and UserRequirements models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    mobile = db.Column(db.Integer, nullable=False)
    whatsapp = db.Column(db.Integer, nullable=False)  # Add WhatsApp field
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class user_requirements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    button_value = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    mobile = db.Column(db.Integer, nullable=False)
    whatsapp = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', backref=db.backref('user_requirements', lazy=True))


# Define the schema for storing button values along with user details
class ButtonClick(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    button_value = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('button_clicks', lazy=True))
    user_name = db.Column(db.String(30), nullable=False)
    user_mobile = db.Column(db.Integer, nullable=False)
    user_whatsapp = db.Column(db.Integer, nullable=False)



class venue_booking_query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    seating_capacity = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    mobile = db.Column(db.Integer, nullable=False)
    whatsapp = db.Column(db.Integer, nullable=False)
    user = db.relationship('User', backref=db.backref('venue_booking_query', lazy=True))


# Define the Venue model
class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    availability = db.Column(db.String(8), nullable=False)
    function_hall_name = db.Column(db.String, nullable=False,unique=True)
    address = db.Column(db.String(300), nullable=False)
    manager_name = db.Column(db.String, nullable=False)
    contact_number = db.Column(db.Integer, nullable=False,unique=True)
    whatsapp_number = db.Column(db.Integer, nullable=False)
    seating_capacity = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(6), nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    amenities = db.Column(db.String, nullable=False)

    # Add CheckConstraints
    __table_args__ = (
        CheckConstraint("availability IN ('available', 'booked')"),
        CheckConstraint("LENGTH(contact_number) = 10"),
        CheckConstraint("LENGTH(whatsapp_number) = 10"),
        CheckConstraint("type IN ('ac', 'non ac')")
    )



# Define the Registrations model
class Registrations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    mobile = db.Column(db.String(10), nullable=False)
    whatsapp = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    current_occupation = db.Column(db.String(100), nullable=False)
    languages = db.Column(db.String(100))
    experience = db.Column(db.Integer)
    cuisines = db.Column(db.String(100))
    preferred_location = db.Column(db.String(100))
    interested_occupation = db.Column(db.String(100))
    other_occupation = db.Column(db.String(100))


# Define Event model for storing event management form submissions
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    mobile = db.Column(db.Integer, nullable=False)
    event_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(100), nullable=False)
    event_type = db.Column(db.String(100), nullable=False)
    other_event_type = db.Column(db.String(100))
    venue_preferences = db.Column(db.String(100), nullable=False)
    entertainment_preferences = db.Column(db.String(100))
    activities_preferences = db.Column(db.String(100))
    theme = db.Column(db.String(100))
    decor_preferences = db.Column(db.String(100))
    lighting_requirements = db.Column(db.String(100))
    stage_setup = db.Column(db.String(100))
    deadlines = db.Column(db.String(100))
    schedule = db.Column(db.String(100))
    additional_services = db.Column(db.String(100))
    transportation_needs = db.Column(db.String(100))
    accommodation_requirements = db.Column(db.String(100))


class GroceryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

class GroceryOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    whatsapp = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    delivery_datetime = db.Column(db.DateTime, nullable=False)
    order_review = db.Column(db.Text, nullable=False) 
# ... (other imports & setup from above)
    

# Define Workshop model
class Workshop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(12), nullable=False)  # Changed to String to accommodate formatting
    whatsapp = db.Column(db.String(12), nullable=False)  # Changed to String to accommodate formatting
    cuisine = db.Column(db.String(50), nullable=False)
    
    # Include name, mobile, and whatsapp from User table
    user_name = db.Column(db.String(30), nullable=False)
    user_mobile = db.Column(db.String(12), nullable=False)
    user_whatsapp = db.Column(db.String(12), nullable=False)


# Define the Booking model
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('bookings', lazy=True))
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    contact = db.Column(db.String(10), nullable=False)
    whatsapp = db.Column(db.String(10), nullable=False)
    delivery_type = db.Column(db.String(100), nullable=False)
    schedule = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text, nullable=True)
    cooked_type = db.Column(db.String(100), nullable=False)
    
    # Additional fields from User model
    user_name = db.Column(db.String(30), nullable=False)
    user_mobile = db.Column(db.Integer, nullable=False)
    user_whatsapp = db.Column(db.Integer, nullable=False)


# Event listener function for sending notifications
def notify_on_new_entry(mapper, connection, target):
    try:
        # Connect to SMTP server
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login("mail2userfromculinaryhub@gmail.com", "xfsw cnyn ldwf tqec")
            
            # Construct email message
            msg = MIMEMultipart()
            msg['From'] = "mail2userfromculinaryhub@gmail.com"
            msg['To'] = "culinaryhubbackenddb@gmail.com"
            msg['Subject'] = "New entry added to database"
            
            # Extract entry details and table name
            table_name = target.__tablename__
            entry_details = '\n'.join(f"{column.name}: {getattr(target, column.name)}" for column in target.__table__.columns)
            
            # Construct email body
            body = f"A new entry has been added to the {table_name} table:\n\n{entry_details}"
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server.send_message(msg)
    except Exception as e:
        print(f"Error sending notification email: {e}")

# Attach event listeners to all tables
tables = [User, user_requirements, Registrations, Event,venue_booking_query,Booking, Workshop,GroceryOrder, ButtonClick]
for table in tables:
    db.event.listen(table, 'after_insert', notify_on_new_entry)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        whatsapp = request.form['whatsapp']  # Add WhatsApp field
        email = request.form['email']  # Add email field
        password = request.form['password']
        # Check if the mobile number already exists in the database
        existing_user = User.query.filter_by(mobile=mobile).first()
        if existing_user:
            flash('User already exists. Please log in.')
            return redirect(url_for('login'))

        new_user = User(name=name, mobile=mobile, whatsapp=whatsapp, email=email, password=password)  # Update user creation with new fields
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('landing'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    # Check if the user has exceeded the maximum login attempts
    if 'login_attempts' not in session:
        session['login_attempts'] = 0

    if request.method == 'POST':
        # Handle login form submission
        mobile = request.form['mobile']
        password = request.form['password']
        user = User.query.filter_by(mobile=mobile, password=password).first()
        if user:
            session['user_id'] = user.id
            # Reset login attempts upon successful login
            session['login_attempts'] = 0
            return redirect(url_for('landing'))
        else:
            # Increment login attempts upon failed login
            session['login_attempts'] += 1
            if session['login_attempts'] == 1 or session['login_attempts'] == 2:
                flash("Invalid mobile number or password. Please try again.", "error")  # Flash message for invalid credentials
                return redirect(url_for('login'))  # Redirect to login page itself
            elif session['login_attempts'] >= 3:
                flash("No user found. Please sign up.", "error")  # Flash message for exceeding attempts
                return redirect(url_for('signup'))

    else:
        # Render the login form
        return render_template('login.html')


@app.route('/verify_email', methods=['POST'])
def verify_email():
   
    email = request.form['email']
    
    # Check if the email exists in the database
    user = User.query.filter_by(email=email).first()
    
    if user:
        # Generate and send OTP
        otp = generate_otp()
        if send_otp_email(user.email, otp):
            session['otp'] = otp
            session['email'] = email
            flash("OTP sent to your email. Please check and enter.", "info")
            return redirect(url_for('verify_otp'))
        else:
            flash("Error sending OTP. Please try again later.", "error")
            return redirect(url_for('login'))
    else:
        flash("Email not found. Please try again or sign up.", "error")
        return redirect(url_for('login'))

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():

    app.logger.info(f"Session variables: {session}")

    if 'otp' not in session or 'email' not in session:
        flash("OTP session expired. Please try again.", "error")
        return redirect(url_for('login'))

    if request.method == 'POST':
        otp = request.form['otp']
        if otp == session['otp']:
            session.pop('otp')
            session.pop('email')
            return redirect(url_for('landing'))
        else:
            flash("Invalid OTP. Please try again.", "error")
            return redirect(url_for('verify_otp'))

    return render_template('verify_otp.html')

@app.route('/button_clicked', methods=['POST'])
def button_clicked():
    button_value = request.json.get('button_value')

    # Retrieve user details based on session user ID
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            # Store the button value and user details in the database
            button_click = ButtonClick(
                button_value=button_value,
                user_id=user.id,
                user_name=user.name,
                user_mobile=user.mobile,
                user_whatsapp=user.whatsapp
            )
            db.session.add(button_click)
            db.session.commit()

            # Redirect to the respective URL based on the button value
            if button_value == 'book_chef':
                return redirect(url_for('book_chef'))
            elif button_value == 'event_management':
                return redirect(url_for('event_management'))
            elif button_value == 'store':
                return redirect(url_for('store'))
            elif button_value == 'workshops':
                return redirect(url_for('workshops'))
            elif button_value == 'faqs':
                return redirect(url_for('faqs'))
            elif button_value == 'book_functionhall':
                return redirect(url_for('book_functionhall'))
            elif button_value == 'staff':
                return redirect(url_for('staff'))
            elif button_value == 'groceries':
                return redirect(url_for('groceries'))
            else:
                return "Button value not recognized"
        else:
            return "User not found"
    else:
        return "User ID not found in session"


@app.route('/landing')
def landing():
    # Check if user is logged in or signed up successfully
    # For demonstration, let's assume user is logged in or signed up
    return render_template('landing.html')


@app.route('/book_chef')
def book_chef():
    return render_template('book_a_chef.html')

@app.route('/store_data', methods=['POST'])
def store_data():
    if request.method == 'POST':
        # Check if user is logged in
        if 'user_id' not in session:
            flash('User not logged in.')
            return redirect(url_for('login'))

        # Get user details from User table
        user = User.query.get(session['user_id'])
        if not user:
            flash('User not found.')
            return redirect(url_for('login'))

        # Extract button value from request payload
        # Extract button value from request payload
        button_value = request.json.get('value')

        # Save button data along with user information
        new_button_data = user_requirements(
            user_id=user.id,
            button_value=button_value,
            name=user.name,
            mobile=user.mobile,
            whatsapp=user.whatsapp
        )
        db.session.add(new_button_data)
        db.session.commit()

        return jsonify({'message': 'Data stored successfully', 'success': True})

@app.route('/joinus', methods=['GET', 'POST'])
def join_us():
    if request.method == 'POST':
        try:
            # Extract data from the form submission
            name = request.form['name']
            mobile = request.form['mobile']
            whatsapp = request.form['whatsapp']
            age = request.form['age']
            location = request.form['location']
            current_occupation = request.form['current_occupation']
            languages = request.form['languages']
            experience = request.form['experience']
            cuisines = request.form['cuisines']
            preferred_location = request.form['preferred_location']
            interested_occupation = request.form['interested_occupation']
            other_occupation = request.form.get('other_occupation', None)

            # Insert the data into the registrations table
            new_registration = Registrations(
                name=name,
                mobile=mobile,
                whatsapp=whatsapp,
                age=age,
                location=location,
                current_occupation=current_occupation,
                languages=languages,
                experience=experience,
                cuisines=cuisines,
                preferred_location=preferred_location,
                interested_occupation=interested_occupation,
                other_occupation=other_occupation
            )
            db.session.add(new_registration)
            db.session.commit()

            return jsonify({'success': True}), 200
        except Exception as e:
            db.session.rollback()
            print("Error:", str(e))  # Print the error message to the console for debugging
            return jsonify({'error': str(e)}), 500
    else:
        return render_template('joinus.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Extract data from the form submission
        name = request.form['name']
        mobile = request.form['mobile']
        age = request.form['age']
        location = request.form['location']
        languages = request.form.get('languages', '')
        experience = request.form.get('experience', '')
        cuisines = request.form.get('cuisines', '')

        # Insert the data into the registrations table
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO registrations 
                          (name, mobile, age, location, languages, experience, cuisines) 
                          VALUES (?, ?, ?, ?, ?, ?, ?)''',
                       (name, mobile, age, location, languages, experience, cuisines))
        conn.commit()
        conn.close()

        return jsonify({'message': 'Registration successful! Our team will contact you soon.'}), 200
    except Exception as e:
        # Log the exception
        logging.error(f"Error occurred in submit route: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/eventmanagement', methods=['GET', 'POST'])
def event_management():
    if request.method == 'POST':
        # Check if user is logged in
        if 'user_id' not in session:
            flash('User not logged in.')
            return redirect(url_for('login'))

        # Get user details from User table
        user = User.query.get(session['user_id'])
        if not user:
            flash('User not found.')
            return redirect(url_for('login'))

        # Handle form submission
        event_name = request.form['eventName']
        date = request.form['date']
        location = request.form['location']
        duration = request.form['duration']
        event_type = request.form['eventType']
        other_event_type = request.form.get('otherEventType', '')
        venue_preferences = request.form['venuePreferences']
        entertainment_preferences = request.form.get('entertainmentPreferences', '')
        activities_preferences = request.form.get('activitiesPreferences', '')
        theme = request.form.get('theme', '')
        decor_preferences = request.form.get('decorPreferences', '')
        lighting_requirements = request.form.get('lightingRequirements', '')
        stage_setup = request.form.get('stageSetup', '')
        deadlines = request.form.get('deadlines', '')
        schedule = request.form.get('schedule', '')
        additional_services = request.form.get('additionalServices', '')
        transportation_needs = request.form.get('transportationNeeds', '')
        accommodation_requirements = request.form.get('accommodationRequirements', '')

        # Create a new Event object and add user details
        new_event = Event(
            user_id=user.id,
            name=user.name,
            mobile=user.mobile,
            event_name=event_name,
            date=date,
            location=location,
            duration=duration,
            event_type=event_type,
            other_event_type=other_event_type,
            venue_preferences=venue_preferences,
            entertainment_preferences=entertainment_preferences,
            activities_preferences=activities_preferences,
            theme=theme,
            decor_preferences=decor_preferences,
            lighting_requirements=lighting_requirements,
            stage_setup=stage_setup,
            deadlines=deadlines,
            schedule=schedule,
            additional_services=additional_services,
            transportation_needs=transportation_needs,
            accommodation_requirements=accommodation_requirements
        )
        db.session.add(new_event)
        db.session.commit()

        flash('Event details submitted successfully!', 'success')
        return redirect(url_for('event_management'))

    return render_template('eventmanagement.html')

@app.route('/store')
def store():
    return render_template('store.html')


@app.route('/workshops')
def workshops():
    # Your code to handle the workshops route goes here
    return render_template('workshops.html')


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        whatsapp = request.form['whatsapp']
        cuisine = request.form['cuisine']

        # Retrieve user ID from session
        user_id = session.get('user_id')

        # Retrieve user details from User table based on user ID
        user = User.query.filter_by(id=user_id).first()

        if user:
            # Save form data to the Workshop table
            workshop = Workshop(user_id=user_id, name=name, email=email, phone=phone, whatsapp=whatsapp, cuisine=cuisine,
                                user_name=user.name, user_mobile=user.mobile, user_whatsapp=user.whatsapp)
            db.session.add(workshop)
            db.session.commit()
            
        # Return success response
        response = {'message': 'Registration successful! Our team will reach you as soon as possible.'}
        return jsonify(response), 200
    else:
        return 'Method not allowed'








# Define routes and views
@app.route('/FAQs')
def faqs():
    return render_template('faqs.html', faqs=faqs)


@app.route('/book_functionhall')
def book_functionhall():
    return render_template('venue.html')

@app.route('/search_venues', methods=['POST'])
def search_venues():
    if request.method == 'POST':
        # Check if user is logged in
        if 'user_id' not in session:
            flash('User not logged in.')
            return redirect(url_for('login'))

        # Get user details from User table
        user = User.query.get(session['user_id'])
        if not user:
            flash('User not found.')
            return redirect(url_for('login'))


    budget = int(request.form['budget'])
    location = request.form['location']
    seating_capacity = int(request.form['seating_capacity'])
    type = request.form['type']
    
    
    user = User.query.get(session['user_id'])
    name = user.name
    mobile = user.mobile
    whatsapp = user.whatsapp
    
    # Create a new UserPreferences instance and save it to the database
    user_preferences =venue_booking_query( user_id=user.id,budget=budget, location=location, seating_capacity=seating_capacity, type=type,name=name,mobile=mobile,whatsapp=whatsapp)
    db.session.add(user_preferences)
    db.session.commit()


    # Define range for budget and seating capacity
    budget_range = (budget * 0.1)  # 10% range
    seating_capacity_range = int(seating_capacity * 0.1)  # 10% range

    # Retrieve venues matching user preferences and within the budget and seating capacity range
    matching_venues = Venue.query.filter(
        and_(
            Venue.budget >= budget - budget_range,
            Venue.budget <= budget + budget_range,
            Venue.address.ilike(f'%{location}%'),
            Venue.seating_capacity >= seating_capacity - seating_capacity_range,
            Venue.seating_capacity <= seating_capacity + seating_capacity_range,
            Venue.type.ilike(f'%{type}%')
        )
    ).all()

    return render_template('search_results.html', venues=matching_venues, user_preferences=request.form)
@app.route('/staff')
def staff():
    return render_template('add_venue.html')

# Route to handle form submission and add or update venue in the database
@app.route('/add_venue', methods=['POST'])
def add_venue():
 
    # Get data from the form
    availability = request.form['availability']
    function_hall_name = request.form['function_hall_name']
    address = request.form['address']
    manager_name = request.form['manager_name']
    contact_number = request.form['contact_number']
    whatsapp_number = request.form['whatsapp_number']
    seating_capacity = int(request.form['seating_capacity'])
    type = request.form['type']
    budget = int(request.form['budget'])
    amenities = request.form['amenities']

    # Check if the venue already exists based on function_hall_name
    existing_venue = Venue.query.filter_by(function_hall_name=function_hall_name).first()
    
    if existing_venue:
            # Update the existing venue
            existing_venue.availability = availability
            existing_venue.address = address
            existing_venue.manager_name = manager_name
            existing_venue.contact_number = contact_number
            existing_venue.whatsapp_number = whatsapp_number
            existing_venue.seating_capacity = seating_capacity
            existing_venue.type = type
            existing_venue.budget = budget
            existing_venue.amenities = amenities
            db.session.commit()
            return 'Venue updated successfully'
       



    # Create a new Venue instance
    new_venue = Venue(availability=availability, function_hall_name=function_hall_name, address=address,
                      manager_name=manager_name, contact_number=contact_number, whatsapp_number=whatsapp_number,
                      seating_capacity=seating_capacity, type=type, budget=budget, amenities=amenities)

    # Add the new venue to the database
    db.session.add(new_venue)
    db.session.commit()

    return 'Venue added successfully'
 
@app.route('/groceries')  # Define the route for groceries.html
def groceries():
    return render_template('groceries.html')

@app.route('/get_grocery_items')
def get_grocery_items():
    items = GroceryItem.query.all()
    return jsonify([item.name for item in items])

@app.route('/add_grocery_item', methods=['POST'])
def add_grocery_item():
    item_name = request.form.get('itemName')
    if item_name:
        existing_item = GroceryItem.query.filter_by(name=item_name).first()
        if not existing_item:  # Add only if item doesn't exist 
            new_item = GroceryItem(name=item_name)
            db.session.add(new_item)
            db.session.commit()
        return 'Item added or existed' 
    else:
        return 'Error: Missing item name', 400

@app.route('/submit_order', methods=['POST'])
def submit_order():
    required_fields = ['name', 'mobile', 'whatsapp', 'address', 'delivery-date', 'orderReview']
    for field in required_fields:
        if field not in request.form:
            return f"Missing field: {field}.", 400

    try:
        new_order = GroceryOrder(
            name=request.form['name'],
            mobile=request.form['mobile'],
            whatsapp=request.form['whatsapp'],
            address=request.form['address'],
            delivery_datetime=datetime.strptime(request.form['delivery-date'], '%Y-%m-%dT%H:%M'),
            order_review=request.form['orderReview']
        )

        print("Order object:", new_order)              # Inspect the order data
        db.session.add(new_order)  
        print("Added order to session")              # Check if added successfully
        db.session.commit()                         # Attempt to commit changes
        print("Committed changes")                   # Check if commit succeeded

        raise Exception("Forced Test Exception")     # TEMPORARY: Force an error to test commit behavior

    except Exception as e: 
        db.session.rollback()                       # Rollback any changes in case of errors
        print(f"Error during submission: {e}") 
        return f'Error submitting order: {e}', 500



# Route to render the booking form
@app.route('/dabbawalaservices')
def dabbawala_services():
    # Retrieve user ID from session
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        return render_template('dabbawala.html', user=user)
    else:
        return 'User not logged in'  # Handle if user is not logged in

# Route to handle booking
@app.route('/book', methods=['POST'])
def book():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        address = request.form['address']
        contact = request.form['contact']
        whatsapp = request.form['whatsapp']
        delivery_type = request.form['deliveryType']
        schedule = request.form['schedule']
        instructions = request.form['instructions']
        cooked_type = request.form['cookedType']

        # Retrieve user ID from session
        user_id = session.get('user_id')
        if not user_id:
            return 'User not logged in'  # Handle if user is not logged in

        # Retrieve user data from User table based on user id
        user = User.query.get(user_id)

        # Save form data to the Booking table
        booking = Booking(user=user, name=name, address=address, contact=contact, whatsapp=whatsapp,
                          delivery_type=delivery_type, schedule=schedule, instructions=instructions,
                          cooked_type=cooked_type,
                          user_name=user.name, user_mobile=user.mobile, user_whatsapp=user.whatsapp)
        db.session.add(booking)
        db.session.commit()

        # Return success response
        response = {'message': 'Booking successful! Our team will reach out to you shortly.'}
        return jsonify(response), 200
    else:
       return render_template('dabbawala.html')


if __name__ == '__main__':
    app.debug = True
    with app.app_context():
         db.create_all()
    app.run(debug=True)



