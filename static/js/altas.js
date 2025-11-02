document.addEventListener("DOMContentLoaded", () => {
  const selectTutor = document.getElementById("tutor-select");
  const formPacienteDiv = document.getElementById("form-paciente");
  const tutorIdInput = document.getElementById("tutor-id");

  // --- Mostrar formulario si ya hay tutor seleccionado al cargar ---
  if (selectTutor && formPacienteDiv && tutorIdInput) {
    const formPaciente = formPacienteDiv.querySelector("form");
    if (selectTutor.value) {
      formPacienteDiv.classList.remove("d-none");
      tutorIdInput.value = selectTutor.value;
    }
    selectTutor.addEventListener("change", () => {
      if (selectTutor.value) {
        formPacienteDiv.classList.remove("d-none");
        tutorIdInput.value = selectTutor.value;
      } else {
        formPacienteDiv.classList.add("d-none");
        tutorIdInput.value = "";
      }
    });

    // --- Bloque para formulario paciente ---
    if (formPaciente) {
      formPaciente.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(formPaciente);
        try {
          const response = await fetch(formPaciente.action, {
            method: "POST",
            body: formData,
          });
          const data = await response.json();
          if (response.ok) {
            alert(data.mensaje || "Paciente creado correctamente");
            // Redirigir al detalle del paciente
            window.location.href = `/paciente/${data.id}`;
          } else {
            alert(data.error || "Hubo un error al crear el paciente");
          }
        } catch (error) {
          console.error(error);
          alert("Error de conexión al servidor");
        }
      });
    }
  }

  // --- Bloque para nuevo_tutor ---
  const formTutor = document.getElementById("form-tutor");
  if (formTutor) {
    formTutor.addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(formTutor);
      try {
        const response = await fetch(formTutor.action, {
          method: "POST",
          body: formData,
        });
        const data = await response.json();
        if (response.ok) {
          alert(data.mensaje);
          // Redirigir a nuevo_paciente con tutor recién creado seleccionado
          window.location.href = `/paciente/nuevo?tutor_id=${data.id}`;
        } else {
          alert(data.error || "Hubo un error al crear el tutor");
        }
      } catch (error) {
        console.error(error);
        alert("Error de conexión al servidor");
      }
    });
  }
  // --- Profesional (crear o editar) ---
  const formProfesional = document.getElementById("form-profesional");
  if (formProfesional) {
    const metodo = formProfesional.dataset.metodo || "POST"; // POST o PUT según la vista

    formProfesional.addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(formProfesional);

      try {
        const response = await fetch(formProfesional.action, {
          method: metodo,
          body: formData
        });
        const data = await response.json();
        if (response.ok) {
          alert(data.mensaje);
          window.location.href = "/admin";
        } else {
          alert(data.error || "Hubo un error al guardar el profesional");
        }
      } catch (error) {
        console.error(error);
        alert("Error de conexión al servidor");
      }
    });
  }
});