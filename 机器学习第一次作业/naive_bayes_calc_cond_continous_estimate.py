import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gamma

X_COL = "debt_to_income_ratio"      # continuous column
B_COL = "loan_paid_back"      # conditioning column (0 / 1)
MAX_ROWS = 19_000

x_given_0 = []
x_given_1 = []

row_count = 0

with open("loan_dataset_20000.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        if row_count >= MAX_ROWS:
            break

        try:
            x = float(row[X_COL])
            b = int(row[B_COL])
        except ValueError:
            raise ValueError(f"Invalid data at row {row_count + 2}")

        if b not in (0, 1):
            raise ValueError(f"Conditioning value must be 0 or 1, got {b}")

        if b == 0:
            x_given_0.append(x)
        else:
            x_given_1.append(x)

        row_count += 1

assert row_count == MAX_ROWS

# --------------------------------------------------
# 2. Fit Gamma distributions (MLE)
# --------------------------------------------------

# Force location = 0 (important for interpretability)
k0, loc0, theta0 = gamma.fit(x_given_0, floc=0)
k1, loc1, theta1 = gamma.fit(x_given_1, floc=0)

print("B = 0  -> shape k =", k0, ", scale θ =", theta0)
print("B = 1  -> shape k =", k1, ", scale θ =", theta1)

# --------------------------------------------------
# 3. Plot histograms + fitted PDFs (subplots)
# --------------------------------------------------

fig, axes = plt.subplots(1, 2, figsize=(12, 4), sharey=True)

x_grid = np.linspace(0, max(max(x_given_0), max(x_given_1)), 1000)

# ---- B = 0 ----
axes[0].hist(
    x_given_0, bins=50, density=True, alpha=0.6
)
axes[0].plot(
    x_grid,
    gamma.pdf(x_grid, k0, scale=theta0),
    linewidth=2
)
axes[0].set_title(r"$X \mid B = 0$")
axes[0].set_xlabel("DTI ratio")
axes[0].set_ylabel("Probability density")

# ---- B = 1 ----
axes[1].hist(
    x_given_1, bins=50, density=True, alpha=0.6
)
axes[1].plot(
    x_grid,
    gamma.pdf(x_grid, k1, scale=theta1),
    linewidth=2
)
axes[1].set_title(r"$X \mid B = 1$")
axes[1].set_xlabel("DTI ratio")

plt.tight_layout()
plt.show()