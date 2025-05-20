const profileData = JSON.parse(document.getElementById("profile-data").textContent);
const nicknameSearch = document.getElementById("nickname-search");
const nicknameList = document.getElementById("nickname-list");
const profileCardArea = document.getElementById("profile-card-area");

// 서버에서 context로 받은 친구/요청 상태
const friendsIds = window.friendsIds || [];
const sentRequestsIds = window.sentRequestsIds || [];
const currentUserId = window.currentUserId;

nicknameSearch.addEventListener("input", function() {
  const value = nicknameSearch.value.trim().toLowerCase();
  document.querySelectorAll(".nickname-item").forEach(function(item) {
    const nickname = item.dataset.nickname.toLowerCase();
    item.style.display = nickname.includes(value) ? "" : "none";
  });
});

nicknameList.addEventListener("click", function(e) {
  if (e.target.classList.contains("view-profile-btn")) {
    const userid = e.target.dataset.userid;
    showProfile(userid);
  }
});

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

// [NEW] 친구요청 수락/거절 (오른쪽 Accept/Reject 버튼 이벤트)
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

function showProfile(userid) {
  if (!window.isUserLoggedIn) {
    profileCardArea.innerHTML = `<div class="profile-placeholder"><b>You need to log in to view public profiles.</b></div>`;
    return;
  }
  if (parseInt(userid) === currentUserId) {
    profileCardArea.innerHTML = `<div class="profile-placeholder"><b>This is your profile.</b></div>`;
    return;
  }
  const data = profileData[userid];
  if (!data) {
    profileCardArea.innerHTML = `<div class="profile-placeholder">Profile not found.</div>`;
    return;
  }

  // 상태별 버튼 결정
  let btnHtml = "";
  if (friendsIds.includes(parseInt(userid))) {
    btnHtml = `<button class="remove-friend-btn" data-userid="${userid}" style="background:#3cb371;color:white;">Remove Friend</button>`;
  } else if (sentRequestsIds.includes(parseInt(userid))) {
    btnHtml = `<button class="cancel-request-btn" data-userid="${userid}" style="background:#fd7e14;color:white;">Cancel Request</button>`;
  } else {
    btnHtml = `<button class="add-friend-btn" data-userid="${userid}" style="background:#007bff;color:white;">Add Friend</button>`;
  }

  let html = `<div class="public-profile-card">
    <div class="public-profile-title">${data.nickname}'s Public Profile</div>
    <ul class="public-info-list">
      <li><b>Name (Nickname):</b> ${data.nickname}</li>
      <li><b>Gender:</b> ${data.gender}</li>
      <li><b>Native Language:</b> ${data.native_language}</li>`;
  if (data.nationality) html += `<li><b>Nationality:</b> ${data.nationality}</li>`;
  if (data.major) html += `<li><b>Major:</b> ${data.major}</li>`;
  if (data.personality) html += `<li><b>Personality (MBTI):</b> ${data.personality}</li>`;
  if (data.purpose) html += `<li><b>Purpose:</b> ${data.purpose}</li>`;
  if (data.bio) html += `<li><b>Bio:</b> ${data.bio}</li>`;
  if (data.instagram_id) html += `<li><b>Instagram:</b> ${data.instagram_id}</li>`;
  if (data.born_year) html += `<li><b>Born Year:</b> ${data.born_year}</li>`;
  html += `</ul>
    <div class="friend-action-area">${btnHtml}</div>
    </div>`;
  profileCardArea.innerHTML = html;
}

function handleFriendRequest(userid, action) {
  let url = "";
  let method = "POST";
  let csrftoken = getCookie('csrftoken');

  if (action === "add") url = `/accounts/friend-request/`;
  else if (action === "cancel") url = `/accounts/friend-request-cancel/`;
  else if (action === "remove") url = `/accounts/friend-remove/`;
  else return;

  fetch(url, {
    method: method,
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken
    },
    body: JSON.stringify({ userid: userid })
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        window.location.reload();
      } else {
        alert(data.msg || "Failed. Please try again.");
      }
    })
    .catch(err => {
      alert("Error: " + err);
    });
}

// [NEW] 친구 요청 수락/거절 Ajax 함수
function handleFriendRequestAction(userid, action) {
  let url = "";
  if (action === "accept") url = "/accounts/friend-accept/";
  else if (action === "reject") url = "/accounts/friend-reject/";
  else return;

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie('csrftoken')
    },
    body: JSON.stringify({ userid: userid })
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        window.location.reload();
      } else {
        alert(data.msg || "Failed. Please try again.");
      }
    })
    .catch(err => {
      alert("Error: " + err);
    });
}

// CSRF 토큰 가져오기 (Django용)
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
