class Posts {
  constructor() {
    this.setupEventListeners();
  }

  setupEventListeners() {
    document.getElementById("posts-list").addEventListener("click", (e) => {
      const postCard = e.target.closest(".post-card");
      if (postCard) {
        const postId = postCard.dataset.id;
        window.router.navigate("post", { id: postId });
      }
    });

    document.getElementById("create-post-btn").addEventListener("click", () => {
      window.router.navigate("create-post");
    });

    document
      .getElementById("create-post-form")
      .addEventListener("submit", (e) => this.handleCreatePost(e));
  }

  async handleCreatePost(e) {
    e.preventDefault();
    const title = e.target.title.value;
    const content = e.target.content.value;

    try {
      const query = `
                mutation {
                    createPost(title: "${title}", content: "${content}") {
                        id
                        title
                        content
                        author {
                            username
                        }
                    }
                }
            `;

      await window.auth.graphqlRequest(query);
      window.auth.showNotification("Post created successfully!", "success");
      e.target.reset();
      window.router.navigate("posts");
    } catch (error) {
      window.auth.showNotification(error.message, "error");
    }
  }

  async fetchPosts() {
    try {
      const query = `
                query {
                    posts {
                        id
                        title
                        content
                        author {
                            username
                        }
                    }
                }
            `;

      const response = await window.auth.graphqlRequest(query);
      return response.data.posts;
    } catch (error) {
      window.auth.showNotification(error.message, "error");
      return [];
    }
  }

  async fetchPost(id) {
    try {
      const query = `
                query {
                    post(id: "${id}") {
                        id
                        title
                        content
                        author {
                            username
                        }
                    }
                }
            `;

      const response = await window.auth.graphqlRequest(query);
      return response.data.post;
    } catch (error) {
      window.auth.showNotification(error.message, "error");
      return null;
    }
  }

  async renderPosts() {
    const posts = await this.fetchPosts();
    const postsContainer = document.getElementById("posts-list");

    if (posts.length === 0) {
      postsContainer.innerHTML = "<p>No posts found.</p>";
      return;
    }

    postsContainer.innerHTML = posts
      .map(
        (post) => `
            <div class="post-card" data-id="${post.id}">
                <h3>${post.title}</h3>
                <p>${post.content.substring(0, 100)}${
          post.content.length > 100 ? "..." : ""
        }</p>
                <small>By: ${post.author.username}</small>
            </div>
        `
      )
      .join("");
  }

  async renderPost(id) {
    const post = await this.fetchPost(id);
    const postContainer = document.getElementById("post-content");

    if (!post) {
      postContainer.innerHTML = "<p>Post not found.</p>";
      return;
    }

    postContainer.innerHTML = `
            <h2>${post.title}</h2>
            <small>By: ${post.author.username}</small>
            <p class="post-content">${post.content}</p>
        `;
  }
}

window.posts = new Posts();
