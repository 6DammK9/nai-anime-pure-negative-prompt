const { readFileSync, writeFileSync } = require("fs");
const fIn = process.argv[2] || "./logs/result.json";
const fEnc = "utf-8";
const mK0 = "__metadata__";
const mK1 = ["sd_merge_recipe", "sd_merge_models"];
const cN = "custom_name";
const sIn = readFileSync(fIn, fEnc);
const sTrimmed = sIn.split("\r\n").slice(1).join("\r\n");
const jIn = JSON.parse(sTrimmed);
const jOut = jIn;
for (const mK2 of mK1)
    jOut[mK0][mK2] = JSON.parse(jIn[mK0][mK2]);
const modelName = jIn[mK0][mK1[0]][cN];
const fOut = process.argv[3] || `./logs/result-${modelName}.json`;
writeFileSync(fOut, JSON.stringify(jOut, null, 4), fEnc);