/* 把根目录的网页文件同步到 Capacitor 的 www/ 目录（只拷贝需要的文件） */
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const WWW = path.join(ROOT, 'www');
const FILES = ['index.html', 'data.js', 'manifest.json', 'sw.js', 'sample-course.json', 'install-calendar.html', 'calendar-sync-v1.shortcut', 'calendar-sync-v2.shortcut', 'calendar-sync-v2.1.shortcut'];
/* extract-scrape.js 源在 tools/ 下 */
const TOOLS_FILES = ['extract-scrape.js'];
const DIRS = ['icons'];

fs.mkdirSync(WWW, { recursive: true });
for (const f of FILES){
  const src = path.join(ROOT, f);
  if (fs.existsSync(src)) fs.copyFileSync(src, path.join(WWW, f));
}
for (const f of TOOLS_FILES){
  const src = path.join(__dirname, f);
  if (fs.existsSync(src)) fs.copyFileSync(src, path.join(WWW, f));
}
for (const d of DIRS){
  const src = path.join(ROOT, d);
  if (fs.existsSync(src)){
    fs.cpSync(src, path.join(WWW, d), { recursive: true });
  }
}
console.log('www/ 同步完成:', fs.readdirSync(WWW).join(', '));
