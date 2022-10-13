const fs = require("fs");
const step = process.argv[2] || 1.0;
const prompts = "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name"
fs.writeFileSync(`step.txt`, prompts.split(", ").map(s => `(${s}:${step})`).join(", "));