document.getElementById("loginForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const username = document.getElementById("input-username").value;
    const password = document.getElementById("input-password").value;

    const response = await fetch("http://127.0.0.1:8000/api/token/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    });

    const data = await response.json();

    if (response.ok) {
        localStorage.setItem("access", data.access);
        localStorage.setItem("refresh", data.refresh);
        alert("Login successful");
    } else {
        alert("Login failed");
    }
});