const API_URL = "http://127.0.0.1:8000";


async function loadProjects() {
    const response = await fetch(`${API_URL}/projects/`);

    const projects = await response.json();

    const container = document.getElementById("projects-container");

    container.innerHTML = "";

    if (projects.length === 0) {
        container.innerHTML = "<p>No projects yet.</p>";
        return;
    }

    projects.forEach(project => {
        const card = document.createElement("div");

        card.className = "project-card";

        card.innerHTML = `
            <h3>${project.name}</h3>
            <p>${project.description}</p>
        `;

        container.appendChild(card);
    });
}


loadProjects();

//New project button

const newProjectButton = document.getElementById("new-project-button");

const projectFormContainer = document.getElementById(
    "project-form-container"
);

const cancelProjectButton = document.getElementById(
    "cancel-project-button"
);


newProjectButton.addEventListener("click", () => {
    projectFormContainer.classList.remove("hidden");
});


cancelProjectButton.addEventListener("click", () => {
    projectFormContainer.classList.add("hidden");
});

const projectForm = document.getElementById("project-form");


projectForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const name = document.getElementById("project-name").value;
    const description = document.getElementById(
        "project-description"
    ).value;

    const response = await fetch(
        `${API_URL}/projects/?name=${encodeURIComponent(name)}&description=${encodeURIComponent(description)}`,
        {
            method: "POST"
        }
    );

    if (!response.ok) {
        alert("There was a problem creating the project.");
        return;
    }

    projectForm.reset();

    projectFormContainer.classList.add("hidden");

    loadProjects();
});