import matplotlib.pyplot as plt

# Define methods and times
methods = ["readlines()", "loop line-by-line", "set()"]
times = [86.79, 46.42, 86.39]  # Your real results here

# Plot
plt.figure(figsize=(10, 6))
plt.bar(methods, times, color=["#4CAF50", "#2196F3", "#FFC107"])
plt.title("File Search Method Benchmark")
plt.xlabel("Search Method")
plt.ylabel("Execution Time (ms)")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()

# Save chart
plt.savefig("benchmark_chart.png")
plt.show()
