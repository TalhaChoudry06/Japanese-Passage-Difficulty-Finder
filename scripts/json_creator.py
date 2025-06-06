import csv
import json

dict_from_csv = {}

with open("data/cleaned_data_no_duplicates_n1-n5.csv", encoding='utf-8') as inp:
    reader = csv.reader(inp)
    next(reader)  # skip header

    for i, rows in enumerate(reader, 1):
        if len(rows) != 4:
            print(f"Skipping line {i} due to column mismatch: {rows}")
            continue

        key = rows[0].strip()
        value = rows[3].strip()

        if key in dict_from_csv:
            if dict_from_csv[key] != value:
                print(f"Duplicate key at line {i}: {key} (was: {dict_from_csv[key]}, now: {value})")

        dict_from_csv[key] = value

print(f"Loaded {len(dict_from_csv)} unique entries.")

# ✅ Save to JSON file
with open("jlpt_dict.json", "w", encoding="utf-8") as f:
    json.dump(dict_from_csv, f, ensure_ascii=False, indent=2)

print("Dictionary saved to 'jlpt_dict.json'")
