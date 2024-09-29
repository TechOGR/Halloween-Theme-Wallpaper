document.addEventListener("DOMContentLoaded", function () {
  const programButtonsContainer = document.getElementById("program-buttons");
  const editProgramForm = document.getElementById("edit-program");
  const programNameInput = document.getElementById("program-name");
  const saveButton = document.getElementById("save-button");
  let currentProgram = null;

  // Cargar programas desde el archivo JSON
  fetch("/load_programs", { method: "GET" })
    .then((response) => response.json())
    .then((programs) => {
      programs.forEach((program) => {
        const btnDiv = document.createElement("div");
        btnDiv.className = `btn ${program.name}`;

        const h1 = document.createElement("h1");
        h1.className = program.name;
        h1.textContent = program.name;

        h1.addEventListener("click", (event) => openProgram(program.name));

        btnDiv.appendChild(h1);
        programButtonsContainer.appendChild(btnDiv);
      });
    })
    .catch((error) => console.log(error));

  function openProgram(programName) {
    fetch("/open", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: programName }),
    })
      .then((response) => response.text())
      .then((data) => console.log(data))
      .catch((error) => console.log(error));
  }

  // Editar nombre del programa
  programButtonsContainer.addEventListener("dblclick", function (event) {
    const clickedElement = event.target;

    if (clickedElement.tagName === "H1") {
      currentProgram = clickedElement.className;
      programNameInput.value = clickedElement.textContent;
      editProgramForm.style.display = "block";
    }
  });

  // // Guardar cambios en el nombre del programa
  // saveButton.addEventListener("click", function () {
  //   const newName = programNameInput.value;

  //   fetch("/edit_program", {
  //     method: "POST",
  //     headers: { "Content-Type": "application/json" },
  //     body: JSON.stringify({ old_name: currentProgram, new_name: newName }),
  //   })
  //     .then((response) => response.json())
  //     .then((data) => {
  //       if (data.success) {
  //         // Actualizar el nombre en la interfaz
  //         document.querySelector(`.${currentProgram}`).textContent = newName;
  //         document.querySelector(`.${currentProgram}`).className = newName;

  //         // Ocultar el formulario de edición
  //         editProgramForm.style.display = "none";
  //       }
  //     })
  //     .catch((error) => console.log(error));
  // });
});
