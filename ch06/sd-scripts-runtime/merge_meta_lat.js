//Assume RAM is sufficient. Use with `prepare_buckets_latent_v2.py`.

const meta_to_merge = [
    "F:/just_astolfo/meta_lat_sd1_0.json",
    "F:/just_astolfo/meta_lat_sd1_1.json",
    "F:/just_astolfo/meta_lat_sd1_2.json",
    "F:/just_astolfo/meta_lat_sd1_3.json",
];

const merged_meta = "F:/just_astolfo/meta_lat_sd1_x.json";

const merged = {};

const sample = {
    "1176244": {
        "tags": "",
        "captions": "",
        "train_resolution": [
            768,
            1024
        ]
    }
};

const fs = require("fs").promises;

async function loadJson(p) {
    const s = await fs.readFile(p, "utf-8");
    //console.log(s);
    return JSON.parse(s);
}

async function main() {

    for (const meta_file of meta_to_merge) {
        const j = await loadJson(meta_file);
        for (const [k, v] of Object.entries(j)) {
            merged[k] = { ...v, ...merged[k] };
        }
    }

    await fs.writeFile(merged_meta, JSON.stringify(merged, null, 2), "utf-8")
}

main().catch(console.error);