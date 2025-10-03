document.addEventListener("DOMContentLoaded", () => {
  const selectTutor = document.getElementById("tutor-select");
  const formPaciente = document.getElementById("form-paciente");
  const tutorIdInput = document.getElementById("tutor-id");

  selectTutor.addEventListener("change", () => {
    if (selectTutor.value) {
      // Tutor seleccionado → mostrar formulario
      formPaciente.classList.remove("d-none");
      tutorIdInput.value = selectTutor.value;
    } else {
      // Sin tutor → ocultar formulario
      formPaciente.classList.add("d-none");
      tutorIdInput.value = "";
    }
  });
});