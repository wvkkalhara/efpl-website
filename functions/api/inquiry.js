/**
 * POST /api/inquiry — EnerFab quote/inquiry form handler (Cloudflare Pages Function).
 *
 * Defences, in order:
 *  1. Method + origin checks (only https://enerfab.lk / www, or *.pages.dev
 *     previews when ALLOW_PREVIEW_ORIGINS="true"). Together with Turnstile
 *     this is the CSRF protection: the site has no cookies or sessions, so a
 *     forged cross-site post has no credentials to ride on and fails both
 *     the Origin check and the single-use Turnstile token.
 *  2. Body size and content-type limits.
 *  3. Honeypot field ("website") — bots that fill it get a fake success.
 *  4. Strict validation and sanitising of every field (length, charset,
 *     allow-listed "interest", link-spam limit, header-injection safe).
 *  5. Cloudflare Turnstile server-side verification (hostname + action bound).
 *  6. Rate limiting is done at the edge with a Cloudflare WAF rate-limiting
 *     rule on /api/inquiry (see SEO-SECURITY-BLUEPRINT.md).
 *
 * Environment variables (Pages > Settings > Variables and secrets):
 *  TURNSTILE_SECRET_KEY  (secret)  Turnstile secret key
 *  RESEND_API_KEY        (secret)  API key for https://resend.com (email delivery)
 *  MAIL_TO               e.g. info@enerfab.lk
 *  MAIL_FROM             e.g. "EnerFab Website <website@enerfab.lk>" (domain verified in Resend)
 *  ALLOW_PREVIEW_ORIGINS "true" to accept *.pages.dev preview origins
 */

const ALLOWED_ORIGINS = ['https://enerfab.lk', 'https://www.enerfab.lk'];
const ALLOWED_HOSTNAMES = ['enerfab.lk', 'www.enerfab.lk'];
const INTERESTS = [
  '', 'Biomass gasifiers', 'Fuelwood and biomass supply', 'Steel fabrication', 'Mini-hydro power plants',
  'Material handling', 'ESCO and energy audits', 'Wood Grab EWG 1', 'Wood Chopper DM500', 'Something else'
];
const MAX_BODY = 16 * 1024;

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' }
  });

// Plain-HTML form posts (JavaScript off) get a redirect back to the page.
const reply = (request, ok, error, status) => {
  const wantsJson = (request.headers.get('Accept') || '').includes('application/json');
  if (wantsJson) return json(ok ? { ok: true } : { ok: false, error }, ok ? 200 : status);
  return Response.redirect(new URL(ok ? '/contact/?sent=1#inquiry' : '/contact/?error=1#inquiry', request.url).toString(), 303);
};

// Remove control characters (keep newlines in the message), collapse whitespace, trim.
const clean = (v, multiline = false) => {
  let s = typeof v === 'string' ? v : '';
  s = s.normalize('NFC').replace(multiline ? /[\u0000-\u0009\u000B-\u001F\u007F  ]/g : /[\u0000-\u001F\u007F  ]/g, ' ');
  s = multiline ? s.replace(/[ \t]+/g, ' ').replace(/\n{3,}/g, '\n\n') : s.replace(/\s+/g, ' ');
  return s.trim();
};
const esc = (s) => s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const EMAIL_RE = /^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+$/;

function originAllowed(origin, env) {
  if (!origin) return false;
  if (ALLOWED_ORIGINS.includes(origin)) return true;
  if (env.ALLOW_PREVIEW_ORIGINS === 'true') {
    try { const u = new URL(origin); return u.protocol === 'https:' && u.hostname.endsWith('.pages.dev'); } catch { return false; }
  }
  return false;
}

async function verifyTurnstile(token, ip, env) {
  if (!env.TURNSTILE_SECRET_KEY) return { ok: false, reason: 'not-configured' };
  const body = new FormData();
  body.append('secret', env.TURNSTILE_SECRET_KEY);
  body.append('response', token);
  if (ip) body.append('remoteip', ip);
  body.append('idempotency_key', crypto.randomUUID());
  const r = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', { method: 'POST', body });
  const out = await r.json().catch(() => ({}));
  if (!out.success) return { ok: false, reason: (out['error-codes'] || []).join(',') || 'failed' };
  if (out.action && out.action !== 'inquiry') return { ok: false, reason: 'bad-action' };
  const hostOk = ALLOWED_HOSTNAMES.includes(out.hostname) || (env.ALLOW_PREVIEW_ORIGINS === 'true' && String(out.hostname).endsWith('.pages.dev'));
  if (!hostOk) return { ok: false, reason: 'bad-hostname' };
  return { ok: true };
}

