from flask import Flask, render_template, redirect, request, session
from flask_bcrypt import Bcrypt
from mysqlconnection import connectToMySQL




app = Flask(__name__)
app.secret_key="I solemly swear I am upto no good"
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    
    return render_template("index.html")
            


@app.route("/wall")
def show_users():
    if 'email' not in session:
        return redirect("/")

    mysql = connectToMySQL("priv_wall")
    query = "SELECT * FROM users WHERE email <> \'"+session['email']+"\';"

    otherusers = mysql.query_db(query)
    
    mysql = connectToMySQL("priv_wall")
    query = "SELECT messages.id as 'messageid', messages.message_text as 'text', messages.created_at, users.first_name as first_name, users.last_name as last_name FROM messages JOIN users on messages.fk_sender_id = users.id WHERE fk_target_id = "+str(session['id'])+";"

    messages = mysql.query_db(query)
    print(messages)

    return render_template("wall.html",users = otherusers,messages = messages)

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
    mysql = connectToMySQL("priv_wall")
    query = "INSERT INTO users (first_name,last_name,email,password,created_at,updated_at,last_login_at) VALUES (%(fn)s, %(ln)s,%(em)s,%(pass)s,now(),now(),now());"
    result = mysql.query_db(query,data)
    if(result):
        session['email'] = data['em']
        session['fname'] = data['fn']
        session['id'] = result
        
        return redirect("/wall")

    print('reg error')
    return redirect('/')


@app.route("/login", methods=["POST"])
def login():
    print(request.form)
    mysql = connectToMySQL("priv_wall")
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
            session['fname'] = result[0]['first_name']
            session['id'] = result[0]['id']
            
            mysql = connectToMySQL("priv_wall")
            mysql.query_db("UPDATE users SET last_login_at = now() WHERE email =\'"+session['email']+"\';")
            return redirect('/wall')

    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()

    return redirect('/')

@app.route("/sendmessage",methods=["POST"])
def send_route():
    print("****SENDING MESSAGE****")
    print(request.form)

    mysql = connectToMySQL("priv_wall")
    data = {
        'tg': int(request.form['target']),
        'ms': request.form['message']
    }
    print(type(data['tg']))
    query = "INSERT INTO messages (message_text,created_at,fk_sender_id,fk_target_id) VALUES (%(ms)s,now(), "+str(session['id'])+",  %(tg)s)"
    print(query)
    success = mysql.query_db(query,data)

    return redirect('/wall')


@app.route("/badperson")
def hacker():
    session.clear()
    return render_template('badperson.html')

@app.route("/deletemessage",methods=["POST"])
def delete_email():
    print('Deleting')
    print(request.form)
    mysql = connectToMySQL("priv_wall")
    data = {
        'ms': request.form['messageid']
    }
    query="SELECT COUNT(id) FROM messages WHERE id=%(ms)s and fk_target_id = "+str(session['id'])+";"
    count =mysql.query_db(query,data)
    print(count)
    if count[0]['COUNT(id)'] > 0:
        print('passed count check')
        mysql = connectToMySQL("priv_wall")
        query="DELETE FROM messages WHERE id=%(ms)s"
        deleted = mysql.query_db(query,data)
        print('deleted message' +str(data['ms']))

        return redirect('/wall')

    return redirect('/badperson')

if __name__ == "__main__":
    app.run(debug=True)