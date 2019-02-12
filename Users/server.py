from flask import Flask, render_template, redirect, request
from mysqlconnection import connectToMySQL    
app = Flask(__name__)
@app.route("/")
def index():
    
    return redirect("/users")
            


@app.route("/users")
def show_users():
    mysql = connectToMySQL("flask2")

    query = mysql.query_db("SELECT * FROM friends;")
    
    return render_template("index.html", all_friends = query)


@app.route("/users/<num>")
def show_user(num):
    mysql = connectToMySQL("flask2")

    query = mysql.query_db("SELECT * FROM friends WHERE id="+str(num)+";")
    print(query)
    
    return render_template("showuser.html", friend = query)

@app.route("/users/<num>/edit")
def edit_user(num):

    mysql = connectToMySQL("flask2")

    query = mysql.query_db("SELECT * FROM friends WHERE id="+str(num)+";")
    print(query)
    
    return render_template("update_user.html", friend = query)
@app.route("/update", methods=['POST'])
def update():
    mysql = connectToMySQL("flask2")
    query = mysql.query_db("UPDATE friends SET first_name =\'"+request.form['fname']+"\' WHERE id=1;")
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)