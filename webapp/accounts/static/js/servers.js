function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');

        for (let cookie of cookies) {
            cookie = cookie.trim();

            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }

    return cookieValue;
}


const modal =
    document.getElementById("serverModal");

const addBtn =
    document.getElementById("addServerBtn");

const container =
    document.getElementById("serverContainer");

addBtn.addEventListener("click", () => {
    modal.style.display = "flex";
});

window.addEventListener("click", (e) => {
    if (e.target === modal) {
        modal.style.display = "none";
    }
});

async function loadServers() {

    const response = await fetch(
        "/api/addserver/"
    );

    const data =
        await response.json();

    container.innerHTML = "";

    data.results.forEach(server => {

        container.innerHTML += `
            <div class="server-row">

                <span>
                    ${server.hostname}
                </span>

                <span>
                    ${server.ipaddress}
                </span>

                <span class="${server.status}">
                    ${server.status}
                </span>

                <div class="actions">

                    <button
                        class="view-btn">
                        View
                    </button>

                    <button
                        class="delete-btn"
                        onclick="deleteServer(${server.id})">
                        Delete
                    </button>

                </div>

            </div>
        `;
    });
}

async function deleteServer(id){
    const csrftoken = getCookie('csrftoken');
    await fetch(
        `/api/addserver/${id}/`,
        {
            method:"DELETE",
            headers: {
                "X-CSRFToken": csrftoken
            }
        }
    );

    loadServers();
}

document
.getElementById("serverForm")
.addEventListener("submit",
async (e) => {

    e.preventDefault();
    const csrftoken = getCookie('csrftoken');
    
    const hostname =
        document.getElementById("hostname").value;

    const ipaddress =
        document.getElementById("ipaddress").value;
    const os = 
        document.getElementById("os").value;

    await fetch(
        "/api/addserver/",
        {
            method:"POST",

            headers:{
                "Content-Type":"application/json",
                'X-CSRFToken': csrftoken
            },

            body:JSON.stringify({
                hostname,
                ipaddress,
                os,
            })
        }
    );

    modal.style.display = "none";

    document
        .getElementById("serverForm")
        .reset();

    loadServers();
});

loadServers();