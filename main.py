import numpy as np
from flask import Flask, redirect, render_template, request, url_for
import pickle

app = Flask(__name__, template_folder='templates')

model = pickle.load(open('model.pkl', 'rb'))


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/healthcheck")
def healthcheck():
    # if request.method == "POST":
    #     age = request.form["age"]
    #     # height = request.form["height"]
    #     # weight = request.form["weight"]
    #     # count = request.form["count"]
    #     return redirect('/result')
    # else:
    return render_template('healthcheck.html')


@app.route("/result", methods=['GET', 'POST'])
def result():
    if request.method == "POST":
        age = request.form["age"]
        height = request.form["height"]
        weight = request.form["weight"]
        specs = request.form["specs"]
        gender = request.form["gender"]

        BMI = (int(weight) * 2.2) * 703 / ((float(height) * 12) ** 2)

        count = request.form["count"]
        screentime = request.form["screentime"]

        final = np.array([[age, screentime, count, BMI, gender, specs]])
        prediction = model.predict(final)
        WeightCategory = ""
        if BMI <= 18.5:
            WeightCategory = 'Underweight'
        elif 18.5 < BMI <= 24.9:
            WeightCategory = 'Normal'
        elif 24.9 < BMI > 29.9:
            WeightCategory = 'Overweight'

        if prediction[0] == 0:
            return render_template('result.html', prediction=prediction[0], weight=weight, BMI=round(BMI, 2),
                                   height=height, screentime=int(screentime), count=count, category=WeightCategory)
        else:
            return render_template('result.html', prediction=prediction[0], weight=weight, BMI=round(BMI, 2),
                                   height=height,
                                   screentime=int(screentime), count=count, category=WeightCategory)
    else:
        return render_template('result.html')


@app.route('/predict')
def predict():
    # age = request.form['age']
    # weight = request.form['weight']
    # height = request.form['height']
    # time = request.form['time']
    # steps = request.form['steps']
    # bmi = request.form['bmi']
    # gender = request.form['gender']
    # spect = request.form['spect']

    #
    final = np.array([[21, 9, 1003, 58.456637, 1, 1]])
    prediction = model.predict(final)
    # output = '{0:{1}f}'.format(prediction[0][1], 2)
    if prediction[0] == 0:
        return "<h1>Person is NOT healthy</h1>"

    else:

        return "<h1>Person is healthy</h1>"


app.run(debug=True)
