import json
import matplotlib.pyplot as plt
import os


def load_results(filepath):
    with open(filepath, "r") as file:
        return json.load(file)


def plot_metric(results, metric, ylabel, title, save_path):
    processed_items = [entry["processed_items"] for entry in results]
    values = [entry[metric] for entry in results]

    plt.figure(figsize=(8, 5))
    plt.plot(processed_items, values, marker="o", linestyle="-", markersize=3, label=metric)
    plt.xlabel("Number of Processed Items")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)

    plt.savefig(save_path)
    plt.show()


def plot_percentiles(results, save_path):
    processed_items = [entry["processed_items"] for entry in results]
    p50 = [entry["percentiles"]["50th"] for entry in results]
    p90 = [entry["percentiles"]["90th"] for entry in results]
    p95 = [entry["percentiles"]["95th"] for entry in results]
    p100 = [entry["percentiles"]["100th"] for entry in results]

    plt.figure(figsize=(8, 5))
    plt.plot(processed_items, p100, marker="*", linestyle=":", markersize=3, label="100th Percentile")
    plt.plot(processed_items, p95, marker="^", linestyle="-.", markersize=3, label="95th Percentile")
    plt.plot(processed_items, p90, marker="s", linestyle="-", markersize=3, label="90th Percentile")
    plt.plot(processed_items, p50, marker="o", linestyle="--", markersize=3, label="50th Percentile")

    plt.xlabel("Number of Processed Items")
    plt.ylabel("Error Value")
    plt.title("Error Percentiles Over Time")
    plt.legend()
    plt.grid(True)

    plt.savefig(save_path)
    plt.show()


def visualize(results_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    results = load_results(results_file)

    plot_metric(results, "avg_error", "Average Error", "Avg Error vs. Processed Items", f"{output_dir}/avg_error.png")
    plot_metric(results, "overestimation_percentage", "Overestimation Percentage (%)", "Overestimation Percentage vs. Processed Items",
                f"{output_dir}/overestimation_percentage.png")
    plot_metric(results, "load_factor", "Load Factor", "Factor vs. Processed Items",
                f"{output_dir}/load_factor.png")
    plot_metric(results, "query_speed", "Query Speed (seconds per item)", "Query Speed vs. Processed Items",
                f"{output_dir}/query_speed.png")
    plot_metric(results, "memory_usage", "Memory Usage (bytes)", "Memory Usage vs. Processed Items",
                f"{output_dir}/memory_usage.png")
    plot_percentiles(results, f"{output_dir}/percentiles.png")
