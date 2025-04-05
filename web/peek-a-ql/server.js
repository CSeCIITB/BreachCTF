const express = require("express");
const { graphqlHTTP } = require("express-graphql");
const { buildSchema } = require("graphql");
const cors = require("cors");
const jwt = require("jsonwebtoken");
const bcrypt = require("bcryptjs");
const sanitizeHtml = require("sanitize-html");

const JWT_SECRET = Math.random().toString(36).slice(2, 10);

// Generate 100 random users
const users = Array.from({ length: 100 }, () => ({
  id: `user-${Math.random().toString(36).slice(2, 9)}`,
  username: `user_${Math.random().toString(36).slice(2, 5)}`,
  password: Math.random().toString(36).slice(2, 10),
}));

const adminIndex = Math.floor(Math.random() * users.length);
const admin = users[adminIndex];
admin.username = "admin";

// Generate 100 random posts
const posts = Array.from({ length: 100 }, () => ({
  id: `post-${Math.random().toString(36).slice(2, 9)}`,
  title: `Post ${Math.random().toString(36).slice(2, 5)}`,
  content: `Content ${Math.random().toString(36).slice(2, 10)}`,
  author: users[Math.floor(Math.random() * users.length)],
}));

const adminPostIndex = Math.floor(Math.random() * posts.length);
const adminPost = posts[adminPostIndex];
adminPost.author = admin;

const flagPost = {
  id: `post-${Math.random().toString(36).slice(2, 9)}`,
  title: "Here's the flag",
  content: "Breach{gr4phql_1snt_s0_s3cur3_4ft3r_4ll}",
  author: admin,
};

const schema = buildSchema(`
  type Query {
    post(id: ID!): Post
    posts: [Post!]!
    me: User
  }

  type Mutation {
    login(username: String!, password: String!): AuthPayload
    register(username: String!, password: String!): AuthPayload
    createPost(title: String!, content: String!): Post
  }

  type AuthPayload {
    token: String!
    user: User!
  }

  type Post {
    id: ID!
    title: String
    content: String
    author: User
  }

  type User {
    id: ID!
    username: String
    password: String
  }

  type Preferences {
    theme: String
    notifications: Boolean
  }

  type SiteStatus {
    operational: Boolean
  }
`);

// Authentication middleware
const getUser = (req) => {
  const authHeader = req.headers.authorization;
  if (!authHeader) return null;

  try {
    const token = authHeader.split(" ")[1];
    const decoded = jwt.verify(token, JWT_SECRET);
    return users.find((user) => user.id === decoded.userId);
  } catch (err) {
    return null;
  }
};

// --- Root resolver ---
const root = {
  post: ({ id }, context) => {
    if (!context.user) throw new Error("Authentication required");
    return posts.find((post) => post.id === id);
  },
  posts: (_, context) => {
    if (!context.user) throw new Error("Authentication required");

    if (context.user.username === "admin") {
      return [flagPost];
    }

    return posts;
  },
  me: (_, context) => {
    if (!context.user) throw new Error("Authentication required");
    return context.user;
  },
  createPost: ({ title, content }, context) => {
    if (!context.user) throw new Error("Authentication required");

    

    const newPost = {
      id: `post-${Math.random().toString(36).slice(2, 9)}`,
      title: sanitizeHtml(title, {  allowedTags: [ 'b', 'i', 'em', 'strong', 'h1', 'h2', 'h3' ] }),
      content: sanitizeHtml(content, {  allowedTags: [ 'b', 'i', 'em', 'strong', 'h1', 'h2', 'h3' ] }),
      author: context.user,
    };

    posts.push(newPost);
    return newPost;
  },
  login: ({ username, password }) => {
    const user = users.find((u) => u.username === username);
    if (!user) throw new Error("User not found");

    const valid = password === user.password;
    if (!valid) throw new Error("Invalid password");

    const token = jwt.sign({ userId: user.id }, JWT_SECRET, {
      expiresIn: "1h",
    });
    return { token, user };
  },
  register: ({ username, password }) => {
    if (users.some((u) => u.username === username)) {
      throw new Error("Username already exists");
    }

    const newUser = {
      id: `user-${Math.random().toString(36).slice(2, 9)}`,
      username,
      password,
    };
    users.push(newUser);

    const token = jwt.sign({ userId: newUser.id }, JWT_SECRET, {
      expiresIn: "1h",
    });
    return { token, user: newUser };
  },
};

// --- Express App Setup ---
const app = express();
const PORT = 3000;

// Enable CORS for all origins.
app.use(cors());

app.use(
  "/graphql",
  graphqlHTTP((req) => ({
    schema: schema,
    rootValue: root,
    graphiql: true,
    context: { user: getUser(req) },
  })),
);

app.use(express.static("frontend"));

// --- Start the server ---
app.listen(PORT, () => {
  console.log(`[Server] GraphQL server running.`);
  console.log(
    `[Server] Frontend should fetch from http://localhost:${PORT}/graphql`,
  );
});
