document.addEventListener("DOMContentLoaded", function () {
  const programButtonsContainer = document.getElementById("program-buttons");
  const editProgramForm = document.getElementById("edit-program");
  const programNameInput = document.getElementById("program-name");

  // Cargar programas desde el archivo JSON
  fetch("/load_programs", { method: "GET" })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Error en la solicitud: ${response.statusText}`);
      }
      return response.json();
    })
    .then((programs) => {
      programButtonsContainer.innerHTML = "";

      Object.entries(programs).forEach(([programName, programPath]) => {
        const btnDiv = document.createElement("div");
        btnDiv.className = "program-item";

        const h1 = document.createElement("h1");
        h1.className = programName;
        h1.textContent = programName;

        h1.addEventListener("click", () => openProgram(programName));

        btnDiv.appendChild(h1);
        programButtonsContainer.appendChild(btnDiv);
      });
    })
    .catch((error) => {
      console.error("Error al cargar los programas:", error);
      programButtonsContainer.innerHTML =
        "<p>Error al cargar los programas.</p>";
    });

  function openProgram(programName) {
    fetch("/open", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: programName }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Error al abrir el programa: ${response.statusText}`);
        }
        return response.text();
      })
      .then((data) => console.log("Programa abierto:", data))
      .catch((error) => console.error("Error al abrir el programa:", error));
  }

  programButtonsContainer.addEventListener("dblclick", function (event) {
    const clickedElement = event.target;

    if (clickedElement.tagName === "H1") {
      currentProgram = clickedElement.className;
      programNameInput.value = clickedElement.textContent;
      editProgramForm.style.display = "block";
    }
  });
});
