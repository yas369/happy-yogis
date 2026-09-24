/* Plate Check service worker: offline app shell, notification clicks, and
   best-effort background reminders where the browser supports Periodic
   Background Sync (Chrome on Android, installed app only). */
'use strict';

const SHELL = 'plate-check-shell-v1';
const STATE = 'plate-check-state';
const FILES = ['./', 'index.html', 'manifest.webmanifest', 'icon.svg', 'icon-192.png', 'icon-512.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(SHELL).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k.startsWith('plate-check-shell-') && k !== SHELL).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// Network first, so updates arrive immediately; the cache covers offline use.
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;
  e.respondWith(
    fetch(req)
      .then(res => {
        if (res.ok) { const copy = res.clone(); caches.open(SHELL).then(c => c.put(req, copy)); }
        return res;
      })
      .catch(() => caches.match(req, { ignoreSearch: true }).then(r => r || caches.match('index.html')))
  );
});

self.addEventListener('notificationclick', e => {
  e.notification.close();
  const url = (e.notification.data && e.notification.data.url) || './';
  e.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then(list => {
      for (const c of list) if (c.url.includes('/food-tracker/') && 'focus' in c) { c.navigate(url).catch(() => {}); return c.focus(); }
      return self.clients.openWindow(url);
    })
  );
});

function keyOf(d) {
  return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
}

async function backgroundCheck() {
  const cache = await caches.open(STATE);
  const r = await cache.match('state.json');
  if (!r) return;
  const s = await r.json();
  const firedRes = await cache.match('sw-fired.json');
  const swFired = firedRes ? await firedRes.json() : {};
  const now = new Date(), k = keyOf(now), mins = now.getHours() * 60 + now.getMinutes();
  const day = (s.days && s.days[k]) || { meals: [], total: 0 };
  const left = (s.target || 0) - (day.total || 0);
  for (const rem of s.reminders || []) {
    if (!rem.on) continue;
    const [h, m] = rem.time.split(':').map(Number);
    const due = h * 60 + m;
    const fk = k + ':' + rem.id;
    // Background sync fires irregularly, so allow a wider window than the page does.
    if (mins < due || mins > due + 90 || (s.fired && s.fired[fk]) || swFired[fk]) continue;
    swFired[fk] = true;
    if (rem.meal && day.meals.includes(rem.meal)) continue;
    const body = rem.meal
      ? (left > 0 ? left + ' kcal left today. ' : 'Already at your limit. Keep it light. ') + 'Check how hungry you are, then eat slowly.'
      : (left >= 0 ? 'The kitchen is closed for today.' : 'You are over today’s limit. No more snacks tonight.');
    await self.registration.showNotification(rem.meal ? rem.label + ' time' : 'Kitchen closed?', {
      body, tag: 'plate-check-' + rem.id, icon: 'icon-192.png', badge: 'icon-192.png', data: { url: './?add=1' },
    });
  }
  await cache.put('sw-fired.json', new Response(JSON.stringify(swFired), { headers: { 'Content-Type': 'application/json' } }));
}

self.addEventListener('periodicsync', e => {
  if (e.tag === 'meal-reminders') e.waitUntil(backgroundCheck());
});
