import os
import dash
from dash import dcc, html
import plotly.graph_objects as go
import json
from dash.dependencies import Input, Output
from pathlib import Path


def get_latest_results_file(base_path):
    base = Path(base_path)
    subdirs = [d for d in base.iterdir() if d.is_dir()]
    if not subdirs:
        raise FileNotFoundError("No timestamped result directories found.")

    latest_dir = max(subdirs, key=lambda d: d.name)
    return latest_dir / "results.json"


RESULTS_FILE = get_latest_results_file("../experiments/FIFA/ConservativeCountMinSketch/w10000_d5")
app = dash.Dash(__name__)

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
    html.H1("CMS Algorithm Performance Metrics"),
    *(dcc.Graph(id=graph_id) for graph_id, *_ in GRAPH_METRICS),
    *(dcc.Graph(id=graph_id) for graph_id, _ in PERCENTILE_GRAPHS),
    dcc.Interval(id='interval-component', interval=500, n_intervals=0),
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


last_modified = None


def file_changed(path):
    global last_modified
    modified = os.path.getmtime(path)
    if last_modified is None or modified != last_modified:
        last_modified = modified
        return True
    return False


@app.callback(
    [Output(graph_id, 'figure') for graph_id, *_ in GRAPH_METRICS] +
    [Output(graph_id, 'figure') for graph_id, _ in PERCENTILE_GRAPHS],
    Input('interval-component', 'n_intervals')
)
def update_graphs(_):
    if not file_changed(RESULTS_FILE):
        raise dash.exceptions.PreventUpdate
    results = load_results(RESULTS_FILE)
    figures = [generate_metric_graph(results, metric, ylabel, title)
               for _, metric, ylabel, title in GRAPH_METRICS]
    figures += [generate_percentile_graph(results, category)
                for _, category in PERCENTILE_GRAPHS]
    return figures


if __name__ == '__main__':
    app.run(debug=True)
