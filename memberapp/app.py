from Flask import flask, render_template, g, request, session, redirect, url_for
from database import get_db, connect_db

app = Flask(__name__)

# generate random string - to gen config value for secret key
# need to generate this for session to work!
app.config['SECRET_KEY'] = os.urandom(24)

# tear down database every time a request ends
# checks if there's an active database
# database dynamically closed, if db active
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def get_current_user():
    pass

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    pass

@app.route('/login', methods=['GET', 'POST'])
def login():
    pass

@app.route('/users', )
def users():
    pass

@app.route('/logout')
def logout():
    pass


if __name__ == '__main__':
    app.run(debug=True)

