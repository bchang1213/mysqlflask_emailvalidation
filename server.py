from flask import Flask, render_template, redirect, request, session, flash
# import the Connector function
from mysqlconnection import MySQLConnector
import re
# create a regular expression object that we can use run operations on
app=Flask(__name__)
app.secret_key = 'super secret key'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# connect and store the connection in "mysql"
# note that you pass the database name to the function
mysql=MySQLConnector(app,'fullfriends')

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/post', methods=["POST"])
def send_data():
	if len(request.form['email']) < 1:
		flash("Email cannot be blank!")
		return redirect("/")
	elif not EMAIL_REGEX.match(request.form['email']):
		flash("Invalid Email Address!")
		return redirect("/")
	else:
		query = "INSERT INTO emails (email_address, date_created) VALUES (:email, NOW())"
		data = {
			'email': request.form['email']
		}
		mysql.query_db(query, data)
		return redirect("/success")

@app.route('/success')
def list():
	flash("The email you entered is valid!")
	query = "SELECT emails.email_address, DATE_FORMAT(emails.date_created, ('%M %d %Y')) AS date, DATE_FORMAT(emails.date_created, '%H %i') AS time, emails.id FROM emails"
	emails = mysql.query_db(query)
	return render_template("success.html", all_emails=emails)

@app.route('/success/<user_id>/delete', methods=["POST"])
def delete(user_id):
	data = {
	'some_id': user_id
	}
	flash("Email and entry deleted.")
	query = "DELETE FROM emails WHERE emails.id = :some_id"
	mysql.query_db(query, data)
	return redirect("/success")

app.run(debug=True)