class Router {
  constructor() {
    this.routes = {
      login: {
        id: "login-page",
        requiresAuth: false,
      },
      register: {
        id: "register-page",
        requiresAuth: false,
      },
      posts: {
        id: "posts-page",
        requiresAuth: true,
        onRender: () => window.posts.renderPosts(),
      },
      post: {
        id: "post-page",
        requiresAuth: true,
        onRender: (params) => window.posts.renderPost(params.id),
      },
      "create-post": {
        id: "create-post-page",
        requiresAuth: true,
      },
    };

    this.setupEventListeners();
    this.handleInitialRoute();
  }

  setupEventListeners() {
    document.querySelectorAll("[data-page]").forEach((element) => {
      element.addEventListener("click", (e) => {
        e.preventDefault();
        const page = e.target.dataset.page;
        this.navigate(page);
      });
    });
  }

  handleInitialRoute() {
    const isAuthenticated = window.auth.isAuthenticated();
    if (isAuthenticated) {
      this.navigate("posts");
    } else {
      this.navigate("login");
    }
  }

  navigate(routeName, params = {}) {
    const route = this.routes[routeName];
    if (!route) return;

    if (route.requiresAuth && !window.auth.isAuthenticated()) {
      window.auth.showNotification("Please login first", "error");
      this.navigate("login");
      return;
    }

    // Hide all pages
    document.querySelectorAll(".page").forEach((page) => {
      page.classList.remove("active");
    });

    // Show the target page
    const targetPage = document.getElementById(route.id);
    targetPage.classList.add("active");

    // Call the onRender function if it exists
    if (route.onRender) {
      route.onRender(params);
    }
  }
}

window.router = new Router();
