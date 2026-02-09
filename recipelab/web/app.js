const screens = document.querySelectorAll(".screen");
const navButtons = document.querySelectorAll(".nav-btn");

function showScreen(id) {
  screens.forEach((screen) => screen.classList.remove("active"));
  navButtons.forEach((btn) => btn.classList.remove("active"));
  document.getElementById(id).classList.add("active");
  document.querySelector(`[data-screen="${id}"]`).classList.add("active");
}

navButtons.forEach((btn) => {
  btn.addEventListener("click", () => showScreen(btn.dataset.screen));
});

const usernameKey = "recipelab-username";

function getUsername() {
  return localStorage.getItem(usernameKey) || "local";
}

const loginForm = document.getElementById("login-form");
loginForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const formData = new FormData(loginForm);
  const username = formData.get("username");
  localStorage.setItem(usernameKey, username);
  document.getElementById("login-status").textContent = `Saved as ${username}`;
});

const uploadForm = document.getElementById("upload-form");
uploadForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(uploadForm);
  formData.append("user_id", getUsername());
  const response = await fetch("/api/recipes/import", {
    method: "POST",
    body: formData,
  });
  const data = await response.json();
  document.getElementById("upload-status").textContent = JSON.stringify(data, null, 2);
});

const searchForm = document.getElementById("search-form");
searchForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(searchForm);
  const query = formData.get("query");
  const response = await fetch(`/api/recipes/search?q=${encodeURIComponent(query)}`);
  const data = await response.json();
  document.getElementById("search-results").textContent = JSON.stringify(data, null, 2);
});

const chatForm = document.getElementById("chat-form");
chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(chatForm);
  formData.append("user_id", getUsername());
  const response = await fetch("/api/chat", {
    method: "POST",
    body: formData,
  });
  const data = await response.json();
  document.getElementById("chat-response").textContent = JSON.stringify(data, null, 2);
});

const prefsSave = document.getElementById("prefs-save");
prefsSave.addEventListener("click", () => {
  const text = document.getElementById("prefs-input").value;
  const formData = new FormData();
  formData.append("user_id", getUsername());
  formData.append("rules", text);
  fetch("/api/preferences", { method: "POST", body: formData })
    .then((resp) => resp.json())
    .then(() => {
      document.getElementById("prefs-status").textContent = "Saved.";
    })
    .catch(() => {
      document.getElementById("prefs-status").textContent = "Save failed.";
    });
});

const pantrySave = document.getElementById("pantry-save");
pantrySave.addEventListener("click", () => {
  const text = document.getElementById("pantry-input").value;
  const formData = new FormData();
  formData.append("user_id", getUsername());
  formData.append("items", text);
  fetch("/api/pantry", { method: "POST", body: formData })
    .then((resp) => resp.json())
    .then(() => {
      document.getElementById("pantry-status").textContent = "Saved.";
    })
    .catch(() => {
      document.getElementById("pantry-status").textContent = "Save failed.";
    });
});
