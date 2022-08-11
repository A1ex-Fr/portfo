import datetime
import email
import csv
from unicodedata import name
from flask import Flask, redirect, render_template, request, url_for
app = Flask(__name__)


@app.route('/')
def my_home():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


def write_to_db(data):
    with open('database.txt', mode='a') as db:
        name = data.get("name")
        email = data.get("email")
        subject = data.get("subject")
        message = data.get("message")
        date = datetime.date.today()
        file = db.write(f'\n{date}, {name}, {email}, {subject}, {message}')


def write_to_csv_db(data):
    with open('database.csv', mode='a') as csv_db:
        name = data.get("name")
        email = data.get("email")
        subject = data.get("subject")
        message = data.get("message")
        date = datetime.date.today()
        csv_writer = csv.writer(csv_db, delimiter=';',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([date, name, email, subject, message])


@ app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            name = data.get("name")
            write_to_csv_db(data)
            return redirect(url_for('thankyou', name=name))
        except:
            return 'ERROR: did not save in Database!!!!!'
    else:
        return 'something went wrong pleas submit the form one more time'


@ app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')


if __name__ == '__main__':
    app.run(debug=True)
