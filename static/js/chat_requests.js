// static/js/chat_requests.js
document.addEventListener('DOMContentLoaded', () => {
  // 1) 추천 목록 클릭 처리 (.ai-match-link)
  document.body.addEventListener('click', e => {
    const link = e.target.closest('.ai-match-link');
    if (!link) return;      // .ai-match-link 가 아니면 무시
    e.preventDefault();
    const username = link.dataset.username;
    fetch(`/accounts/chat-request/send/${username}/?ajax=1`)
      .then(res => res.text())
      .then(html => {
        document.getElementById('profile-and-form').innerHTML = html;
      })
      .catch(err => console.error('Fetch request error:', err));
  });

  // 2) AJAX 폼 제출 처리 (#chat-request-form)
  document.body.addEventListener('submit', e => {
    if (e.target.id === 'chat-request-form') {
      e.preventDefault();
      fetch(e.target.action + '?ajax=1', {
        method: 'POST',
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        body: new FormData(e.target)
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          // 성공 시 요청 목록으로 이동
          window.location.reload();
        } else {
          // 실패 시에는 필요에 따라 에러 메시지 표시
          console.error('Chat request failed:', data);
        }
      })
      .catch(error => console.error('Chat request error:', error));
    }
  });
});
