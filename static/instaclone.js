document.addEventListener("DOMContentLoaded", function () {
  // Like/Unlike
  document.body.addEventListener("click", function (e) {
    if (e.target.closest(".like-btn")) {
      e.preventDefault();
      const btn = e.target.closest(".like-btn");
      const form = btn.closest("form");
      const postId = form.querySelector('input[name="post_id"]').value;
      fetch("/posts/like/", {
        method: "POST",
        headers: {
          "X-CSRFToken": getCSRFToken(),
          Accept: "application/json",
        },
        body: new URLSearchParams({ post_id: postId }),
      })
        .then((res) => res.json())
        .then((data) => {
          // Update like icon and count
          if (data.success) {
            btn.classList.toggle("liked", data.liked);
            btn.querySelector("i").className = data.liked
              ? "fas fa-heart"
              : "far fa-heart";
            const countSpan = form.parentElement.querySelector(".like-count");
            if (countSpan) countSpan.textContent = data.likes + " likes";
          }
        });
    }
    // Save/Unsave
    if (e.target.closest(".save-btn")) {
      e.preventDefault();
      const btn = e.target.closest(".save-btn");
      const form = btn.closest("form");
      const postId = form.querySelector('input[name="post_id"]').value;
      fetch("/posts/save/", {
        method: "POST",
        headers: {
          "X-CSRFToken": getCSRFToken(),
          Accept: "application/json",
        },
        body: new URLSearchParams({ post_id: postId }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            btn.classList.toggle("saved", data.saved);
            btn.querySelector("i").className =
              "fa fa-bookmark" + (data.saved ? " saved" : "");
          }
        });
    }
  });

  // AJAX comment post
  document.body.addEventListener("submit", function (e) {
    if (e.target.classList.contains("comment-form")) {
      e.preventDefault();
      const form = e.target;
      const postId = form.querySelector('input[name="post_id"]').value;
      const textInput = form.querySelector('input[name="text"]');
      const text = textInput.value.trim();
      if (!text) return;
      fetch("/posts/comment/", {
        method: "POST",
        headers: {
          "X-CSRFToken": getCSRFToken(),
          Accept: "application/json",
        },
        body: new URLSearchParams({ post_id: postId, text }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            const commentsDiv = document.getElementById("comments-" + postId);
            // Add delete button if user is owner (just posted)
            const commentHtml = `<div class='comment-box'><div><span class='comment-username'>${data.username}</span> <span class='comment-text'>${data.text}</span> <span class='comment-timestamp'>${data.created_at}</span></div><form method='post' action='/posts/comment/delete/' class='delete-comment-form'><input type='hidden' name='comment_id' value='${data.comment_id}'><button type='submit' class='btn-delete-comment' title='Delete'><i class='fa fa-trash'></i></button></form></div>`;
            commentsDiv.insertAdjacentHTML("beforeend", commentHtml);
            textInput.value = "";
          }
        });
    }
  });

  // AJAX view all comments
  document.body.addEventListener("click", function (e) {
    if (e.target.classList.contains("view-all-comments")) {
      e.preventDefault();
      const postId = e.target.getAttribute("data-post-id");
      fetch(`/posts/comments/${postId}/`, {
        method: "GET",
        headers: { Accept: "application/json" },
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            const commentsDiv = document.getElementById("comments-" + postId);
            commentsDiv.innerHTML = "";
            data.comments.forEach((c) => {
              const commentHtml = `<div class='comment-box'><span><span class='comment-username'>${c.username}</span> <span class='comment-text'>${c.text}</span></span> <span class='comment-timestamp'>${c.created_at}</span></div>`;
              commentsDiv.insertAdjacentHTML("beforeend", commentHtml);
            });
            e.target.style.display = "none";
          }
        });
    }
  });

  // AJAX comment delete
  document.body.addEventListener("click", function (e) {
    if (e.target.closest(".btn-delete-comment")) {
      e.preventDefault();
      const btn = e.target.closest(".btn-delete-comment");
      const form = btn.closest("form");
      const commentBox = btn.closest(".comment-box");
      const formData = new FormData(form);
      fetch("/posts/comment/delete/", {
        method: "POST",
        headers: {
          "X-CSRFToken": getCSRFToken(),
        },
        body: formData,
      }).then((res) => {
        if (res.ok) {
          commentBox.remove();
        }
      });
    }
  });
});

function getCSRFToken() {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, 10) === "csrftoken=") {
        cookieValue = decodeURIComponent(cookie.substring(10));
        break;
      }
    }
  }
  return cookieValue;
}
