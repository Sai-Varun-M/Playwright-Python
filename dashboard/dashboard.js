/* ============================================================
   Playwright Dashboard — JavaScript Logic
   ============================================================ */

(function () {
  'use strict';

  // ── Data ─────────────────────────────────────────────────────────
  const DATA = window.REPORT_DATA || generateDemoData();
  const { summary, tests, suiteBreakdown, browserBreakdown } = DATA;

  // ── Boot ─────────────────────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', () => {
    renderKPIs();
    renderDonut();
    renderSuiteChart();
    renderBrowserChart();
    renderDurationChart();
    renderTable(tests);
    populateFilters();
    attachFilters();
    attachModal();
    document.getElementById('generated-at').textContent =
      'Generated: ' + (summary.generatedAt || new Date().toLocaleString());
  });

  // ── KPIs ──────────────────────────────────────────────────────────
  function renderKPIs() {
    animateCounter('total-count',   summary.total,    '');
    animateCounter('passed-count',  summary.passed,   '');
    animateCounter('failed-count',  summary.failed,   '');
    animateCounter('skipped-count', summary.skipped,  '');
    animateCounter('pass-rate',     summary.passRate, '%');
    animateCounter('avg-duration',  summary.avgDurationMs, 'ms');
  }

  function animateCounter(id, target, suffix) {
    const el = document.getElementById(id);
    if (!el) return;
    const duration = 900;
    const start = performance.now();
    const from = 0;
    function step(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const value = Math.round(from + (target - from) * eased);
      el.textContent = value + suffix;
      if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  // ── Chart defaults ────────────────────────────────────────────────
  Chart.defaults.color = '#8b9bbf';
  Chart.defaults.font.family = "'Inter', sans-serif";
  Chart.defaults.font.size = 12;

  // ── Donut chart ───────────────────────────────────────────────────
  function renderDonut() {
    const ctx = document.getElementById('donut-chart');
    if (!ctx) return;
    new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['Passed', 'Failed', 'Skipped'],
        datasets: [{
          data: [summary.passed, summary.failed, summary.skipped],
          backgroundColor: ['#22c55e', '#ef4444', '#f59e0b'],
          borderColor: '#161d2e',
          borderWidth: 3,
          hoverBorderWidth: 4,
          hoverOffset: 8,
        }]
      },
      options: {
        cutout: '72%',
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: ctx => ` ${ctx.label}: ${ctx.parsed} (${
                summary.total ? Math.round(ctx.parsed / summary.total * 100) : 0}%)`
            }
          }
        },
        animation: { animateRotate: true, duration: 1000 }
      }
    });
    document.getElementById('donut-center-label').textContent =
      summary.passRate + '%';
  }

  // ── Suite bar chart ───────────────────────────────────────────────
  function renderSuiteChart() {
    const ctx = document.getElementById('suite-chart');
    if (!ctx || !suiteBreakdown.length) return;
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: suiteBreakdown.map(s => s.suite),
        datasets: [
          {
            label: 'Passed',
            data: suiteBreakdown.map(s => s.passed),
            backgroundColor: 'rgba(34,197,94,0.75)',
            borderRadius: 6,
          },
          {
            label: 'Failed',
            data: suiteBreakdown.map(s => s.failed),
            backgroundColor: 'rgba(239,68,68,0.75)',
            borderRadius: 6,
          },
          {
            label: 'Skipped',
            data: suiteBreakdown.map(s => s.skipped),
            backgroundColor: 'rgba(245,158,11,0.55)',
            borderRadius: 6,
          }
        ]
      },
      options: barOptions()
    });
  }

  // ── Browser bar chart ─────────────────────────────────────────────
  function renderBrowserChart() {
    const ctx = document.getElementById('browser-chart');
    if (!ctx || !browserBreakdown.length) return;
    const icons = { chromium: '🌐', firefox: '🦊', webkit: '🧭', chrome: '🌐' };
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: browserBreakdown.map(b => (icons[b.browser] || '🌐') + ' ' + b.browser),
        datasets: [
          {
            label: 'Passed',
            data: browserBreakdown.map(b => b.passed),
            backgroundColor: 'rgba(34,197,94,0.75)',
            borderRadius: 6,
          },
          {
            label: 'Failed',
            data: browserBreakdown.map(b => b.failed),
            backgroundColor: 'rgba(239,68,68,0.75)',
            borderRadius: 6,
          }
        ]
      },
      options: barOptions()
    });
  }

  function barOptions() {
    return {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          grid: { color: 'rgba(255,255,255,0.04)' },
          ticks: { color: '#8b9bbf' },
        },
        y: {
          beginAtZero: true,
          grid: { color: 'rgba(255,255,255,0.06)' },
          ticks: { color: '#8b9bbf', precision: 0 },
        }
      },
      plugins: {
        legend: {
          labels: { color: '#8b9bbf', boxWidth: 12, padding: 14 }
        }
      },
      animation: { duration: 900 }
    };
  }

  // ── Duration chart ────────────────────────────────────────────────
  function renderDurationChart() {
    const ctx = document.getElementById('duration-chart');
    if (!ctx || !tests.length) return;
    const sorted = [...tests].sort((a, b) => b.duration - a.duration).slice(0, 20);
    const colors = sorted.map(t =>
      t.status === 'passed'  ? 'rgba(99,102,241,0.75)' :
      t.status === 'failed'  ? 'rgba(239,68,68,0.75)' :
                               'rgba(245,158,11,0.55)'
    );
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: sorted.map(t => truncate(t.name, 30)),
        datasets: [{
          label: 'Duration (ms)',
          data: sorted.map(t => t.duration),
          backgroundColor: colors,
          borderRadius: 4,
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            grid: { color: 'rgba(255,255,255,0.06)' },
            ticks: {
              color: '#8b9bbf',
              callback: v => v + 'ms'
            }
          },
          y: {
            grid: { display: false },
            ticks: {
              color: '#8b9bbf',
              font: { family: "'JetBrains Mono', monospace", size: 11 }
            }
          }
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: ctx => ` ${ctx.parsed.x}ms`
            }
          }
        },
        animation: { duration: 900 }
      }
    });
  }

  // ── Table ─────────────────────────────────────────────────────────
  let currentTests = [...tests];

  function renderTable(data) {
    const tbody = document.getElementById('table-body');
    const countEl = document.getElementById('row-count');

    if (!data.length) {
      tbody.innerHTML = '<tr><td colspan="6" class="empty-row">No tests match the current filters.</td></tr>';
      countEl.textContent = '0 tests';
      return;
    }

    tbody.innerHTML = data.map((t, i) => `
      <tr data-index="${i}">
        <td><span class="status-pill status-${t.status}">${statusIcon(t.status)} ${t.status}</span></td>
        <td><span class="test-name" title="${escapeHtml(t.name)}">${escapeHtml(truncate(t.name, 50))}</span></td>
        <td><span class="tag">${escapeHtml(t.suite)}</span></td>
        <td><span class="tag">${browserIcon(t.browser)} ${escapeHtml(t.browser)}</span></td>
        <td><span class="duration-val">${t.duration}ms</span></td>
        <td>
          ${t.error
            ? `<button class="btn-details" data-index="${i}" onclick="window.__showError(${i})">View Error</button>`
            : `<button class="btn-details" disabled>—</button>`}
        </td>
      </tr>
    `).join('');

    countEl.textContent = `${data.length} test${data.length !== 1 ? 's' : ''}`;
    currentTests = data;
  }

  // ── Modal ──────────────────────────────────────────────────────────
  function attachModal() {
    const modal    = document.getElementById('error-modal');
    const backdrop = document.getElementById('modal-backdrop');
    const closeBtn = document.getElementById('modal-close');
    const body     = document.getElementById('modal-body');
    const title    = document.getElementById('modal-title');

    window.__showError = function (index) {
      const t = currentTests[index];
      if (!t) return;
      title.textContent = `❌ ${t.name}`;
      body.textContent  = t.error || 'No error details available.';
      modal.removeAttribute('hidden');
    };

    const close = () => modal.setAttribute('hidden', '');
    closeBtn.addEventListener('click', close);
    backdrop.addEventListener('click', close);
    document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
  }

  // ── Filters ────────────────────────────────────────────────────────
  function populateFilters() {
    const suites   = [...new Set(tests.map(t => t.suite))];
    const browsers = [...new Set(tests.map(t => t.browser))];

    const suiteEl   = document.getElementById('filter-suite');
    const browserEl = document.getElementById('filter-browser');

    suites.forEach(s => {
      const opt = document.createElement('option');
      opt.value = s; opt.textContent = s;
      suiteEl.appendChild(opt);
    });

    browsers.forEach(b => {
      const opt = document.createElement('option');
      opt.value = b; opt.textContent = b;
      browserEl.appendChild(opt);
    });
  }

  function attachFilters() {
    const statusEl  = document.getElementById('filter-status');
    const suiteEl   = document.getElementById('filter-suite');
    const browserEl = document.getElementById('filter-browser');
    const searchEl  = document.getElementById('search-input');

    const apply = () => {
      const status  = statusEl.value;
      const suite   = suiteEl.value;
      const browser = browserEl.value;
      const query   = searchEl.value.toLowerCase();

      const filtered = tests.filter(t =>
        (status  === 'all' || t.status  === status)  &&
        (suite   === 'all' || t.suite   === suite)   &&
        (browser === 'all' || t.browser === browser) &&
        (!query  || t.name.toLowerCase().includes(query))
      );
      renderTable(filtered);
    };

    [statusEl, suiteEl, browserEl].forEach(el => el.addEventListener('change', apply));
    searchEl.addEventListener('input', apply);
  }

  // ── Helpers ────────────────────────────────────────────────────────
  function statusIcon(s) {
    return s === 'passed' ? '✅' : s === 'failed' ? '❌' : '⏭️';
  }

  function browserIcon(b) {
    const m = { chromium: '🌐', firefox: '🦊', webkit: '🧭', chrome: '🌐' };
    return m[b] || '🌐';
  }

  function truncate(str, max) {
    return str.length > max ? str.slice(0, max) + '…' : str;
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  // ── Demo data (shown when no data.js is present) ──────────────────
  function generateDemoData() {
    const suites   = ['smoke', 'e2e', 'api'];
    const browsers = ['chromium', 'firefox', 'webkit'];
    const statuses = ['passed', 'passed', 'passed', 'passed', 'failed', 'skipped'];
    const names = [
      'test_home_page_loads', 'test_valid_login', 'test_invalid_username',
      'test_navigate_to_checkboxes', 'test_select_option_1', 'test_get_all_posts',
      'test_create_post', 'test_update_post', 'test_delete_post',
      'test_site_is_responsive', 'test_logout_after_login', 'test_toggle_checkbox_on',
    ];

    const ts = [];
    names.forEach(name => {
      browsers.forEach(browser => {
        const suite  = name.includes('post') || name.includes('get') ? 'api' : name.includes('login') ? 'e2e' : 'smoke';
        const status = statuses[Math.floor(Math.random() * statuses.length)];
        ts.push({ id: `${suite}::${name}::${browser}`, name, suite, browser, status,
                  duration: Math.floor(Math.random() * 3000) + 100, error: status === 'failed' ? 'AssertionError: Expected "Welcome" in heading, got "Error"' : '' });
      });
    });

    const passed  = ts.filter(t => t.status === 'passed').length;
    const failed  = ts.filter(t => t.status === 'failed').length;
    const skipped = ts.filter(t => t.status === 'skipped').length;
    const total   = ts.length;

    const suiteMap = {};
    ts.forEach(t => {
      if (!suiteMap[t.suite]) suiteMap[t.suite] = { suite: t.suite, passed: 0, failed: 0, skipped: 0, total: 0 };
      suiteMap[t.suite][t.status]++;
      suiteMap[t.suite].total++;
    });

    const browserMap = {};
    ts.forEach(t => {
      if (!browserMap[t.browser]) browserMap[t.browser] = { browser: t.browser, passed: 0, failed: 0, total: 0 };
      if (t.status !== 'skipped') browserMap[t.browser][t.status]++;
      browserMap[t.browser].total++;
    });

    return {
      summary: {
        total, passed, failed, skipped,
        passRate: Math.round(passed / total * 100),
        totalDurationMs: ts.reduce((a, t) => a + t.duration, 0),
        avgDurationMs: Math.round(ts.reduce((a, t) => a + t.duration, 0) / total),
        generatedAt: new Date().toLocaleString() + ' (demo data)'
      },
      tests: ts,
      suiteBreakdown: Object.values(suiteMap),
      browserBreakdown: Object.values(browserMap),
    };
  }
})();
