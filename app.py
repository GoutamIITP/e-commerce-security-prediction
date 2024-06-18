from flask import Flask, render_template, request,url_for
from functions import (load_model, predict_spam, load_credit_model, predict_credit)
from passfunc import (load_vectorizer,load_passmodel, check_password_strength,word_divide_char)  

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("ecommerce.html", spam_prediction=None, error=None)


@app.route("/features")
def features():
    return render_template("features.html", spam_prediction=None, error=None)


@app.route("/teams")
def teams():
    return render_template("team.html", spam_prediction=None, error=None)


@app.route("/creditcard")
def creditcard():
    return render_template("creditcard.html", spam_prediction=None, error=None)


@app.route("/credit_predict", methods=["POST"])
def credit_predict():
    if request.method == "POST":
        card_content = request.form["card_content"]
        try:
            credit_prediction = predict_credit(card_content, load_credit_model())  # Load model once
            return render_template("creditcard.html", credit_prediction=credit_prediction, error=None)
        except Exception as e:
            return render_template("creditcard.html", credit_prediction=None, error=str(e))


@app.route("/email")
def email():
    return render_template("emailspam.html", spam_prediction=None, error=None)


@app.route("/emailpredict", methods=["POST"])
def predict():
    if request.method == "POST":
        email_content = request.form["email_content"]
        try:
            model, vectorizer = load_model()
            prediction = predict_spam(email_content, model, vectorizer)
            return render_template("emailspam.html", spam_prediction=prediction, error=None)
        except Exception as e:
            return render_template("emailspam.html", spam_prediction=None, error=str(e))


@app.route("/password")
def password():
    return render_template("password.html")




@app.route("/password_predict", methods=['POST'])
def password_predict():
    if request.method == "POST":
        pass
        exampleInputpassword1 = request.form["password"]
        try:
            saved_vectorizer = load_vectorizer()
            app.logger.info("Loaded vectorizer successfully")
            final_model = load_passmodel()
            app.logger.info("Loaded model successfully")

            password_prediction = check_password_strength(exampleInputpassword1, saved_vectorizer, final_model)
            app.logger.info("Password prediction: %s", password_prediction)
            if password_prediction == 0:
                return render_template("password.html", strength="Very Weak Password", error=None)
            elif password_prediction == 1:
                return render_template("password.html", strength="Average Password", error=None)
            elif password_prediction == 2:
                return render_template("password.html", strength="Strong Password", error=None)
        except FileNotFoundError as e:
            app.logger.error("Error loading vectorizer or model: %s", e)
            return render_template("password.html", strength=None, error="Error loading model or vectorizer")
        except Exception as e:
            app.logger.error("Unexpected error: %s", e)
            return render_template("password.html", strength=None, error="An unexpected error occurred")
    else:
        return render_template("password.html")


if __name__ == "__main__":
    app.run(debug=True)
