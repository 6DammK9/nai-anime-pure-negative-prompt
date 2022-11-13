const fs = require("fs");
const step = parseFloat(process.argv[2]) || 1.0;
const full = !!(process.argv[3]) || false;

const prompts = [
    //    `
    //lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name
    //`,
    //`
    //lowres, worst quality, low quality, normal quality, 
    //bad_anatomy, bad_feet, bad_hands, bad_proportions, bad_perspective, 
    //extra, speech_bubble, english_text, text_focus, error, no_humans, comic, 
    //cropped, cropped_legs, outside_border, cropped_torso, cropped_shoulders, cropped_arms, cropped_head
    //`,
    `bad, comic, cropped, error, extra, worst, lowres, speech, low, normal`

    /**
        `
    ugly, pregnant, vore, duplicate, long arms, 
    morbid, mutilated, tranny, trans, trannsexual, hermaphrodite, extra fingers, 
    fused fingers, too many fingers, long neck, mutated hands, 
    poorly drawn hands, poorly drawn face, 
    mutation, deformed, blurry, bad anatomy, 
    bad proportions, malformed limbs, extra limbs, 
    cloned face, disfigured, more than 2 nipples, gross proportions, 
    missing arms, missing legs, extra arms, extra legs
    `,
        ` 
    lowres, worst quality, low quality, normal quality, ugly, blurry, 
    text, error, extra digit, fewer digits, jpeg artifacts, signature, watermark, username, cropped, duplicate, 
    bad anatomy, mutilated, mutation, deformed, bad proportions, extra limbs, more than 2 nipples, more than 1 head, gross proportions, pregnant, morbid, vore, malformed limbs, 
    poorly drawn face, cloned face, disfigured, long neck, 
    bad hands, missing fingers, extra fingers, mutated hands, poorly drawn hands, fused fingers, too many fingers, 
    missing arms, extra arms, long arms, 
    bad feet, missing legs, extra legs, 
    tranny, trans, trannsexual, hermaphrodite, out of frame
    `,
        `
    lowres, blurry, worst quality, low quality, normal quality, 
    bad anatomy, disfigured, deformed, mutation, mutilated, ugly, totem pole, 
    poorly drawn face, cloned face, several faces, 
    long neck, mutated hands, bad hands, poorly drawn hands, 
    extra limbs, malformed limbs, missing arms, 
    missing fingers, extra fingers, fused fingers, too many fingers, 
    missing legs, extra legs, 
    extra digit, fewer digits, 
    glitchy, cropped, jpeg artifacts, signature, watermark, username, text, error
    `
    **/
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
