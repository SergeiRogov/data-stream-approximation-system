import os
import dash
import json
import datetime
import subprocess
from dash import dcc, html, no_update
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from pathlib import Path


def get_latest_results_file(base_path):
    base = Path(base_path)
    subdirs = [d for d in base.iterdir() if d.is_dir()]
    if not subdirs:
        raise FileNotFoundError("No timestamped result directories found.")

    latest_dir = max(subdirs, key=lambda d: d.name)
    return latest_dir / "results.json"


app = dash.Dash(__name__)
server = app.server
last_modified = 0

GRAPH_METRICS = [
    ("avg_error_graph", "avg_error", "Average Error", "Avg Error vs. Processed Items"),
    ("overestimation_percentage_graph", "overestimation_percentage", "Overestimation Percentage (%)", "Overestimation Percentage vs. Processed Items"),
    ("underestimation_percentage_graph", "underestimation_percentage", "Underestimation Percentage (%)", "Underestimation Percentage vs. Processed Items"),
    ("exact_match_percentage_graph", "exact_match_percentage", "Exact Match Percentage (%)", "Exact Match Percentage vs. Processed Items"),
    ("load_factor_graph", "load_factor", "Load Factor", "Load Factor vs. Processed Items"),
    ("avg_query_time_graph", "avg_query_time", "Average Query Time (seconds)", "Avg Query Time vs. Processed Items"),
    ("memory_usage_graph", "memory_usage", "Memory Usage (bytes)", "Memory Usage vs. Processed Items"),
]

PERCENTILE_GRAPHS = [
    ("overestimation_percentiles_graph", "overestimation"),
    ("underestimation_percentiles_graph", "underestimation"),
    ("combined_percentiles_graph", "combined"),
]

app.layout = html.Div([
    html.Div([
        html.Label("Select Algorithm 1"),
        dcc.Dropdown(
            id='algo1-dropdown',
            options=[{'label': name, 'value': name} for name in
                     ["CountMinSketch",
                      "ConservativeCountMinSketch",
                      "CountMeanMinSketch",
                      "CountSketch",
                      "DecayCMS"]],
            value='CountMinSketch'
        ),
        html.Label("Select Algorithm 2"),
        dcc.Dropdown(
            id='algo2-dropdown',
            options=[{'label': name, 'value': name} for name in
                     ["CountMinSketch",
                      "ConservativeCountMinSketch",
                      "CountMeanMinSketch",
                      "CountSketch",
                      "DecayCMS"]],
            value='ConservativeCountMinSketch'
        ),
        html.Label("Width"),
        dcc.Input(id='width-input', type='number', value=10000, min=1),
        html.Label("Depth"),
        dcc.Input(id='depth-input', type='number', value=5, min=1),
        html.Label("Select Dataset"),
        dcc.Dropdown(
            id='dataset-dropdown',
            options=[{'label': name, 'value': name} for name in
                     ["FIFA.csv",
                      "uchoice-Kosarak.txt",
                      "uchoice-Kosarak-5-25.txt",
                      "synthetic"]],
            value='FIFA.csv'
        ),
        html.Button("Run Experiment", id='run-button', n_clicks=0),
    ]),
    html.Div(id='graphs-container'),
    dcc.Interval(id='interval-component', interval=500, n_intervals=0, disabled=True),
    dcc.Store(id="latest-results-store"),
])


def load_results(filepath):
    with open(filepath, "r") as file:
        return json.load(file)


def generate_line_graph(x, y, name, ylabel, title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name=name))
    fig.update_layout(
        title=title,
        xaxis_title="Number of Processed Items",
        yaxis_title=ylabel,
        template="plotly_dark",
        height=400
    )
    return fig


def generate_metric_graph(results, metric, ylabel, title):
    x = [entry["processed_items"] for entry in results]
    y = [entry[metric] for entry in results]
    return generate_line_graph(x, y, metric, ylabel, title)


def generate_percentile_graph(results, category):
    x = [entry["processed_items"] for entry in results]
    get = lambda p: [entry["percentiles"][category].get(p, 0.0) for entry in results]
    percentiles = [("100th", get("100th")), ("95th", get("95th")),
                   ("90th", get("90th")), ("50th", get("50th"))]

    fig = go.Figure()
    for label, y in percentiles:
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name=f"{label} Percentile"))

    fig.update_layout(
        title=f"{category.capitalize()} Error Percentiles Over Time",
        xaxis_title="Number of Processed Items",
        yaxis_title="Error Value",
        template="plotly_dark",
        height=400
    )
    return fig


def file_changed(path):
    global last_modified
    modified = os.path.getmtime(path)
    if last_modified is None or modified != last_modified:
        last_modified = modified
        return True
    return False


def generate_result_path(algorithm, dataset, width, depth, timestamp):
    dir_path = f"../experiments/{dataset}/{algorithm}/w{width}_d{depth}/{timestamp}/results.json"
    return dir_path


dcc.Interval(
    id='interval-component',
    interval=0.5*1000,
    n_intervals=0
)


@app.callback(
    Output('interval-component', 'disabled'),
    Output('latest-results-store', 'data'),
    Input('run-button', 'n_clicks'),
    State('algo1-dropdown', 'value'),
    State('algo2-dropdown', 'value'),
    State('dataset-dropdown', 'value'),
    State('width-input', 'value'),
    State('depth-input', 'value')
)
def run_experiment(n_clicks, algo1, algo2, dataset, width, depth):
    if n_clicks == 0:
        raise dash.exceptions.PreventUpdate

    now = datetime.datetime.now()
    timestamp1 = now.strftime("%Y-%m-%d_%H-%M-%S")
    timestamp2 = (now + datetime.timedelta(seconds=1)).strftime("%Y-%m-%d_%H-%M-%S") if algo1 == algo2 else timestamp1

    subprocess.Popen([
        "python3", "../simulation/simulation.py",
        "--algorithm", algo1,
        "--dataset", dataset,
        "--width", str(width),
        "--depth", str(depth),
        "--timestamp", timestamp1
    ])
    subprocess.Popen([
        "python3", "../simulation/simulation.py",
        "--algorithm", algo2,
        "--dataset", dataset,
        "--width", str(width),
        "--depth", str(depth),
        "--timestamp", timestamp2
    ])

    results1 = generate_result_path(algo1, dataset, width, depth, timestamp1)
    results2 = generate_result_path(algo2, dataset, width, depth, timestamp2)
    label_1 = f"{algo1}"
    label_2 = f"{algo2}"
    return False, {label_1: results1, label_2: results2}


@app.callback(
    Output('graphs-container', 'children'),
    Input('interval-component', 'n_intervals'),
    Input('latest-results-store', 'data')
)
def update_graphs(n_intervals, results_paths):
    if not results_paths:
        return []

    graphs = []
    for label, path in results_paths.items():
        if not os.path.exists(path):
            continue
        data = load_results(path)
        for graph_id, metric, ylabel, title in GRAPH_METRICS:
            fig = generate_metric_graph(data, metric, ylabel, f"{title} [{label}]")
            graphs.append(dcc.Graph(id=f"{graph_id}-{label}", figure=fig))

        for graph_id, category in PERCENTILE_GRAPHS:
            fig = generate_percentile_graph(data, category)
            fig.update_layout(title=f"{category.capitalize()} Percentiles [{label}]")
            graphs.append(dcc.Graph(id=f"{graph_id}-{label}", figure=fig))

    return graphs


if __name__ == '__main__':
    app.run(debug=True)
