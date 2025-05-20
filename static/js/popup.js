document.addEventListener('DOMContentLoaded', () => {
  const btn = document.querySelector('.match-btn');
  if (!btn) return;

  btn.addEventListener('click', e => {
    e.preventDefault();
    // a 태그 href 속성에서 URL 가져오기
    const url = btn.getAttribute('href');
    // 팝업창 열기: 이름(chatPopup), 크기 지정
    window.open(
      url,
      'chatPopup',
      'width=500,height=600,menubar=no,toolbar=no,location=no,status=no'
    );
  });
});
