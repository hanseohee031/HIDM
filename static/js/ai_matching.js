// static/js/ai_matching.js

// CSRF 토큰 함수 (chat_requests.js에서 그대로 가져옴)
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    document.cookie.split(';').forEach(cookie => {
      const [key, value] = cookie.trim().split('=');
      if (key === name) cookieValue = decodeURIComponent(value);
    });
  }
  return cookieValue;
}

document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('recommendations-container');

  // — Start 버튼(AJAX) 처리
  const btnStart = document.getElementById('btn-start');
  if (btnStart) {
    btnStart.addEventListener('click', () => {
      // UI 업데이트
      btnStart.disabled = true;
      btnStart.textContent = 'Loading…';
      container.innerHTML = '<p>Loading recommendations…</p>';

      // AJAX 요청
      const url = btnStart.dataset.url + '&ajax=1';
      fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
        .then(res => res.json())
        .then(json => {
          container.innerHTML = json.html;
        })
        .catch(() => {
          container.innerHTML = '<p class="error">Failed to load recommendations.</p>';
        });
    });
  }

  // — Refresh 버튼(AJAX) 처리
  const btnRefresh = document.querySelector('.btn-refresh');
  if (btnRefresh) {
    btnRefresh.addEventListener('click', e => {
      e.preventDefault();
      // UI 업데이트
      btnRefresh.textContent = 'Loading…';
      container.innerHTML = '<p>Loading recommendations…</p>';

      // AJAX 요청
      const url = btnRefresh.href + '&ajax=1';
      fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
        .then(res => res.json())
        .then(json => {
          container.innerHTML = json.html;
        })
        .catch(() => {
          container.innerHTML = '<p class="error">Failed to refresh recommendations.</p>';
        });
    });
  }

  // — Swap 버튼(AJAX) 처리 (이벤트 위임)
  document.body.addEventListener('click', e => {
    if (e.target.classList.contains('swap-btn')) {
      const btn = e.target;
      const username = btn.dataset.username;
      const card = document.getElementById(`card-${username}`);

      // UI 업데이트
      btn.disabled = true;
      btn.textContent = 'Loading…';
      if (card) card.innerHTML = '<p>Loading…</p>';

      // AJAX 요청
      fetch(`/accounts/ai-matching/swap/${username}/?ajax=1`, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': getCookie('csrftoken'),
        },
      })
      .then(res => res.json())
      .then(json => {
        if (card) card.outerHTML = json.html;
      })
      .catch(() => {
        if (card) card.innerHTML = '<p class="error">Swap failed.</p>';
      });
    }
  });
});
