const API_URL = "/graphql";

class Auth {
  constructor() {
    this.token = localStorage.getItem("token");
    this.setupEventListeners();
    this.updateNavigation();
  }

  setupEventListeners() {
    document
      .getElementById("login-form")
      .addEventListener("submit", (e) => this.handleLogin(e));
    document
      .getElementById("register-form")
      .addEventListener("submit", (e) => this.handleRegister(e));
    document
      .getElementById("logout-link")
      .addEventListener("click", (e) => this.handleLogout(e));
  }

  async handleLogin(e) {
    e.preventDefault();
    const username = e.target.username.value;
    const password = e.target.password.value;

    try {
      const query = `
                mutation {
                    login(username: "${username}", password: "${password}") {
                        token
                        user {
                            id
                            username
                        }
                    }
                }
            `;

      const response = await this.graphqlRequest(query);
      const { token } = response.data.login;

      this.setToken(token);
      this.showNotification("Login successful!", "success");
      window.router.navigate("posts");
    } catch (error) {
      this.showNotification(error.message, "error");
    }
  }

  async handleRegister(e) {
    e.preventDefault();
    const username = e.target.username.value;
    const password = e.target.password.value;

    try {
      const query = `
                mutation {
                    register(username: "${username}", password: "${password}") {
                        token
                        user {
                            id
                            username
                        }
                    }
                }
            `;

      const response = await this.graphqlRequest(query);
      const { token } = response.data.register;

      this.setToken(token);
      this.showNotification("Registration successful!", "success");
      window.router.navigate("posts");
    } catch (error) {
      this.showNotification(error.message, "error");
    }
  }

  handleLogout(e) {
    e.preventDefault();
    this.setToken(null);
    this.showNotification("Logged out successfully!", "success");
    window.router.navigate("login");
  }

  setToken(token) {
    this.token = token;
    if (token) {
      localStorage.setItem("token", token);
    } else {
      localStorage.removeItem("token");
    }
    this.updateNavigation();
  }

  updateNavigation() {
    const authLinks = document.querySelectorAll(".auth-link");
    const logoutLink = document.getElementById("logout-link");

    if (this.token) {
      authLinks.forEach((link) => (link.style.display = "none"));
      logoutLink.style.display = "inline-block";
    } else {
      authLinks.forEach((link) => (link.style.display = "inline-block"));
      logoutLink.style.display = "none";
    }
  }

  async graphqlRequest(query) {
    const headers = {
      "Content-Type": "application/json",
    };

    if (this.token) {
      headers["Authorization"] = `Bearer ${this.token}`;
    }

    const response = await fetch(API_URL, {
      method: "POST",
      headers,
      body: JSON.stringify({ query }),
    });

    const result = await response.json();

    if (result.errors) {
      throw new Error(result.errors[0].message);
    }

    return result;
  }

  showNotification(message, type) {
    const notification = document.getElementById("notification");
    notification.textContent = message;
    notification.className = `notification ${type}`;

    setTimeout(() => {
      notification.className = "notification";
    }, 3000);
  }

  isAuthenticated() {
    return !!this.token;
  }
}

window.auth = new Auth();