export async function onRequestPost({ request, env }) {
  // 1. Origin / fetch-metadata checks
  const origin = request.headers.get('Origin');
  const site = request.headers.get('Sec-Fetch-Site');
  if (!originAllowed(origin, env) || (site && site !== 'same-origin')) return reply(request, false, 'This request was blocked.', 403);

  // 2. Size and type
  const len = Number(request.headers.get('Content-Length') || 0);
  if (len > MAX_BODY) return reply(request, false, 'Your message is too long.', 413);
  const type = (request.headers.get('Content-Type') || '').toLowerCase();
  if (!type.startsWith('multipart/form-data') && !type.startsWith('application/x-www-form-urlencoded')) return reply(request, false, 'Unsupported request.', 415);

  let form;
  try { form = await request.formData(); } catch { return reply(request, false, 'The form could not be read.', 400); }

  // 3. Honeypot: pretend success so bots learn nothing
  if (clean(form.get('website'))) return reply(request, true);

  // 4. Validate
  const data = {
    name: clean(form.get('name')),
    company: clean(form.get('company')),
    email: clean(form.get('email')).toLowerCase(),
    phone: clean(form.get('phone')),
    interest: clean(form.get('interest')),
    message: clean(form.get('message'), true)
  };
  const errors = [];
  if (data.name.length < 2 || data.name.length > 100) errors.push('name');
  if (data.company.length > 150) errors.push('company');
  if (data.email.length > 254 || !EMAIL_RE.test(data.email)) errors.push('email');
  if (data.phone.length > 40 || !/^[0-9+()\-\s.]*$/.test(data.phone)) errors.push('phone');
  if (!INTERESTS.includes(data.interest)) errors.push('interest');
  if (data.message.length < 10 || data.message.length > 3000) errors.push('message');
  if ((data.message.match(/https?:\/\//gi) || []).length > 2) errors.push('links');
  if (errors.length) return reply(request, false, 'Please check these fields: ' + errors.join(', ') + '.', 422);

  // 5. Turnstile
  const token = clean(form.get('cf-turnstile-response'));
  if (!token || token.length > 2048) return reply(request, false, 'Please complete the security check.', 400);
  const ts = await verifyTurnstile(token, request.headers.get('CF-Connecting-IP'), env);
  if (!ts.ok) return reply(request, false, ts.reason === 'not-configured' ? 'The form is not set up yet.' : 'The security check failed. Please try again.', ts.reason === 'not-configured' ? 503 : 403);

  // 6. Deliver
  if (!env.RESEND_API_KEY || !env.MAIL_FROM) return reply(request, false, 'The form is not set up yet.', 503);
  const subjectName = data.name.replace(/[\r\n]/g, ' ').slice(0, 80);
  const rows = [['Name', data.name], ['Company', data.company || '-'], ['Email', data.email], ['Phone', data.phone || '-'], ['Interested in', data.interest || '-']];
  const text = rows.map(([k, v]) => `${k}: ${v}`).join('\n') + '\n\n' + data.message;
  const htmlBody = '<table cellpadding="6">' + rows.map(([k, v]) => `<tr><th align="left">${esc(k)}</th><td>${esc(v)}</td></tr>`).join('') +
    `</table><p style="white-space:pre-wrap">${esc(data.message)}</p>`;
  const send = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: env.MAIL_FROM,
      to: [env.MAIL_TO || 'info@enerfab.lk'],
      reply_to: data.email,
      subject: `Website inquiry${data.interest ? ' – ' + data.interest : ''} – ${subjectName}`,
      text,
      html: htmlBody
    })
  });
  if (!send.ok) return reply(request, false, 'Your message could not be sent right now.', 502);
  return reply(request, true);
}

export async function onRequest({ request }) {
  // Any method other than POST
  return new Response('Method Not Allowed', { status: 405, headers: { Allow: 'POST', 'Cache-Control': 'no-store' } });
}
