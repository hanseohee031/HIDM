// static/js/find_friends.js

// 1) 서버에서 전달된 JSON 파싱
const profileData = JSON.parse(document.getElementById("profile-data").textContent);

// 2) DOM 요소 참조
const nicknameSearch    = document.getElementById("nickname-search");
const nicknameList      = document.getElementById("nickname-list");
const profileCardArea   = document.getElementById("profile-card-area");

// 3) 친구/요청 상태 (서버에서 window 변수로 세팅)
const friendsIds        = window.friendsIds || [];
const sentRequestsIds   = window.sentRequestsIds || [];
const currentUserId     = window.currentUserId;

// 4) 검색 입력 이벤트: nickname 필터링
nicknameSearch.addEventListener("input", function() {
  const value = nicknameSearch.value.trim().toLowerCase();
  document.querySelectorAll(".nickname-item").forEach(item => {
    item.style.display = item.dataset.nickname.toLowerCase().includes(value) ? "" : "none";
  });
});

// 5) 리스트 클릭 이벤트: View Profile 버튼
nicknameList.addEventListener("click", function(e) {
  if (e.target.classList.contains("view-profile-btn")) {
    showProfile(e.target.dataset.userid);
  }
});

// 6) 프로필 카드 내 버튼(친구추가/취소/삭제) 이벤트
profileCardArea.addEventListener("click", function(e) {
  if (e.target.classList.contains("add-friend-btn")) {
    handleFriendRequest(e.target.dataset.userid, "add");
  } else if (e.target.classList.contains("cancel-request-btn")) {
    handleFriendRequest(e.target.dataset.userid, "cancel");
  } else if (e.target.classList.contains("remove-friend-btn")) {
    if (confirm("Are you sure you want to remove this friend?")) {
      handleFriendRequest(e.target.dataset.userid, "remove");
    }
  }
});

// 7) 오른쪽 Friend Requests 섹션: Accept/Reject
const friendRequestsList = document.getElementById("friend-requests-list");
if (friendRequestsList) {
  friendRequestsList.addEventListener("click", function(e) {
    if (e.target.classList.contains("accept-friend-btn")) {
      handleFriendRequestAction(e.target.dataset.friendid, "accept");
    } else if (e.target.classList.contains("reject-friend-btn")) {
      handleFriendRequestAction(e.target.dataset.friendid, "reject");
    }
  });
}

/**
 * 프로필 카드 렌더링
 */
function showProfile(userid) {
  // 로그인 필요
  if (!window.isUserLoggedIn) {
    profileCardArea.innerHTML = `
      <div class="profile-placeholder">
        <b>You need to log in to view public profiles.</b>
      </div>`;
    return;
  }
  // 본인 프로필일 때
  if (parseInt(userid) === currentUserId) {
    profileCardArea.innerHTML = `
      <div class="profile-placeholder">
        <b>This is your profile.</b>
      </div>`;
    return;
  }

  const data = profileData[userid];
  if (!data) {
    profileCardArea.innerHTML = `
      <div class="profile-placeholder">
        Profile not found.
      </div>`;
    return;
  }

  // 1) 버튼 결정 로직
  let btnHtml = "";
  if (friendsIds.includes(parseInt(userid))) {
    btnHtml = `<button class="remove-friend-btn" data-userid="${userid}" style="background:#3cb371;color:white;">Remove Friend</button>`;
  } else if (sentRequestsIds.includes(parseInt(userid))) {
    btnHtml = `<button class="cancel-request-btn" data-userid="${userid}" style="background:#fd7e14;color:white;">Cancel Request</button>`;
  } else {
    btnHtml = `<button class="add-friend-btn" data-userid="${userid}" style="background:#007bff;color:white;">Add Friend</button>`;
  }

  // 2) 카드 HTML 조립
  let html = `
    <div class="public-profile-card">
      <div class="public-profile-title">${data.nickname}'s Public Profile</div>
      <ul class="public-info-list">
        <li><b>Name (Nickname):</b> ${data.nickname}</li>
        <li><b>Gender:</b> ${data.gender}</li>
        <li><b>Native Language:</b> ${data.native_language}</li>`;

  // Advanced Profile (공개된 항목만)
  if (data.nationality)   html += `<li><b>Nationality:</b> ${data.nationality}</li>`;
  if (data.major)         html += `<li><b>Major:</b> ${data.major}</li>`;
  if (data.personality)   html += `<li><b>Personality (MBTI):</b> ${data.personality}</li>`;
  if (data.born_year)     html += `<li><b>Born Year:</b> ${data.born_year}</li>`;

  // ★ Interests 추가
  if (data.interests && data.interests.length) {
    html += `<li><b>Interests:</b> ${data.interests.join(', ')}</li>`;
  }

  html += `
      </ul>
      <div class="friend-action-area">${btnHtml}</div>
    </div>`;

  profileCardArea.innerHTML = html;
}

/**
 * 친구 요청 / 취소 / 삭제 Ajax 처리
 */
function handleFriendRequest(userid, action) {
  let url = "";
  const csrftoken = getCookie('csrftoken');

  if (action === "add")    url = "/accounts/friend-request/";
  else if (action === "cancel") url = "/accounts/friend-request-cancel/";
  else if (action === "remove") url = "/accounts/friend-remove/";
  else return;

  fetch(url, {
    method: "POST",
    headers: {"Content-Type":"application/json","X-CSRFToken":csrftoken},
    body: JSON.stringify({ userid })
  })
  .then(r => r.json())
  .then(data => data.success ? window.location.reload() : alert(data.msg || "Failed"))
  .catch(err => alert("Error: "+err));
}

/**
 * 친구 요청 수락 / 거절 Ajax 처리
 */
function handleFriendRequestAction(userid, action) {
  let url = "";
  if (action === "accept") url = "/accounts/friend-accept/";
  else if (action === "reject") url = "/accounts/friend-reject/";
  else return;

  fetch(url, {
    method: "POST",
    headers: {"Content-Type":"application/json","X-CSRFToken":getCookie('csrftoken')},
    body: JSON.stringify({ userid })
  })
  .then(r => r.json())
  .then(data => data.success ? window.location.reload() : alert(data.msg || "Failed"))
  .catch(err => alert("Error: "+err));
}

/**
 * Django CSRF 토큰 읽기 유틸
 */
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie) {
    document.cookie.split(';').forEach(c => {
      c = c.trim();
      if (c.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(c.substring(name.length+1));
      }
    });
  }
  return cookieValue;
}
