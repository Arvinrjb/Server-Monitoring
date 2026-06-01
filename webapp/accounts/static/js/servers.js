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

    data.forEach(server => {

        container.innerHTML += `
            <div class="server-row">

                <span>
                    ${server.hostname}
                </span>

                <span>
                    ${server.ipaddress}
                </span>

                <span class="online">
                    Online
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

    await fetch(
        `/api/addserver/${id}/`,
        {
            method:"DELETE"
        }
    );

    loadServers();
}

document
.getElementById("serverForm")
.addEventListener("submit",
async (e) => {

    e.preventDefault();

    const hostname =
        document.getElementById("hostname").value;

    const ipaddress =
        document.getElementById("ipaddress").value;

    await fetch(
        "/api/addserver/",
        {
            method:"POST",

            headers:{
                "Content-Type":
                "application/json"
            },

            body:JSON.stringify({
                hostname,
                ipaddress
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