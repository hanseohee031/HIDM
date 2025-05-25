// static/js/chat_requests.js
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.ai-match-link').forEach(link => {
    link.addEventListener('click', e => {
      e.preventDefault();
      const username = link.dataset.username;
      fetch(`/accounts/chat-request/send/${username}/?ajax=1`)
        .then(res => res.text())
        .then(html => {
          document.getElementById('profile-and-form').innerHTML = html;
        });
    });
  });

  document.body.addEventListener('submit', e => {
    if (e.target.id === 'chat-request-form') {
      e.preventDefault();
      fetch(e.target.action + '?ajax=1', {
        method: 'POST',
        headers: {'X-Requested-With': 'XMLHttpRequest'},
        body: new FormData(e.target)
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) window.location.href = '/accounts/chat-requests/';
      });
    }
  });
});
