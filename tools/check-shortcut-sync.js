/* 统一校验：网页启动名、快捷指令构建名、安装页下载名、签名文件和 Pages 部署文件必须一致。 */
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const fail = message => { console.error('[shortcut-sync] ' + message); process.exit(1); };
const read = rel => {
  const file = path.join(ROOT, rel);
  if (!fs.existsSync(file)) fail('缺少文件：' + rel);
  return fs.readFileSync(file, 'utf8');
};

const index = read('index.html');
const runner = (index.match(/const shortcutName = '([^']+)'/) || [])[1];
if (!runner) fail('index.html 中未找到 shortcutName');

const builder = read('tools/shortcuts/build_calendar_shortcut_v2.py');
const builtName = (builder.match(/SHORTCUT_NAME = '([^']+)'/) || [])[1];
if (builtName !== runner) fail(`启动名与构建名不一致：${runner} != ${builtName}`);

const expectedFile = runner + '.shortcut';
const install = read('install-calendar.html');
const downloads = [...install.matchAll(/download="([^"]+\.shortcut)"/g)].map(m => m[1]);
if (!downloads.includes(expectedFile)) fail(`安装页下载名未匹配：期望 ${expectedFile}`);

const shortcutPath = path.join(ROOT, expectedFile);
if (!fs.existsSync(shortcutPath)) fail('缺少签名文件：' + expectedFile);
const header = fs.readFileSync(shortcutPath).subarray(0, 4).toString('ascii');
if (header !== 'AEA1') fail('签名文件头无效：' + expectedFile);

const workflow = read('.github/workflows/deploy-pwa.yml');
const copyLine = `cp ${expectedFile} dist/${expectedFile}`;
if (!workflow.includes(copyLine)) fail('Pages 部署未包含：' + copyLine);

console.log(`[shortcut-sync] OK ${runner} -> ${expectedFile}`);
