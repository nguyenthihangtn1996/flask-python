from flask import Flask, render_template
import requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG']= True

@app.route("/")
def index():
    url = 'https://samples.openweathermap.org/data/2.5/forecast?q=M%C3%BCnchen,DE&appid=b6907d289e10d714a6e88b30761fae22'
    city = 'Las Vegas'

    r = requests.get(url.format(city)).json()

    weather = {
            'city' : city,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }
    print(weather)

    return render_template('weather.html')

if __name__ == "__main__":
    app.run(debug=True)