# The 12M dataset. #

Idea: 2 folders, then make keys like "booru/123456" and "e621/123456".

Result: Great success.

I was thinking to "decompress 1ktar" to `/dev/shm` since I have many RAM

Now I have chosen a single CPU platform which I need to decompress everything eventually.

```log
> const fs = require('fs');
undefined
> console.log(fs.readdirSync("./dataset").length);
2
> console.log(fs.readdirSync("./dataset/danbooru").length);
8005010
> console.log(fs.readdirSync("./dataset/e621").length);
4441660
> 8005010 + 4441660
12446670
```

```log
>python chk.py
12446670
```