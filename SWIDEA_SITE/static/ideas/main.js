// 정렬, 찜하기 등 JS 기능이 여기에 추가될 예정

function ajaxSearch() {
  const q = document.querySelector('input[name="q"]').value;
  const devtool = document.querySelector('select[name="devtool"]').value;
  fetch(`/search/?q=${encodeURIComponent(q)}&devtool=${encodeURIComponent(devtool)}`)
    .then(res => res.json())
    .then(data => {
      document.querySelector('.idea-list').innerHTML = data.html;
      document.querySelector('.pagination').outerHTML = data.pagination_html;
      bindIdeaCardEvents();
    });
}

function bindIdeaCardEvents() {
  document.querySelectorAll('.star-btn').forEach(btn => {
    btn.onclick = function() {
      const ideaId = this.dataset.id;
      fetch(`/idea/${ideaId}/star/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'X-Requested-With': 'XMLHttpRequest',
        },
      })
      .then(res => {
        if (res.status === 403 || res.status === 401) {
          alert('로그인 후 이용 가능합니다.');
          return null;
        }
        if (res.redirected) {
          window.location.href = res.url;
          return null;
        }
        return res.json();
      })
      .then(data => {
        if (!data) return;
        this.querySelector('.star').classList.toggle('active', data.starred);
        this.querySelector('.star-count').innerText = data.star_count;
      })
      .catch(error => {
        console.error('Error:', error);
      });
    };
  });

  document.querySelectorAll('.interest-btn').forEach(btn => {
    btn.onclick = function() {
      const ideaId = this.dataset.id;
      const action = this.dataset.action;
      fetch(`/idea/${ideaId}/interest/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'X-Requested-With': 'XMLHttpRequest',
        },
        body: new URLSearchParams({action: action}),
      })
      .then(res => res.json())
      .then(data => {
        this.parentElement.querySelector('.interest-count').innerText = data.interest;
      });
    };
  });

  document.querySelectorAll('.page-link').forEach(link => {
    link.onclick = function(e) {
      e.preventDefault();
      const page = this.dataset.page;
      const q = document.querySelector('input[name="q"]').value;
      const devtool = document.querySelector('select[name="devtool"]').value;
      fetch(`/search/?q=${encodeURIComponent(q)}&devtool=${encodeURIComponent(devtool)}&page=${page}`)
        .then(res => res.json())
        .then(data => {
          document.querySelector('.idea-list').innerHTML = data.html;
          document.querySelector('.pagination').outerHTML = data.pagination_html;
          bindIdeaCardEvents();
        });
    };
  });
}

document.addEventListener('DOMContentLoaded', function() {
  bindIdeaCardEvents();
  document.querySelector('input[name="q"]').addEventListener('input', function() {
    ajaxSearch();
  });
  document.querySelector('select[name="devtool"]').addEventListener('change', function() {
    ajaxSearch();
  });
});

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