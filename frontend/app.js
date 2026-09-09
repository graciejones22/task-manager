const API_URL = "http://127.0.0.1:8000";
let currentProjectId = null;


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
            <button class="view-project-button">View Project</button>
        `;

        const viewButton = card.querySelector(".view-project-button");

        viewButton.addEventListener("click", () => {
            currentProjectId = project.id;

            console.log("Selected project:", currentProjectId);

            loadTasks(project.id, project.name);
        });

        container.appendChild(card);
    });
}

async function loadTasks(projectId, projectName) {
    const response = await fetch(
        `${API_URL}/tasks/project/${projectId}`
    );

    const tasks = await response.json();

    const tasksSection = document.getElementById("tasks-section");
    const tasksTitle = document.getElementById("tasks-title");
    const tasksContainer = document.getElementById("tasks-container");

    tasksSection.classList.remove("hidden");

    tasksTitle.textContent = `Tasks for ${projectName}`;

    tasksContainer.innerHTML = "";

    if (tasks.length === 0) {
        tasksContainer.innerHTML = "<p>No tasks yet.</p>";
        return;
    }

    tasks.forEach(task => {
        const taskCard = document.createElement("div");

        taskCard.className = "task-card";

        taskCard.innerHTML = `
            <h3>${task.title}</h3>
            <p>${task.description}</p>
            <p>Status: ${task.status}</p>
            <p>Priority: ${task.priority}</p>
        `;

        tasksContainer.appendChild(taskCard);
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

//New task button

const newTaskButton = document.getElementById("new-task-button");

const taskFormContainer = document.getElementById(
    "task-form-container"
);

const cancelTaskButton = document.getElementById(
    "cancel-task-button"
);

newTaskButton.addEventListener("click", () => {
    taskFormContainer.classList.remove("hidden");
});

cancelTaskButton.addEventListener("click", () => {
    taskFormContainer.classList.add("hidden");
});

const taskForm = document.getElementById("task-form");

taskForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const title = document.getElementById("task-title").value;
    const description = document.getElementById(
        "task-description"
    ).value;
    const status = document.getElementById("task-status").value;
    const priority = document.getElementById("task-priority").value;

    if (currentProjectId === null) {
        alert("Please select a project first.");
        return;
    }

    const response = await fetch(
        `${API_URL}/tasks/project/${currentProjectId}`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title,
                description,
                status,
                priority
            })
        }
    );

    if (!response.ok) {
        alert("There was a problem creating the task.");
        return;
    }

    taskForm.reset();

    taskFormContainer.classList.add("hidden");

    loadTasks(
        currentProjectId,
        document.getElementById("tasks-title").textContent.replace(
            "Tasks for ",
            ""
        )
    );
});