from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.secret_key = "secretkey"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Simple in-memory "database"
users = {}          # username -> password
users_by_id = {}    # id -> User object


class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username


@login_manager.user_loader
def load_user(user_id):
    return users_by_id.get(user_id)


@app.route("/")
@login_required
def home():
    return f"Hello, {current_user.username}! <a href='/logout'>Logout</a>"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users:

            return redirect(url_for("register"))

        user_id = str(len(users_by_id) + 1)
        users[username] = password
        users_by_id[user_id] = User(user_id, username)

    
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            for user in users_by_id.values():
                if user.username == username:
                    login_user(user)
                    return redirect(url_for("home"))


    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
