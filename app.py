from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime, timezone
from functools import wraps
import secrets

app = Flask(__name__)

# Secret key for session
app.secret_key = secrets.token_hex(32)

# 45 seconds inactivity timeout
SESSION_TIMEOUT = 45

# Demo login
VALID_EMAIL = "admin@gmail.com"
VALID_PASSWORD = "123456"


# =========================================================
# LOGIN REQUIRED
# =========================================================

def login_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if "user" not in session:
            return redirect(url_for("login"))

        return function(*args, **kwargs)

    return wrapper


# =========================================================
# CHECK SERVER SESSION TIMEOUT
# =========================================================

@app.before_request
def check_session_timeout():

    # Ignore static files
    if request.endpoint == "static":
        return

    # Ignore login page
    if request.endpoint == "login":
        return

    # Ignore timeout endpoint
    if request.endpoint == "session_expired":
        return

    if "user" not in session:
        return

    last_activity = session.get("last_activity")

    if last_activity:

        try:

            last_activity_time = datetime.fromisoformat(last_activity)

            current_time = datetime.now(timezone.utc)

            elapsed = (
                current_time - last_activity_time
            ).total_seconds()

            if elapsed > SESSION_TIMEOUT:

                session.clear()

                if request.path == "/activity":
                    return jsonify({
                        "status": "expired"
                    }), 401

                flash("Session timed out", "timeout")

                return redirect(url_for("login"))

        except Exception:

            session.clear()
            return redirect(url_for("login"))


# =========================================================
# LOGIN PAGE
# IMPORTANT: BOTH / AND /login WORK
# =========================================================

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():

    if "user" in session:
        return redirect(url_for("home"))

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if email == VALID_EMAIL and password == VALID_PASSWORD:

            session.clear()

            session["user"] = email

            session["last_activity"] = (
                datetime.now(timezone.utc).isoformat()
            )

            return redirect(url_for("home"))

        flash("Invalid email or password", "error")

    return render_template("login.html")


# =========================================================
# HOME
# =========================================================

@app.route("/home")
@login_required
def home():

    return render_template("home.html")


# =========================================================
# ABOUT
# =========================================================

@app.route("/about")
@login_required
def about():

    return render_template("about.html")


# =========================================================
# CONTACT
# =========================================================

@app.route("/contact", methods=["GET", "POST"])
@login_required
def contact():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        print("CONTACT FORM")
        print(name)
        print(email)
        print(message)

        flash(
            "Your message has been submitted.",
            "success"
        )

        return redirect(url_for("contact"))

    return render_template("contact.html")


# =========================================================
# FEEDBACK
# =========================================================

@app.route("/feedback", methods=["GET", "POST"])
@login_required
def feedback():

    if request.method == "POST":

        rating = request.form.get("rating")
        comments = request.form.get("comments")

        print("FEEDBACK")
        print(rating)
        print(comments)

        flash(
            "Thank you for your feedback.",
            "success"
        )

        return redirect(url_for("feedback"))

    return render_template("feedback.html")


# =========================================================
# USER ACTIVITY
# =========================================================

@app.route("/activity", methods=["POST"])
@login_required
def activity():

    session["last_activity"] = (
        datetime.now(timezone.utc).isoformat()
    )

    return jsonify({
        "status": "active"
    })


# =========================================================
# SESSION EXPIRED FROM JAVASCRIPT
# =========================================================

@app.route("/session-expired", methods=["POST"])
def session_expired():

    session.clear()

    return jsonify({
        "status": "expired"
    })


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(url_for("login"))


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )