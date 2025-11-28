import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------
# 1. DATA EXTRACTION
# ---------------------------------------------------------
# Independent Variable: GPU Counts (Updated for new dataset)
gpu_counts = [128, 320, 512]

# Data extracted from the provided logs
# Format: 'BaselineName': { 'metric': [val_128, val_320, val_512] }
data = {
    'AMP': {
        'throughput': [0.1316, 0.2062, 0.3125],
        'cost': [0.8279, 1.0739, 1.3944],
        'search_time': [4.45, 7.09, 11.43],
        'oom': False
    },
    'FlashFlex': {
        'throughput': [0.1175, 0.2389, 0.3082],
        'cost': [0.9270, 1.1397, 1.4138],
        'search_time': [1.71, 20.79, 84.55],
        'oom': False
    },
    'Metis': {
        'throughput': [0.1243, 0.2273, 0.4292],
        'cost': [0.8763, 0.5110, 1.0150],
        'search_time': [334.73, 341.23, 395.28],
        'oom': False
    },
    'SAILOR': {
        'throughput': [0.1700, 0.3609, 0.5229],
        'cost': [0.6288, 0.7545, 0.8332],
        'search_time': [1.10, 2.86, 5.39],
        'oom': False
    }
}

baselines = list(data.keys())
n_groups = len(gpu_counts)
n_baselines = len(baselines)

# ---------------------------------------------------------
# 2. PLOTTING SETUP
# ---------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(20, 6))
fig.suptitle('Sailor Planner vs Baselines (128, 320, 512 GPUs)', fontsize=16)

# Bar configuration
bar_width = 0.15  # Increased width slightly since there are fewer baselines
index = np.arange(n_groups)
opacity = 0.8
colors = plt.cm.tab10(np.linspace(0, 1, n_baselines))

# ---------------------------------------------------------
# 3. HELPER FUNCTION TO PLOT
# ---------------------------------------------------------
def plot_metric(ax_idx, metric_key, title, y_label, log_scale=False):
    ax = axes[ax_idx]
    
    for i, baseline in enumerate(baselines):
        values = data[baseline][metric_key]
        offset = (i - n_baselines/2) * bar_width + (bar_width/2)
        rects = ax.bar(index + offset, values, bar_width,
                       alpha=opacity,
                       color=colors[i],
                       label=baseline)
        
    ax.set_xlabel('Number of Available GPUs')
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.set_xticks(index)
    ax.set_xticklabels(gpu_counts)
    
    if log_scale:
        ax.set_yscale('log')
    
    ax.grid(True, which="both", ls="-", alpha=0.2)

# ---------------------------------------------------------
# 4. GENERATE SUBPLOTS
# ---------------------------------------------------------

# Plot 1: Throughput
plot_metric(0, 'throughput', 'Throughput (Higher is Better)', 'Throughput (iters/sec)')

# Plot 2: Cost
plot_metric(1, 'cost', 'Cost (Lower is Better)', 'Cost ($/iter)')

# Plot 3: Search Time
plot_metric(2, 'search_time', 'Search Time (Lower is Better)', 'Time (seconds)', log_scale=True)

# ---------------------------------------------------------
# 5. LEGEND AND SAVE
# ---------------------------------------------------------
# Add a single legend for the whole figure
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper right', bbox_to_anchor=(0.99, 0.95), fontsize='medium', title="Baselines")

plt.tight_layout()
plt.subplots_adjust(top=0.85, right=0.88) # Make space for title and legend

output_file = 'sailor_benchmark_results_hetero.png'
plt.savefig(output_file, dpi=300)
print(f"Plot saved successfully to {output_file}")