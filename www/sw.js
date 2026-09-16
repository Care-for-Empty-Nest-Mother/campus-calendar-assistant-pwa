/* 校历小助手 Service Worker：只缓存应用壳，绝对不能用 index.html 替代文件下载。 */
const CACHE = 'xpu-keli-v15';
const ASSETS = [
  './',
  './index.html',
  './data.js',
  './manifest.json',
  './icons/apple-touch-icon.png',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/icon-512-maskable.png'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(ks => {
      const olds = ks.filter(k => k !== CACHE).map(k => caches.delete(k));
      return Promise.all(olds);
    }).then(() => self.clients.claim())
  );
});

function isAppShellNavigation(url) {
  return url.pathname.endsWith('/') || url.pathname.endsWith('/index.html');
}

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);

  /* 仅网页入口做网络优先缓存；.shortcut、安装页和普通资源不会被错误回退成 HTML。 */
  if (e.request.mode === 'navigate' && isAppShellNavigation(url)) {
    e.respondWith(
      fetch(e.request).then(res => {
        try {
          const copy = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, copy));
        } catch (err) { /* ignore */ }
        return res;
      }).catch(() => caches.match(e.request).then(h => h || caches.match('./index.html')))
    );
    return;
  }

  /* 下载文件和其它导航交给浏览器原生处理，绝不回退 index.html。 */
  if (e.request.mode === 'navigate' || url.pathname.endsWith('.shortcut')) return;

  e.respondWith(
    caches.match(e.request).then(hit => {
      if (hit) return hit;
      return fetch(e.request).then(res => {
        try {
          if (url.origin === self.location.origin) {
            const copy = res.clone();
            caches.open(CACHE).then(c => c.put(e.request, copy));
          }
        } catch (err) { /* ignore */ }
        return res;
      });
    })
  );
});
