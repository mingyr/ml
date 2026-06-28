import csv
from collections import defaultdict, Counter

A_COL = "employment_status"     # 被条件化的列
B_COL = "loan_paid_back"     # 条件列
MAX_ROWS = 19_000

# counts[b][a] = count of (A=a, B=b)
counts = defaultdict(Counter)
row_count = 0

with open("loan_dataset_20000.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)   # 自动跳过表头

    for row in reader:
        if row_count >= MAX_ROWS:
            break

        a = row[A_COL]
        b = row[B_COL]

        counts[b][a] += 1
        row_count += 1

assert row_count == MAX_ROWS, (
    f"Only read {row_count} rows, expected {MAX_ROWS}"
)

# 计算条件概率
conditional_prob = {}

for b, counter in counts.items():
    total = sum(counter.values())
    conditional_prob[b] = {
        a: cnt / total for a, cnt in counter.items()
    }

# 输出结果
for b, dist in conditional_prob.items():
    print(f"P({A_COL} | {B_COL}={b}):")
    for a, p in dist.items():
        print(f"  P({A_COL}={a} | {B_COL}={b}) = {p:.6f}")
