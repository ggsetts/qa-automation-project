/**
 * Cloudflare Worker — Contact Form Proxy
 *
 * Verifies Cloudflare Turnstile token before forwarding form data to Formspree.
 * Rejects requests without a valid token, protecting Formspree's 50/month quota.
 *
 * Environment variables (set in Cloudflare dashboard):
 *   TURNSTILE_SECRET_KEY  — from Turnstile setup
 *   FORMSPREE_ENDPOINT    — e.g. https://formspree.io/f/xyzabcde
 *   ALLOWED_ORIGIN        — your site origin, e.g. https://acmedist.example.com
 */

export default {
  async fetch(request, env) {
    // CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: corsHeaders(env.ALLOWED_ORIGIN),
      });
    }

    if (request.method !== 'POST') {
      return jsonResponse(405, { error: 'Method not allowed' }, env.ALLOWED_ORIGIN);
    }

    try {
      const formData = await request.formData();

      // Extract and verify Turnstile token
      const token = formData.get('cf-turnstile-response');
      if (!token) {
        return jsonResponse(400, { error: 'Missing Turnstile token' }, env.ALLOWED_ORIGIN);
      }

      const turnstileResult = await fetch(
        'https://challenges.cloudflare.com/turnstile/v0/siteverify',
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: new URLSearchParams({
            secret: env.TURNSTILE_SECRET_KEY,
            response: token,
            remoteip: request.headers.get('CF-Connecting-IP') || '',
          }),
        }
      );

      const turnstileData = await turnstileResult.json();

      if (!turnstileData.success) {
        return jsonResponse(403, { error: 'Turnstile verification failed' }, env.ALLOWED_ORIGIN);
      }

      // Remove Turnstile token before forwarding to Formspree
      formData.delete('cf-turnstile-response');

      // Forward to Formspree
      const formspreeResponse = await fetch(env.FORMSPREE_ENDPOINT, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
        },
        body: formData,
      });

      if (!formspreeResponse.ok) {
        return jsonResponse(502, { error: 'Form service error' }, env.ALLOWED_ORIGIN);
      }

      return jsonResponse(200, { success: true }, env.ALLOWED_ORIGIN);
    } catch (err) {
      return jsonResponse(500, { error: 'Internal error' }, env.ALLOWED_ORIGIN);
    }
  },
};

function corsHeaders(origin) {
  return {
    'Access-Control-Allow-Origin': origin || '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };
}

function jsonResponse(status, body, origin) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      'Content-Type': 'application/json',
      ...corsHeaders(origin),
    },
  });
}
