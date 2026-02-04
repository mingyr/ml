import csv

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

import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(12, 4), sharex=True, sharey=True)

axes[0].hist(x_given_0, bins=50, density=True)
axes[0].set_title(r"$X_2$ | B = 0")
axes[0].set_xlabel("X")
axes[0].set_ylabel("Probability density")

axes[1].hist(x_given_1, bins=50, density=True)
axes[1].set_title(r"$X_2$ | B = 1")
axes[1].set_xlabel("X")

plt.tight_layout()
plt.show()
