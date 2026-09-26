import os
import telebot
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "v2box-render-secret-key-13579")

# Environment Variables
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_IDS = [int(i.strip()) for i in os.getenv("ADMIN_IDS", "0").split(",") if i.strip().isdigit()]
ADMIN_PANEL_PASSWORD = os.getenv("ADMIN_PANEL_PASSWORD", "kiki13579")
SHOP_NAME = os.getenv("SHOP_NAME", "V2BOX KEY SHOP")
CURRENCY = os.getenv("CURRENCY", "MMK")
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL", "https://v2box-shop.onrender.com")

bot = telebot.TeleBot(BOT_TOKEN) if BOT_TOKEN else None

@app.route("/")
def home():
    if "logged_in" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        pwd = request.form.get("password")
        if pwd == ADMIN_PANEL_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            error = "Password မမှန်ကန်ပါ။"
    return render_template("login.html", error=error, shop_name=SHOP_NAME)

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("dashboard.html", shop_name=SHOP_NAME, currency=CURRENCY, base_url=RENDER_EXTERNAL_URL)

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
