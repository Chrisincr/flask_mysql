from flask import Flask, render_template, redirect, request,session,flash
from mysqlconnection import connectToMySQL    
app = Flask(__name__)
app.secret_key = "I solemly swear I am upto no good"
@app.route("/")
def index():
    session['survey'] = None
    mysql = connectToMySQL("dojo_survey")

    languages = mysql.query_db("SELECT * FROM languages;")

    mysql = connectToMySQL("dojo_survey")

    locations = mysql.query_db("SELECT * FROM locations;")
    

    return render_template("index.html", languages = languages, locations = locations)

            


@app.route("/submit", methods=["POST"])
def show_users():
    if len(request.form['name']) < 1:
    	flash("Please enter a name")
    if len(request.form['comment']) > 120:
    	flash("Please limit comment to 120 characters")
    
    if not '_flashes' in session.keys():
        flash("Friend successfully added!")
        mysql = connectToMySQL("dojo_survey")
        ninjaid = mysql.query_db("INSERT INTO ninjas(name) VALUES (\'"+request.form['name']+"\');")
        mysql = connectToMySQL("dojo_survey")
        surveyid =mysql.query_db("INSERT INTO surveys(comment, languages_id, locations_id, ninjas_id) VALUES (\'"+request.form['comment']+"\', "+request.form['languages']+", "+request.form['location']+", "+str(ninjaid)+");")
        session['survey'] = surveyid
        return redirect("/result")
    return redirect("/")

@app.route("/result")
def result():
    mysql = connectToMySQL("dojo_survey")
    survey = mysql.query_db("SELECT surveys.comment, languages.name as langname, locations.name as locname, ninjas.name FROM surveys Join languages on surveys.languages_id = languages.id Join locations on surveys.locations_id = locations.id join ninjas on surveys.ninjas_id = ninjas.id WHERE surveys.id ="+str(session['survey'])+";")

    
    return render_template("result.html", survey = survey)



if __name__ == "__main__":
    app.run(debug=True)




