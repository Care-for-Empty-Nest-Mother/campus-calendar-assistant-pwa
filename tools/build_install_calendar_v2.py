from pathlib import Path
import base64
import hashlib

root = Path(__file__).resolve().parents[1]
shortcut = (root / 'calendar-sync-v2.shortcut').read_bytes()
b64 = base64.b64encode(shortcut).decode('ascii')
sha = hashlib.sha256(shortcut).hexdigest()

html = f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#1769aa">
<title>安装同步系统日历 v2 快捷指令</title>
<style>
*{{box-sizing:border-box}}
html,body{{margin:0;min-height:100%;background:#f2f6fa;color:#17212b;font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Helvetica Neue",sans-serif}}
body{{display:flex;align-items:center;justify-content:center;padding:24px 18px calc(24px + env(safe-area-inset-bottom))}}
main{{width:min(620px,100%);background:#fff;border-radius:24px;padding:28px 22px 24px;box-shadow:0 18px 50px rgba(24,63,98,.13);text-align:center}}
.logo{{width:72px;height:72px;border-radius:20px;margin:0 auto 14px;background:linear-gradient(145deg,#2787d4,#125da0);display:grid;place-items:center;color:#fff;font-size:38px;box-shadow:0 10px 24px rgba(23,105,170,.28)}}
h1{{font-size:25px;margin:0 0 8px;letter-spacing:-.5px}}
.lead{{margin:0 0 22px;color:#647486;font-size:15px;line-height:1.55}}
.btn{{display:block;width:100%;padding:16px 18px;border-radius:15px;background:#1769aa;color:#fff;text-decoration:none;font-size:18px;font-weight:700;box-shadow:0 9px 22px rgba(23,105,170,.25);-webkit-tap-highlight-color:transparent}}
.btn:active{{transform:scale(.985);opacity:.92}}
.btn[data-ready="0"]{{opacity:.6}}
.note{{margin:14px 0 0;color:#47647d;font-size:14px;line-height:1.5}}
.steps{{text-align:left;margin:22px 0 0;padding:16px 16px 16px 38px;border-radius:15px;background:#f6f9fc;color:#33485b;font-size:14px;line-height:1.8}}
.steps strong{{color:#17212b}}
.tip{{margin:15px 0 0;color:#76879a;font-size:12px;line-height:1.55;word-break:break-all}}
code{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}}
</style>
</head>
<body>
<main>
  <div class="logo">📅</div>
  <h1>安装同步系统日历 v2 快捷指令</h1>
  <p class="lead">文件已在页面内准备完成，不依赖网络下载，也不会下载成 HTML。</p>
  <a class="btn" id="downloadBtn" href="calendar-sync-v2.shortcut" download="calendar-sync-v2.shortcut" data-ready="0">正在准备快捷指令…</a>
  <p class="note" id="status">正在校验内置的签名文件…</p>
  <ol class="steps">
    <li>点击上方按钮，选择 <strong>存储到文件</strong>。</li>
    <li>打开 iPad 的 <strong>文件</strong> App，进入 <strong>下载</strong>。</li>
    <li>点击 <strong>calendar-sync-v2.shortcut</strong>，再选 <strong>添加快捷指令</strong>。</li>
  </ol>
  <p class="tip">文件大小 {len(shortcut):,} 字节 · SHA-256 <code>{sha}</code></p>
</main>
<script>
(function(){{
  var B64='{b64}';
  var btn=document.getElementById('downloadBtn');
  var status=document.getElementById('status');
  try{{
    var bin=atob(B64), bytes=new Uint8Array(bin.length);
    for(var i=0;i<bin.length;i++) bytes[i]=bin.charCodeAt(i);
    if(bytes.length<4||bytes[0]!==65||bytes[1]!==69||bytes[2]!==65||bytes[3]!==49) throw new Error('签名文件头无效');
    var blob=new Blob([bytes],{{type:'application/x-apple-shortcut'}});
    var url=URL.createObjectURL(blob);
    btn.href=url;
    btn.setAttribute('download','calendar-sync-v2.shortcut');
    btn.dataset.ready='1';
    btn.textContent='一键下载快捷指令';
    status.textContent='文件已就绪。点击按钮后请选择“存储到文件”。';
  }}catch(e){{
    status.textContent='文件准备失败：'+(e.message||e);
  }}
}})();
</script>
</body>
</html>
'''
(root / 'install-calendar.html').write_text(html, encoding='utf-8')
print(root / 'install-calendar.html')
