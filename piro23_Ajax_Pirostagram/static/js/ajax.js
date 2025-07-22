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
const csrftoken = getCookie('csrftoken');

const likeButtons = document.querySelectorAll('.like-btn');

likeButtons.forEach(button => {
    button.addEventListener('click', function (event) {
        const likeButton = event.target.closest('.like-btn');
        const postId = likeButton.dataset.postId;

        fetch(`/like/${postId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            const postCard = likeButton.closest('.post-card');
            const likeCountSpan = postCard.querySelector('.like-count');

            likeCountSpan.textContent = data.like_count;

            const likeIcon = likeButton.querySelector('i');
            likeIcon.classList.add('fas', 'text-danger'); 
            setTimeout(() => {
                likeIcon.classList.remove('fas', 'text-danger'); 
            }, 300);
        });
    });
});


const commentForms = document.querySelectorAll('.comment-form');

commentForms.forEach(form => {
    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const postId = event.target.dataset.postId;
        const contentInput = event.target.querySelector('input[name="content"]');
        const content = contentInput.value;

        if (!content) {
            alert('댓글 내용을 입력하세요.');
            return;
        }

        fetch(`/comment/add/${postId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ content: content }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'ok') {
                const commentList = document.querySelector(`#post-${postId} .comment-list`);
                const newComment = document.createElement('div');
                newComment.classList.add('comment-item');
                newComment.id = `comment-${data.comment.id}`;
                newComment.innerHTML = `
                    <div>
                        <span class="comment-author">${data.comment.author}</span>
                        <span class="comment-content">${data.comment.content}</span>
                    </div>
                    <button class="delete-comment-btn" data-comment-id="${data.comment.id}">×</button>
                `;
                commentList.appendChild(newComment);
                contentInput.value = '';
            } else {
                alert('댓글 작성에 실패했습니다.');
            }
        });
    });
});

const feedContainer = document.querySelector('.feed');

feedContainer.addEventListener('click', function(event) {
    if (event.target.matches('.delete-comment-btn')) {
        const commentId = event.target.dataset.commentId;

        if (confirm('정말로 이 댓글을 삭제하시겠습니까?')) {
            fetch(`/comment/delete/${commentId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'ok') {
                    const commentElement = document.querySelector(`#comment-${commentId}`);
                    commentElement.remove();
                } else if (data.status === 'forbidden') {
                    alert('삭제할 권한이 없습니다.');
                } else {
                    alert('댓글 삭제에 실패했습니다.');
                }
            });
        }
    }
});

const storyModal = document.getElementById('story-modal');
const storyImage = document.getElementById('story-image');
const storyProgressBar = document.getElementById('story-progress-bar');
const storyPrevBtn = document.getElementById('story-prev-btn');
const storyNextBtn = document.getElementById('story-next-btn');

let currentUserStories = [];
let currentStoryIndex = 0;

function showStory(index) {
    storyImage.src = currentUserStories[index].image_url;
    updateProgressBar(index);
}

function updateProgressBar(index) {
    storyProgressBar.innerHTML = ''; 
    currentUserStories.forEach((_, i) => {
        const segment = document.createElement('div');
        segment.classList.add('progress-segment');
        if (i === index) {
            segment.classList.add('active');
        }
        storyProgressBar.appendChild(segment);
    });
}

function openStoryModal() {
    storyModal.style.display = 'flex';
    showStory(currentStoryIndex);
}

function closeStoryModal() {
    storyModal.style.display = 'none';
    currentUserStories = [];
    currentStoryIndex = 0;
}

document.querySelector('.story-bar').addEventListener('click', function(event) {
    const storyItem = event.target.closest('.story-item');
    if (storyItem) {
        const userId = storyItem.dataset.userId;
        fetch(`/stories/${userId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.length > 0) {
                    currentUserStories = data;
                    currentStoryIndex = 0;
                    openStoryModal();
                }
            });
    }
});

storyNextBtn.addEventListener('click', () => {
    if (currentStoryIndex < currentUserStories.length - 1) {
        currentStoryIndex++;
        showStory(currentStoryIndex);
    } else {
        closeStoryModal(); 
    }
});

storyPrevBtn.addEventListener('click', () => {
    if (currentStoryIndex > 0) {
        currentStoryIndex--;
        showStory(currentStoryIndex);
    }
});

storyModal.querySelector('.story-close-btn').addEventListener('click', closeStoryModal);
storyModal.addEventListener('click', (event) => {
    if (event.target === storyModal) { 
        closeStoryModal();
    }
});
