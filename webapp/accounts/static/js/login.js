const API_BASE = "http://127.0.0.1:8000";

function setTokens(access, refresh) {
    localStorage.setItem("access", access);
    localStorage.setItem("refresh", refresh);
}

function clearTokens() {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
}

document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");

    if (!loginForm) {
        return;
    }

    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const emailInput = document.getElementById("input-email");
        const passwordInput = document.getElementById("input-password");

        if (!emailInput || !passwordInput) {
            alert("Login form inputs not found.");
            return;
        }

        const email = emailInput.value.trim();
        const password = passwordInput.value;

        if (!email || !password) {
            alert("Please enter username and password.");
            return;
        }

        try {
            const response = await fetch(`${API_BASE}/api/token/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });

            const data = await response.json();
            if (response.ok) {
                setTokens(data.access, data.refresh);

                window.location.href = "/";
            } else {
                clearTokens();

                const errorMessage = data.detail || "Invalid email or password.";
                alert(errorMessage);
            }
        } catch (error) {
            console.error("Login error:", error);
            alert("Could not connect to server.");
        }
    });
});
