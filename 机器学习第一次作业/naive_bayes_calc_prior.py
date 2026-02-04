import csv
from collections import Counter

EXPECTED_TOTAL = 20_000
COUNT_PREFIX = 19_000
COLUMN_NAME = "loan_paid_back"

counter = Counter()
total_count = 0

with open("loan_dataset_20000.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for line_no, row in enumerate(reader, start=2):  # header = line 1
        raw = row[COLUMN_NAME]

        # type enforcement
        try:
            v = int(raw)
        except ValueError:
            raise ValueError(f"Non-integer value '{raw}' at line {line_no}")

        # domain enforcement
        if v not in (0, 1):
            raise ValueError(
                f"Invalid binary value {v} at line {line_no} (expected 0 or 1)"
            )

        total_count += 1

        # only count first 19000
        if total_count <= COUNT_PREFIX:
            counter[v] += 1

# cardinality check
assert total_count == EXPECTED_TOTAL, (
    f"Expected {EXPECTED_TOTAL} rows, got {total_count}"
)

# results
count_0 = counter[0]
count_1 = counter[1]

print(f"First {COUNT_PREFIX} instances:")
print(f"  value 0: {count_0}")
print(f"  value 1: {count_1}")
print(f"  total  : {count_0 + count_1}")

print(f"Prior probability for C = 0 is {count_0 / 19000}")
print(f"Prior probability for C = 1 is {count_1 / 19000}")
