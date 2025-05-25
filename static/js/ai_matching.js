// static/js/ai_matching.js

// 기존 chat_requests.js에서 이미 쓰던 CSRF 함수 그대로 복사
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
  // — Start 버튼(AJAX) 처리
  const btnStart = document.getElementById('btn-start');
  if (btnStart) {
    btnStart.addEventListener('click', () => {
      const url = btnStart.dataset.url + '&ajax=1';
      fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
        .then(res => res.json())
        .then(json => {
          document.getElementById('recommendations-container').innerHTML = json.html;
        });
    });
  }

  // — Refresh 버튼(AJAX) 처리
  const btnRefresh = document.querySelector('.btn-refresh');
  if (btnRefresh) {
    btnRefresh.addEventListener('click', e => {
      e.preventDefault();
      const url = btnRefresh.href + '&ajax=1';
      fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
        .then(res => res.json())
        .then(json => {
          document.getElementById('recommendations-container').innerHTML = json.html;
        });
    });
  }

  // — Swap 버튼(AJAX) 처리 (이벤트 위임)
  document.body.addEventListener('click', e => {
    if (e.target.classList.contains('swap-btn')) {
      const username = e.target.dataset.username;
      fetch(`/accounts/ai-matching/swap/${username}/?ajax=1`, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': getCookie('csrftoken'),
        },
      })
        .then(res => res.json())
        .then(json => {
          const card = document.getElementById(`card-${username}`);
          if (card) card.outerHTML = json.html;
        });
    }
  });
});
