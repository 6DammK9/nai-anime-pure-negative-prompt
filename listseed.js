const folder = process.argv[2] || './';
const fs = require('fs');
const a = fs.readdirSync(folder).map(s=>s.split("-")[1]).join(",");
fs.writeFileSync(`listseed.txt`, a);