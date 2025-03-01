//Assume RAM is sufficient. Use with `prepare_buckets_latent_v2.py`.
//It is a compromised: Stream based library for huge JSON files are scarse. Now it is not as "pretty" as kohyas original one.
//However NodeJS process a lot more efficient than Python.

//node --max-old-space-size=131072 merge_meta_lat.js

const fs = require('fs');
const bigJson = require('big-json');
const cliProgress = require('cli-progress');

const meta_to_merge = [
    "H:/just_astolfo/meta_cap_dd_0.json",
    "H:/just_astolfo/meta_cap_dd_1.json",
    "H:/just_astolfo/meta_cap_dd_2.json",
    "H:/just_astolfo/meta_cap_dd_3.json",
];

const merged_meta = "H:/just_astolfo/meta_cap_dd_x.json";

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

    const mbar = new cliProgress.MultiBar({}, cliProgress.Presets.shades_classic);

    for (const meta_file of meta_to_merge) {
        //console.log("loadJson...");
        const j = await loadJson(meta_file);
        const sbar = mbar.create(Object.entries(j).length, 0);
        for (const [k, v] of Object.entries(j)) {
            merged[k] = { ...v, ...merged[k] };
            sbar.increment();
        }
    }
    mbar.stop();

    const sbar = new cliProgress.SingleBar({}, cliProgress.Presets.shades_classic);
    //Expect 6x entries, chunks size is unknown.
    sbar.start(Object.entries(merged).length * 6 + 1, 0);
    await writeJson(merged_meta, merged, sbar);
    //sbar.update(1);
    sbar.stop();
}

main().catch(console.error);