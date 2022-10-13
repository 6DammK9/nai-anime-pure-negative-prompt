const area = 512 * 512;
const a1 = process.argv[2] || 1;
const a2 = process.argv[3] || 1;
const ar = a1 / a2 * 1.0;
//ar x^2 +(-512*512) = 0
const x = Math.sqrt(4 * ar * area) / (2 * ar);
console.log([Math.floor(ar * x), Math.floor(x)]);
