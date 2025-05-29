from flask import Flask, Response, send_file, render_template, g, redirect, url_for, request
import sqlite3
from pathlib import Path
from utils.pl_parser import parse_scenarios
from ga_runner import run_evolution_db, get_decisions
from utils.plot import plot_fitness_trend, plot_weight_pie, plot_weight_trend
from io import BytesIO
import matplotlib.pyplot as plt

app = Flask(__name__)
DB_PATH = 'data.db'
PL_PATH = (
    Path(__file__).parent
    / 'evolutionary_ethics'
    / 'symbolic_reasoning_sys'
    / 'expanded versions'
    / 'ethics_engine_expanded_32.pl'
)

last_mtime = None

def get_db():
    """
    Get a database connection, creating one if necessary.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    """
    Close the database connection at the end of the request.
    """
    db = g.pop('db', None)
    if db:
        db.close()

def refresh_scenarios_if_needed():
    """
    Reload scenario definitions from the Prolog file if it has been updated.
    """
    global last_mtime
    mtime = PL_PATH.stat().st_mtime
    if last_mtime is None or mtime > last_mtime:
        last_mtime = mtime
        scenes = parse_scenarios(PL_PATH)
        db = get_db()
        db.execute("DELETE FROM scenarios")
        db.executemany(
            """
            INSERT INTO scenarios
              (code, owner_nearby, valuable, environment, legal_context)
            VALUES (?, ?, ?, ?, ?)
            """, scenes)
        db.commit()

@app.before_request
def before_request():
    """
    Check for updated scenarios before each request.
    """
    refresh_scenarios_if_needed()

@app.route('/')
def index():
    """
    Render the main page with a list of scenarios and no GA run yet.
    """
    db = get_db()
    rows = db.execute("SELECT * FROM scenarios").fetchall()
    return render_template('index.html', scenes=rows, run_id=None)

@app.route('/run_ga', methods=['POST'])
def run_ga_route():
    """
    Execute the genetic algorithm, store results in the database, and render the updated page.
    """
    db = get_db()

    # 1. Create a new record in the ga_runs table
    cur = db.execute(
        """
        INSERT INTO ga_runs (pop_size, generations, cx_prob, mut_prob)
        VALUES (?, ?, ?, ?)
        """, (50, 20, 0.5, 0.3))
    run_id = cur.lastrowid
    db.commit()

    # 2. Run GA and write generation results
    run_evolution_db(run_id, pop_size=50, ngen=20, cxpb=0.5, mutpb=0.3)

    # 3. Save final decisions to the database
    for rid, scenario, action, justification, score in get_decisions(run_id):
        db.execute(
            """
            INSERT INTO ga_final_decisions
              (run_id, scenario_code, action, justification, score)
            VALUES (?, ?, ?, ?, ?)
            """, (rid, scenario, action, justification, score))
    db.commit()

    # After completion, reload scenarios and fetch decisions
    scenes = db.execute(
        "SELECT code, owner_nearby, valuable, environment, legal_context FROM scenarios"
    ).fetchall()
    decisions = db.execute(
        "SELECT scenario_code AS scenario, action, justification, score"
        " FROM ga_final_decisions WHERE run_id=?",
        (run_id,)
    ).fetchall()

    return render_template('index.html', scenes=scenes, run_id=run_id, decisions=decisions)

@app.route('/plot/fitness')
def plot_fitness_route():
    """
    Return the GA fitness trend chart for the given run_id (or latest if missing).
    """
    run_id = request.args.get('run_id', type=int)
    if not run_id:
        row = get_db().execute("SELECT MAX(id) FROM ga_runs").fetchone()
        run_id = row[0] or 1
    buf = plot_fitness_trend(run_id)
    return Response(buf.getvalue(), mimetype='image/png')

@app.route('/plot/weights')
def plot_weights_route():
    """
    Return the pie chart of the best individual's weights for the given run_id.
    """
    run_id = request.args.get('run_id', type=int)
    buf = plot_weight_pie(run_id)
    return Response(buf.getvalue(), mimetype='image/png')

@app.route('/plot/weight_trend')
def plot_weight_trend_route():
    """
    Return the trend chart of weight evolution across generations for the given run_id.
    """
    run_id = request.args.get('run_id', type=int)
    if not run_id:
        row = get_db().execute("SELECT MAX(id) FROM ga_runs").fetchone()
        run_id = row[0] or 1
    buf = plot_weight_trend(run_id)
    return Response(buf.getvalue(), mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
