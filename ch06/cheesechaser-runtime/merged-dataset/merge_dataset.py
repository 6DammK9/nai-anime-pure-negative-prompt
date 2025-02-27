import json

JSON_A = "C:/temp/tags/meta_lat_danbooru.json"
JSON_B = "C:/temp/tags/meta_lat_e621.json"

JSON_C = "C:/temp/tags/meta_lat.json"

#250225: Relative to --train_data_dir
FOLDER_A = "danbooru/"
FOLDER_B = "e621/"

merged = {}

def cast_a(k):
    return f"{FOLDER_A}{k}"

def cast_b(k):
    return f"{FOLDER_B}{k}"

print(f"Loading JSON_A")

with open(JSON_A, 'r') as file:
    data = json.load(file)
    merged.update({cast_a(k):v for (k,v) in data.items()})

print(f"Loading JSON_B")

with open(JSON_B, 'r') as file:
    data = json.load(file)
    merged.update({cast_b(k):v for (k,v) in data.items()})

print(f"Making output")

# Align to actual metadata json.
output = json.dumps(merged, indent=2)

print(f"Writing output")

with open(JSON_C, "w") as outfile:
    outfile.write(output)