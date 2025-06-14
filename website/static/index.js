console.log("index.js is connected!");
let connectedAccountId = null;

console.log("index.js is connected!");

const signUpButton = document.getElementById("sign-up-button");
const addInfoButton = document.getElementById("add-information-button");
const errorDiv = document.getElementById("error");
const connectedAccountDiv = document.getElementById("connected-account-id");

signUpButton.onclick = async () => {
  errorDiv.classList.add("hidden");
  signUpButton.disabled = true;

  fetch("/account", { method: "POST" })
    .then((res) => res.json())
    .then(({ account, error }) => {
      if (error) {
        errorDiv.textContent = error;
        errorDiv.classList.remove("hidden");
        signUpButton.disabled = false;
        return;
      }
      connectedAccountId = account;
      connectedAccountDiv.innerHTML = `Your connected account ID is: <code>${connectedAccountId}</code>`;
      connectedAccountDiv.classList.remove("hidden");
      addInfoButton.classList.remove("hidden");
      signUpButton.classList.add("hidden");
    })
    .catch((err) => {
      errorDiv.textContent = err.message || "Unknown error";
      errorDiv.classList.remove("hidden");
      signUpButton.disabled = false;
    });
};

addInfoButton.onclick = async () => {
  errorDiv.classList.add("hidden");
  addInfoButton.disabled = true;

  fetch("/account_link", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ account: connectedAccountId }),
  })
    .then((res) => res.json())
    .then(({ url, error }) => {
      if (error) {
        errorDiv.textContent = error;
        errorDiv.classList.remove("hidden");
        addInfoButton.disabled = false;
        return;
      }
      window.location.href = url;
    })
    .catch((err) => {
      errorDiv.textContent = err.message || "Unknown error";
      errorDiv.classList.remove("hidden");
      addInfoButton.disabled = false;
    });
};
