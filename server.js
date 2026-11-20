// Minimal static file server for the Ultra OV NL website. No dependencies.
// Serves ./public with clean URLs (/privacy -> /privacy/index.html), security headers and a 404 page.
import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { extname, join, normalize, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(fileURLToPath(new URL('.', import.meta.url)), 'public');
const PORT = Number(process.env.SERVER_PORT || process.env.PORT || 8080);

const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.png': 'image/png',
  '.webp': 'image/webp',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.txt': 'text/plain; charset=utf-8',
  '.xml': 'application/xml; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
};

const SECURITY_HEADERS = {
  'Content-Security-Policy':
    "default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'none'",
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'Permissions-Policy': 'geolocation=(), camera=(), microphone=(), interest-cohort=()',
  'X-Frame-Options': 'DENY',
};

async function resolveFile(urlPath) {
  let p;
  try {
    p = decodeURIComponent(urlPath.split('?')[0]);
  } catch {
    return null;
  }
  const safe = normalize(p).replace(/^(\.\.(\/|\\|$))+/, '');
  const full = join(ROOT, safe);
  if (full !== ROOT && !full.startsWith(ROOT + sep)) return null;
  for (const candidate of [full, join(full, 'index.html'), `${full}.html`]) {
    try {
      const s = await stat(candidate);
      if (s.isFile()) return candidate;
    } catch {}
  }
  return null;
}

function cacheFor(file) {
  if (file.includes(`${sep}assets${sep}`)) return 'public, max-age=86400';
  return 'public, max-age=300';
}

const server = createServer(async (req, res) => {
  if (req.method !== 'GET' && req.method !== 'HEAD') {
    res.writeHead(405, { Allow: 'GET, HEAD', ...SECURITY_HEADERS });
    return res.end();
  }
  const url = req.url || '/';
  // /privacy/ -> /privacy (one canonical URL per page)
  if (url.length > 1 && url.endsWith('/') && !url.includes('?')) {
    res.writeHead(301, { Location: url.slice(0, -1), ...SECURITY_HEADERS });
    return res.end();
  }
  const file = await resolveFile(url);
  const status = file ? 200 : 404;
  const target = file || join(ROOT, '404.html');
  try {
    const body = await readFile(target);
    res.writeHead(status, {
      'Content-Type': TYPES[extname(target)] || 'application/octet-stream',
      'Cache-Control': status === 200 ? cacheFor(target) : 'no-store',
      ...SECURITY_HEADERS,
    });
    res.end(req.method === 'HEAD' ? undefined : body);
  } catch {
    res.writeHead(500, SECURITY_HEADERS);
    res.end('Server error');
  }
});

server.listen(PORT, '0.0.0.0', () => console.log(`Ultra OV NL website on port ${PORT}`));
