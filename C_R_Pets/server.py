from flask import Flask, render_template, redirect, request
from mysqlconnection import connectToMySQL    
app = Flask(__name__)
@app.route("/")
def index():
    mysql = connectToMySQL('first_flask')	        
    pets = mysql.query_db('SELECT * FROM pets;')  
    print(pets)
    return render_template("index.html", all_pets = pets)
            


@app.route("/create_pet", methods=["POST"])
def add_pet_to_db():
    mysql = connectToMySQL("first_flask")

    query = "INSERT INTO pets (name, type, created_at, updated_at) VALUES (%(fn)s, %(tp)s, NOW(), NOW());"
    data = {
        "fn": request.form["name"],
        "tp": request.form["type"],
    }
    new_pet_id = mysql.query_db(query,data)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)