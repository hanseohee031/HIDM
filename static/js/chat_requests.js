// static/js/chat_requests.js

// CSRF 토큰 읽기
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    document.cookie.split(';').forEach(c => {
      const [k,v] = c.trim().split('=');
      if (k === name) cookieValue = decodeURIComponent(v);
    });
  }
  return cookieValue;
}

document.addEventListener('DOMContentLoaded', () => {
  const csrftoken = getCookie('csrftoken');

  // 1) Request Chat 클릭 처리
  document.body.addEventListener('click', e => {
    const link = e.target.closest('.ai-match-link');
    if (!link) return;
    e.preventDefault();

    const username = link.dataset.username;
    fetch(`/accounts/chat-request/send/${username}/?ajax=1`)
      .then(r => r.text())
      .then(html => {
        document.getElementById('profile-and-form').innerHTML = html;
      })
      .catch(console.error);
  });

  // 2) 슬롯 선택 폼 제출 처리 (#chat-request-form)
  document.body.addEventListener('submit', e => {
    if (e.target.id === 'chat-request-form') {
      e.preventDefault();
      fetch(e.target.action + '?ajax=1', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
          'X-CSRFToken': csrftoken,
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: new FormData(e.target)
      })
      .then(r => r.json())
      .then(data => {
        if (data.success) window.location.reload();
      })
      .catch(console.error);
    }
  });
});
