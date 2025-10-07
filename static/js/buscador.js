  // Mostrar filtros segun el modo elegido
  document.addEventListener("DOMContentLoaded", function () {
    const pacienteBtn = document.getElementById("modoPaciente");
    const tutorBtn = document.getElementById("modoTutor");
    const filtrosPaciente = document.getElementById("filtrosPaciente");
    const filtrosTutor = document.getElementById("filtrosTutor");
    const searchForm = document.getElementById("searchForm");

    function actualizarFiltros() {
      if (pacienteBtn.checked) {
        filtrosPaciente.style.display = "block";
        filtrosTutor.style.display = "none";
      } else {
        filtrosPaciente.style.display = "none";
        filtrosTutor.style.display = "block";
      }
    }

    pacienteBtn.addEventListener("change", actualizarFiltros);
    tutorBtn.addEventListener("change", actualizarFiltros);

    actualizarFiltros();

    // Interceptar submit para armar GET con todos los filtros
    searchForm.addEventListener("submit", function (e) {
      e.preventDefault(); // evitar submit normal

      const params = new URLSearchParams();
      params.set("modo", pacienteBtn.checked ? "paciente" : "tutor");

      // q del buscador
      const q = document.getElementById("searchInput").value.trim();
      if (q) params.set("q", q);

      // filtros pacientes
      if (pacienteBtn.checked) {
        filtrosPaciente.querySelectorAll("input").forEach((input) => {
          if (
            (input.type === "checkbox" && input.checked) ||
            (input.type !== "checkbox" && input.value.trim() !== "")
          ) {
            params.set(input.name, input.value.trim());
          }
        });
      }

      // filtros tutores
      if (tutorBtn.checked) {
        filtrosTutor.querySelectorAll("input").forEach((input) => {
          if (
            (input.type === "checkbox" && input.checked) ||
            (input.type !== "checkbox" && input.value.trim() !== "")
          ) {
            params.set(input.name, input.value.trim());
          }
        });
      }

      // Redirigir a /buscar con los parámetros
      window.location.href = "/buscar?" + params.toString();
    });
  });