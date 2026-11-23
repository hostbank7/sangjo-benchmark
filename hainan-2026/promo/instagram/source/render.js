const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const dir=process.argv[2];const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:1});
for(const f of fs.readdirSync(dir).filter(f=>f.startsWith('_')&&f.endsWith('.html')).sort()){
 await pg.goto('file://'+path.join(dir,f));await pg.evaluate(()=>document.fonts.ready);await pg.waitForTimeout(500);
 await pg.screenshot({path:path.join(dir,f.slice(1).replace('.html','.png'))});fs.unlinkSync(path.join(dir,f));}
await b.close();})();
