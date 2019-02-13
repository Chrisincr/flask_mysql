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

@app.route("/users/new")
def newuser():
    return render_template("new_user.html")

@app.route("/users/<num>/edit")
def edit_user(num):

    mysql = connectToMySQL("flask2")

    query = mysql.query_db("SELECT * FROM friends WHERE id="+str(num)+";")
    print(query)
    
    return render_template("update_user.html", friend = query)
@app.route("/update", methods=['POST'])
def update():
    mysql = connectToMySQL("flask2")
    query = mysql.query_db("UPDATE friends SET first_name =\'"+request.form['fname']+"\',last_name =\'"+request.form['lname']+"\',email =\'"+request.form['email']+"\',updated_at = now()  WHERE id="+request.form['id']+";")
    return redirect("/")

@app.route("/users/<num>/delete")
def delete(num):
    mysql = connectToMySQL("flask2")
    query = mysql.query_db("DELETE FROM friends WHERE id=\'"+num+"\';")
    return redirect("/")

@app.route("/users/create", methods=["POST"])
def create():
    mysql = connectToMySQL("flask2")
    query = "INSERT INTO friends (first_name,last_name,email, created_at, updated_at) VALUES (%(fn)s, %(ln)s,%(em)s, NOW(), NOW());"
    data = {
        "fn": request.form["fname"],
        "ln": request.form["lname"],
        "em": request.form["email"]
    }
    new_friend_id = mysql.query_db(query,data)
    return redirect('/users/'+str(new_friend_id))

if __name__ == "__main__":
    app.run(debug=True)