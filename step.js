const fs = require("fs");
const step = parseFloat(process.argv[2]) || 1.0;
const full = !!(process.argv[3]) || false;

const prompts = [
    //`lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name`
    `bad, comic, cropped, error, extra, worst, lowres, speech, low`
];
let merged_prompts = [];
for (const p0 of prompts) {
    const p1 = p0.split(", ");
    for (const p of p1) {
        const pt = p.trim()
            .replace("\r\n", "")
            .replace("\n", "")
            .replace(",", "")
            .trim();
        if (!merged_prompts.includes(pt)) {
            merged_prompts.push(pt);
        }
    }
}
merged_prompts = merged_prompts.sort((a, b) => a.localeCompare(b));
console.log(merged_prompts.length);
console.log(merged_prompts);

let txt = "";
switch (true) {
    case ((step < 0) && !full):
        txt = `${''.padStart(Math.abs(step), '[')}${merged_prompts.join(", ")}${''.padStart(Math.abs(step), ']')}`; break;
    case ((step < 0) && full):
        txt = merged_prompts.map(s => `${''.padStart(Math.abs(step), '[')}${s}${''.padStart(Math.abs(step), ']')}`).join(", "); break;
    case ((step > 1) && Number.isInteger(step) && !full):
        txt = `${''.padStart(step, '{')}${merged_prompts.join(", ")}${''.padStart(step, '}')}`; break;
    case ((step > 1) && Number.isInteger(step) && full):
        txt = merged_prompts.map(s => `${''.padStart(step, '{')}${s}${''.padStart(step, '}')}`).join(", "); break;
    case ((!isNaN(step)) && full):
        txt = merged_prompts.map(s => `(${s}:${step})`).join(", "); break;
    case ((!isNaN(step)) && !full):
        txt = `(${merged_prompts.join(", ")}:${step})`; break;
    default:
        txt = merged_prompts.join(", ");
}

fs.writeFileSync(`step.txt`, txt);
