# import json
# import matplotlib.pyplot as plt

# plannername="Metis_OPT-350"
# with open(f"/workspaces/sailor_test/sailor/Planner/simulations/results/{plannername}.json") as f:
#     d = json.load(f)
#     if isinstance(d, list) and len(d) > 0:
#         d = d[0]  # pick the first dictionary

# throughput = d.get("throughput", 0)
# cost = d.get("cost_per_iteration", 0)

# print(f"Throughput: {throughput}")
# print(f"Cost per iteration: {cost}")

# plt.bar(["Throughput", "Cost"], [throughput, cost])
# plt.title("Simulation Result Summary")
# plt.show()
# plt.savefig(f"/workspaces/sailor_test/sailor/Planner/simulations/results/{plannername}_plot.png")
# print(f"Plot saved to /workspaces/sailor_test/sailor/Planner/simulations/results/{plannername}_plot.png")

import json
import matplotlib.pyplot as plt
import glob
import os
import numpy as np

# --- Configuration ---
# Define the directory containing your result files
results_dir = "/workspaces/sailor_test/sailor/Planner/simulations/results"
# --- End Configuration ---

# Use glob to find all .json files in the directory
json_files = glob.glob(os.path.join(results_dir, "*.json"))

if not json_files:
    print(f"Error: No .json files found in {results_dir}")
    exit()

results = {} # Dictionary to store all planner results

print("--- Processing Planner Results ---")

# Loop through all found JSON files
for f_path in json_files:
    # Extract the model name from the file path
    # e.g., ".../Metis_OPT-350.json" -> "Metis_OPT-350"
    filename = os.path.basename(f_path)
    modelname = os.path.splitext(filename)[0]

    try:
        with open(f_path) as f:
            d = json.load(f)
            if isinstance(d, list) and len(d) > 0:
                d = d[0]  # Keep your logic to pick the first dict if it's a list

            # Get throughput and cost, defaulting to 0 if key is missing
            throughput = d.get("throughput", 0)
            cost = d.get("cost_per_iteration", 0)

            # Store the results
            results[modelname] = {"throughput": throughput, "cost": cost}
            
            print(f"Loaded {modelname}: T={throughput}, C={cost}")

    except json.JSONDecodeError:
        print(f"Warning: Skipping {filename} - Could not decode JSON.")
    except Exception as e:
        print(f"Warning: Skipping {filename} - Error: {e}")

print("---------------------------------")

if not results:
    print("No valid model data was loaded. Exiting.")
    exit()

# --- Prepare Data for Plotting ---
model_names = list(results.keys())
throughputs = [results[name]["throughput"] for name in model_names]
costs = [results[name]["cost"] for name in model_names]

# --- Create the Comparison Plot (Dual Y-Axis) ---

x_positions = np.arange(len(model_names))  # the label locations
width = 0.4  # the width of the bars

fig, ax1 = plt.subplots(figsize=(12, 7))

# Plot Throughput on the first Y-axis (ax1)
color = 'tab:blue'
ax1.set_xlabel("Model Name")
ax1.set_ylabel("Throughput", color=color)
ax1.bar(x_positions - width/2, throughputs, width, color=color, label='Throughput')
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_xticks(x_positions)
ax1.set_xticklabels(model_names, rotation=45, ha="right")

# Create a second Y-axis (ax2) that shares the same X-axis
ax2 = ax1.twinx()  
color = 'tab:orange'
ax2.set_ylabel("Cost per Iteration", color=color)  # we already handled the x-label with ax1
ax2.bar(x_positions + width/2, costs, width, color=color, label='Cost per Iteration')
ax2.tick_params(axis='y', labelcolor=color)

# --- Finalize and Save Plot ---
fig.suptitle("Simulation Result Summary (All Models)", fontsize=16)
fig.tight_layout()  # Adjust layout to prevent labels from overlapping

# Add a combined legend
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

# Save the combined plot
save_path = os.path.join(results_dir, "all_models_comparison_plot.png")
plt.savefig(save_path)
plt.show()

print(f"\nComparison plot saved to {save_path}")