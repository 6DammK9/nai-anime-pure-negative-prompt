//node --max-old-space-size=131072 merge_dataset.js

const fs = require('fs');
const bigJson = require('big-json');
const cliProgress = require('cli-progress');


JSON_A = "C:/temp/tags/meta_lat_danbooru.json"
JSON_B = "C:/temp/tags/meta_lat_e621.json"

//JSON_A = "C:/temp/tags/test_lat_v3.json"
//JSON_B = "C:/temp/tags/test_lat_v3.json"

JSON_C = "C:/temp/tags/meta_lat.json"

//250225: Relative to --train_data_dir
FOLDER_A = "danbooru/"
FOLDER_B = "e621/"

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

function cast_a(k) {
    return `${FOLDER_A}${k}`
}

function cast_b(k) {
    return `${FOLDER_B}${k}`
}

async function main() {

    const mbar = new cliProgress.MultiBar({}, cliProgress.Presets.shades_classic);

    console.log("load JSON_A...");
    const ja = await loadJson(JSON_A);
    const sbara = mbar.create(Object.entries(ja).length, 0);
    for (const [k, v] of Object.entries(ja)) {
        merged[cast_a(k)] = v; //{ ...v, ...merged[k] };
        sbara.increment();
    }
    delete ja;

    console.log("load JSON_B...");
    const jb = await loadJson(JSON_B);
    const sbarb = mbar.create(Object.entries(jb).length, 0);
    for (const [k, v] of Object.entries(jb)) {
        merged[cast_b(k)] = v; //{ ...v, ...merged[k] };
        sbarb.increment();
    }
    delete jb;

    mbar.stop();

    const sbar = new cliProgress.SingleBar({}, cliProgress.Presets.shades_classic);
    //Expect 6x entries, chunks size is unknown.
    sbar.start(Object.entries(merged).length * 8 + 1, 0);
    await writeJson(JSON_C, merged, sbar);
    //sbar.update(1);
    sbar.stop();
}

main().catch(console.error);