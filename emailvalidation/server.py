from flask import Flask, render_template, redirect, request,session,flash
from mysqlconnection import connectToMySQL
import re    
app = Flask(__name__)
app.secret_key = "I solemly swear I am upto no good"

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



@app.route("/")
def index():
    if 'email' not in session:
        session['email'] = None
    
    

    return render_template("index.html",email = session['email'])

            


@app.route("/process", methods=["POST"])
def validate():
    
    if not EMAIL_REGEX.match(request.form['email']):    # test whether a field matches the pattern
        flash("Invalid email address!")
        session['email'] = request.form['email']
    
    if not '_flashes' in session.keys():
        session['email'] = request.form['email']
        flash("Email "+str(session['email']+" successfully added!"))

        mysql = connectToMySQL("email_validation")
        emailid = mysql.query_db("INSERT INTO emails(email,created_at) VALUES (\'"+request.form['email']+"\', NOW());")
        return redirect("/result")
    return redirect("/")

@app.route("/result")
def result():
    
    session.clear()

    mysql = connectToMySQL("email_validation")
    emails = mysql.query_db("SELECT * FROM emails")

    return render_template("result.html",emails = emails)



if __name__ == "__main__":
    app.run(debug=True)




