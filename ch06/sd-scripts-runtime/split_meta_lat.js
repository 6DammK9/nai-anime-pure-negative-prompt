//Assume RAM is sufficient. Use with `prepare_buckets_latent_v2.py`.
//It is a compromised: Stream based library for huge JSON files are scarse. Now it is not as "pretty" as kohyas original one.
//However NodeJS process a lot more efficient than Python.

//node --max-old-space-size=131072 split_meta_lat.js

const fs = require('fs');
const bigJson = require('big-json');
const cliProgress = require('cli-progress');

const meta_to_split = [
    "H:/danbooru2024-webp-4Mpixel/meta_cap_dd_0.json",
    "H:/danbooru2024-webp-4Mpixel/meta_cap_dd_1.json",
    "H:/danbooru2024-webp-4Mpixel/meta_cap_dd_2.json",
    "H:/danbooru2024-webp-4Mpixel/meta_cap_dd_3.json",
];

const raw_meta = "H:/danbooru2024-webp-4Mpixel/meta_cap_dd.json";

//Split by modulation. 
const split = {};

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

async function loadJson(p) {
    return new Promise((resolve, reject) => {
        const stream = fs.createReadStream(p, { encoding: 'utf-8' });
        const parser = bigJson.createParseStream();
        parser.on('data', resolve);
        parser.on('error', reject);
        stream.pipe(parser);
    })
}

async function writeJson(f, p, b) {
    return new Promise((resolve, reject) => {
        const stream = fs.createWriteStream(f, { encoding: 'utf-8' });
        stream.on('finish', resolve);
        stream.on('error', reject);

        const formatter = bigJson.createStringifyStream({ body: p });
        formatter.on('data', (chunk) => { if (b) { b.increment(); } })
        formatter.pipe(stream);
    })
}

async function main() {

    console.log("loadJson...");
    const j = await loadJson(raw_meta);

    const mod_base = meta_to_split.length;

    for (let i = 0; i < mod_base; i++)
        split[i] = {};

    const sbar = new cliProgress.SingleBar({}, cliProgress.Presets.shades_classic);
    sbar.start(Object.entries(j).length, 0);

    for (const [k, v] of Object.entries(j)) {
        const nk = parseInt(k);
        if (isNaN(nk)) continue;
        split[nk % mod_base][nk] = v;
        sbar.increment();
    }

    sbar.stop();

    const mbar = new cliProgress.MultiBar({}, cliProgress.Presets.shades_classic);
    await Promise.all([...Array(mod_base).keys()].map((i) => {
        //Expect 6x entries, chunks size is unknown.
        const sbar = mbar.create(Object.entries(split[i]).length * 6 + 1, 0);
        return writeJson(meta_to_split[i], split[i], sbar);
    }))

    mbar.stop();
}

main().catch(console.error);