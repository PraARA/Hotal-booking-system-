from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,migrate
from datetime import datetime

app = Flask(__name__)

app.debug = True


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)


class User (db.Model):
    id =db.Column(db.Integer, primary_key=True)
    email =db.Column(db.String(20), unique=False, nullable=False)
    password =db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"email :{self.email}, password : {self.password}"

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(10), nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    aadhar_number = db.Column(db.String(12), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)

    def _repr_(self):
        return f"Guest {self.first_name} {self.last_name}, Room: {self.room_number}"


@app.route('/db')
def index():
    users = User.query.all()
    print(users)
    return render_template('home.html', users=users)


@app.route('/favourites')
def favourites():
    return render_template('favourites.html')

@app.route('/EN')
def EN():
    return render_template('EN.html')

# @app.route('/language')
# def lan():
#     return render_template('lan.html')

@app.route('/insert')
def login():
    return render_template('login.html')

@app.route('/checkprice')
def checkprice():
    return render_template('checkprice.html')

@app.route('/')
def interface():
    return render_template('interface.html')

@app.route('/insert' , methods=["POST", "GET"])
def users():
    if request.method == "POST":
        email = request.form.get("em")
        password = request.form.get("ps")
        

        if email != '' and password != '':
            p = User(email = email , password = password)
            db.session.add(p)
            db.session.commit()
            return redirect('/')
        else:
            return redirect('/')
    else:
        return render_template('login.html')


@app.route('/delete1/<int:id>')
def erase(id):
    data = User.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')

@app.route('/')
def Rhome():
    guests = Guest.query.all()  # Fetch all guests from the database
    return render_template('Rhome.html', guests=guests)

# Add guest route to handle form submission
@app.route('/add', methods=['GET', 'POST'])
def add_guest():
    if request.method == 'POST':
        # Get data from the form
        room_number = request.form['room_number']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        aadhar_number = request.form['aadhar_number']
        phone_number = request.form['phone_number']
        check_in_date = datetime.strptime(request.form['check_in_date'], '%Y-%m-%d')
        check_out_date = datetime.strptime(request.form['check_out_date'], '%Y-%m-%d')
        
        # Create a new Guest object
        if room_number and first_name and last_name and aadhar_number and phone_number:
            new_guest = Guest(room_number=room_number, first_name=first_name, last_name=last_name,
                              aadhar_number=aadhar_number, phone_number=phone_number,
                              check_in_date=check_in_date, check_out_date=check_out_date)
            # Add to the database
            db.session.add(new_guest)
            db.session.commit()
            return redirect(url_for('Rhome'))
        else:
            return "Please fill out all fields."

    return render_template('addGuest.html')

# Delete guest route
@app.route('/delete2/<int:guest_id>', methods=['GET'])
def delete_guest(guest_id):
    guest = Guest.query.get_or_404(guest_id)
    db.session.delete(guest)
    db.session.commit()
    return redirect(url_for('Rhome'))

@app.route('/addGuest')
def addGuest():
    return render_template('/addGuest.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
