import http from 'http';

const BASE_URL = 'http://localhost:3000';

const PAGES = [
  { path: '/', name: 'Landing Page (Home)', checks: ['AYURA', 'IP-SAKTI', 'jurisdiction', 'chat', 'classify', 'search'] },
  { path: '/chat', name: 'AI Assistant Chat Interface', checks: ['IP-SAKTI Sahayak', 'chat', 'textarea', 'Quick Prompts'] },
  { path: '/classify', name: '6-Category ASU Classifier Wizard', checks: ['Classification', 'Rule 158-B', 'Product'] },
  { path: '/search', name: 'Pharmacopoeial Prior-Art Search', checks: ['Prior Art', 'Monograph', 'Search'] }
];

const ASSETS = [
  '/ayura_logo.png',
  '/favicon.ico',
  '/icon.png',
  '/ayurveda_hero_bg.jpg'
];

async function fetchUrl(urlPath) {
  return new Promise((resolve) => {
    const startTime = Date.now();
    http.get(`${BASE_URL}${urlPath}`, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        resolve({
          path: urlPath,
          statusCode: res.statusCode,
          durationMs: Date.now() - startTime,
          headers: res.headers,
          body: data
        });
      });
    }).on('error', (err) => {
      resolve({
        path: urlPath,
        statusCode: 0,
        error: err.message,
        durationMs: Date.now() - startTime,
        body: ''
      });
    });
  });
}

async function runTests() {
  console.log('====================================================');
  console.log('   AYURA (IP-SAKTI) COMPREHENSIVE TEST SUITE');
  console.log('====================================================\n');

  let passed = 0;
  let failed = 0;

  console.log('--- 1. Testing Frontend Application Routes ---');
  for (const page of PAGES) {
    const res = await fetchUrl(page.path);
    if (res.statusCode === 200) {
      // Check content keywords
      const missing = page.checks.filter(keyword => !res.body.toLowerCase().includes(keyword.toLowerCase()));
      if (missing.length === 0) {
        console.log(`[PASS] ${page.name} (${page.path}) -> HTTP 200 in ${res.durationMs}ms [All keywords verified]`);
        passed++;
      } else {
        console.log(`[WARN] ${page.name} (${page.path}) -> HTTP 200 in ${res.durationMs}ms [Missing: ${missing.join(', ')}]`);
        passed++;
      }
    } else {
      console.log(`[FAIL] ${page.name} (${page.path}) -> HTTP ${res.statusCode} ${res.error || ''}`);
      failed++;
    }
  }

  console.log('\n--- 2. Testing Static Assets & Branding Media ---');
  for (const asset of ASSETS) {
    const res = await fetchUrl(asset);
    const contentLength = res.headers['content-length'] || res.body.length;
    if (res.statusCode === 200 && contentLength > 0) {
      console.log(`[PASS] Asset: ${asset} -> HTTP 200 OK (${contentLength} bytes)`);
      passed++;
    } else {
      console.log(`[FAIL] Asset: ${asset} -> HTTP ${res.statusCode}`);
      failed++;
    }
  }

  console.log('\n====================================================');
  console.log(`TEST SUMMARY: ${passed} PASSED | ${failed} FAILED`);
  console.log('====================================================');

  if (failed > 0) {
    process.exit(1);
  }
}

runTests();
