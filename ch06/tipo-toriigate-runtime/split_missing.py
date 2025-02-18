import json

MISSING_JSON = "./empty_2023_filtered.json"
SPLIT_JSON = "./split_files_2023/missing_{}.json"

splits = 4

data_missing = None

with open(MISSING_JSON, 'r') as file:
    data_missing = json.load(file)

for i in range(splits):

    missing_id = {
        "tags": [],
        "caption": [],
        "latent": []
    }

    #missing_id["tags"] = [x for x in data_missing["tags"] if (int(x) % splits == i)]
    missing_id["caption"] = [x for x in data_missing["caption"] if (int(x) % splits == i)]
    #missing_id["latent"] = [x for x in data_missing["latent"] if (int(x) % splits == i)]

    json_object = json.dumps(missing_id, indent=2)
        
    with open(SPLIT_JSON.format(i), "w") as outfile:
        outfile.write(json_object)