from flask import Flask, request, render_template, jsonify, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from collections import Counter
from flask_socketio import SocketIO, emit
import uuid
import string
import os
from models import db, Submission  # Importuj SQLAlchemy i Submission

app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app)
# Inicjalizacja SQLAlchemy
db.init_app(app)
migrate = Migrate(app, db)

countdown_time = 0
time_limit = 0
time_left = 0

# Sprawdzenie istnienia bazy danych i inicjalizacja, jeśli nie istnieje
if not os.path.exists(app.config['SQLALCHEMY_DATABASE_URI']):
    with app.app_context():
        db.create_all()


# Funkcja do normalizacji fraz
def normalize_phrase(phrase):
    phrase = phrase.translate(str.maketrans('', '', string.punctuation))
    phrase = phrase.lower()
    phrase = phrase.strip()
    return phrase


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        phrase = request.json.get('phrase').strip()
        normalized_phrase = normalize_phrase(phrase)
        player_id = request.cookies.get('player_id')

        if not player_id:
            player_id = str(uuid.uuid4())

        if countdown_time==0:
            return jsonify({'success': False, 'message': 'You have already submitted a phrase or time out'}), 403

        submission = Submission.query.filter_by(player_id=player_id).first()

        if submission and submission.has_submitted:
            return jsonify({'success': False, 'message': 'You have already submitted a phrase or time out'}), 403



        if not submission:
            submission = Submission(phrase=phrase, normalized_phrase=normalized_phrase, player_id=player_id)

        submission.has_submitted = True
        db.session.add(submission)
        db.session.commit()

        response = jsonify({'success': True, 'message': 'Phrase submitted successfully!'})
        response.set_cookie('player_id', player_id, max_age=60 * 60 * 24 * 365)
        return response

    return render_template('index.html')


@app.route('/timer', methods=['GET', 'POST'])
def timer():
    global time_limit
    if request.method == 'POST':
        time_limit = int(request.form['time_limit'])
    return redirect(url_for('results'))


@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        Submission.query.delete()
        db.session.commit()
        return redirect(url_for('results'))

    submissions = Submission.query.all()

    # Liczymy częstotliwość wystąpień fraz
    phrase_counts = Counter(submission.normalized_phrase for submission in submissions)

    # Sortujemy frazy wg liczby wystąpień (malejąco)
    sorted_phrases = sorted(phrase_counts.items(), key=lambda x: x[1], reverse=True)

    return render_template('results.html', sorted_phrases=sorted_phrases)


@app.route('/reset', methods=['GET', 'POST'])
def reset():
    global countdown_time, time_limit, time_left
    if request.method == 'POST':
        db.session.query(Submission).delete()
        db.session.commit()
        del time_left, time_limit, countdown_time

        response = make_response(redirect(url_for('results')))
        response.delete_cookie('player_id')

        return response

    return render_template('reset.html')


@socketio.on('start_timer')
def handle_start_timer():
    global countdown_time, time_limit, time_left
    countdown_time = time_limit
    while countdown_time > 0:
        socketio.sleep(1)
        time_left = countdown_time
        countdown_time -= 1
        emit('update_timer', {'time': countdown_time}, broadcast=True)
    emit('timer_complete', broadcast=True)


if __name__ == '__main__':
    socketio.run(app)
    app.run(debug=True)
