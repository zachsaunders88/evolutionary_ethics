# utils/plot.py

import os
os.environ.setdefault('MPLCONFIGDIR', os.path.join(os.getcwd(), 'mplconfig'))
os.makedirs(os.environ['MPLCONFIGDIR'], exist_ok=True)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import sqlite3
from io import BytesIO


DB_PATH = 'data.db'


def plot_fitness_trend(run_id: int):
    conn = sqlite3.connect(DB_PATH)
    c    = conn.cursor()
    c.execute("""
      SELECT generation, accuracy
      FROM ga_generation_results
      WHERE run_id=?
      ORDER BY generation
    """, (run_id,))
    rows = c.fetchall()
    conn.close()

    gens = [r[0] for r in rows]
    accs = [r[1] for r in rows]

    fig, ax = plt.subplots()
    ax.plot(gens, accs, marker='o')
    ax.set_xlabel('Generation')
    ax.set_ylabel('Accuracy')
    ax.set_title(f'GA Fitness Trend (run {run_id})')
    ax.grid(True)

    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return buf

def plot_weight_pie(run_id: int = None):
    """
    Fetch util_weight, deon_weight, self_weight from the latest generation
    in the ga_generation_results table, draw a pie chart, and return PNG binary stream.
    If run_id is not specified, select the latest run_id.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if run_id is None:
        # Get the latest run_id
        c.execute("SELECT MAX(run_id) FROM ga_generation_results")
        row = c.fetchone()
        if row is None:
            raise RuntimeError("No GA results in database.")
        run_id = row[0]

    print("Using run_id:", run_id)  # 调试用

    # Query weights of the latest generation
    c.execute(
        """
        SELECT util_weight, deon_weight, self_weight
        FROM ga_best_individuals
        WHERE run_id=?
        ORDER BY accuracy DESC
        LIMIT 1
        """,
        (run_id,)
    )
    row = c.fetchone()
    conn.close()

    if not row:
        raise RuntimeError(f"No weight data for run_id={run_id}")

    labels = ['Utilitarian', 'Deontological', 'Self-interest']
    sizes = list(row)

    fig, ax = plt.subplots()
    ax.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=90
    )
    ax.axis('equal')
    ax.set_title(f'Ethical Weights Composition (run {run_id})')

    buf = BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return buf

def plot_weight_trend(run_id: int):
    """
    Fetch util, deon, self weights of each generation from ga_generation_results table,
    draw a line chart to show their evolution over generations.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
      SELECT generation, util_weight, deon_weight, self_weight
      FROM ga_generation_results
      WHERE run_id=?
      ORDER BY generation
    """, (run_id,))
    rows = c.fetchall()
    conn.close()

    gens       = [r[0] for r in rows]
    util_vals  = [r[1] for r in rows]
    deon_vals  = [r[2] for r in rows]
    self_vals  = [r[3] for r in rows]

    fig, ax = plt.subplots()
    ax.plot(gens, util_vals, marker='o', label='Utilitarian')
    ax.plot(gens, deon_vals, marker='o', label='Deontological')
    ax.plot(gens, self_vals, marker='o', label='Self-interest')
    ax.set_xlabel('Generation')
    ax.set_ylabel('Weight')
    ax.set_title(f'Weight Evolution (run {run_id})')
    ax.grid(True)
    ax.legend()

    buf = BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf
