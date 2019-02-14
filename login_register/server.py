from flask import Flask, render_template, redirect, request, session
from flask_bcrypt import Bcrypt
from mysqlconnection import connectToMySQL




app = Flask(__name__)
app.secret_key="I solemly swear I am upto no good"
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    
    return render_template("index.html")
            


@app.route("/success")
def show_users():
    if 'email' not in session:
        return redirect("/")

    return render_template("success.html")

@app.route("/register", methods=["POST"])
def register():


    data={
        'fn': request.form['fname'],
        'ln': request.form['lname'],
        'em': request.form['email'],
        'p1': request.form['pass1'],
        'p2': request.form['pass2']
    }

    p1_hash= bcrypt.generate_password_hash(data['p1'])
    p2_hash= bcrypt.generate_password_hash(data['p2'])
    print(p1_hash)
    print(p2_hash)
    if data['p1'] == data['p2']:
        data['pass']=p1_hash
    mysql = connectToMySQL("login_register")
    query = "INSERT INTO users (first_name,last_name,email,password,created_on,updated_on) VALUES (%(fn)s, %(ln)s,%(em)s,%(pass)s,now(),now());"
    result = mysql.query_db(query,data)
    if(result):
        session['email'] = data['em']
        return redirect("/success")

    print('reg error')
    return redirect('/')


@app.route("/login", methods=["POST"])
def login():
    print(request.form)
    mysql = connectToMySQL("login_register")
    data = {
        'em': request.form['email'],
        'p1': request.form['pass1']
    }
    
    query = "SELECT * FROM users WHERE email = %(em)s;"
    
    result = mysql.query_db(query, data)    
    print(result)
    if result:
        
        p2_hash = result[0]['password']
        
        print(p2_hash)
        if bcrypt.check_password_hash(result[0]['password'], data['p1']):
            
            session['email'] = result[0]['email']
            return redirect('/success')

    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()

    return redirect('/')

if __name__ == "__main__":
    app.run(host='10.1.1.192',debug=True)