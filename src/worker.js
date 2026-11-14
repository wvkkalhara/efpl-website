/**
 * EnerFab website Worker.
 * Static pages are served from ./public by Workers Static Assets (which also
 * applies public/_headers and public/_redirects). This script only runs for
 * /api/* (see run_worker_first in wrangler.jsonc).
 */
import { handleInquiry } from './inquiry.js';

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/api/inquiry') return handleInquiry(request, env);
    if (url.pathname.startsWith('/api/')) return new Response('Not Found', { status: 404, headers: { 'Cache-Control': 'no-store' } });
    return env.ASSETS.fetch(request);
  }
};
