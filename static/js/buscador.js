  // Mostrar filtros segun el modo elegido
document.addEventListener("DOMContentLoaded", function () {
  const pacienteBtn = document.getElementById("modoPaciente");
  const tutorBtn = document.getElementById("modoTutor");
  const consultaBtn = document.getElementById("modoConsulta");

  const filtrosPaciente = document.getElementById("filtrosPaciente");
  const filtrosTutor = document.getElementById("filtrosTutor");
  const filtrosConsulta = document.getElementById("filtrosConsulta");

  const searchForm = document.getElementById("searchForm");

  function actualizarFiltros() {
    filtrosPaciente.style.display = pacienteBtn.checked ? "block" : "none";
    filtrosTutor.style.display = tutorBtn.checked ? "block" : "none";
    filtrosConsulta.style.display = consultaBtn.checked ? "block" : "none";
  }

  pacienteBtn.addEventListener("change", actualizarFiltros);
  tutorBtn.addEventListener("change", actualizarFiltros);
  consultaBtn.addEventListener("change", actualizarFiltros);

  actualizarFiltros();

  // Interceptar submit para armar GET con todos los filtros
  function ejecutarBusqueda() {
    const params = new URLSearchParams();

    // Determinar el modo
    let modo = "paciente";
    if (tutorBtn.checked) modo = "tutor";
    else if (consultaBtn.checked) modo = "consulta";

    params.set("modo", modo);

    // q del buscador
    const q = document.getElementById("searchInput").value.trim();
    if (q) params.set("q", q);

    // Filtros segun el modo seleccionado
    const filtrosActivos =
      modo === "paciente"
        ? filtrosPaciente
        : modo === "tutor"
        ? filtrosTutor
        : filtrosConsulta;

    filtrosActivos.querySelectorAll("input").forEach((input) => {
      if (
        (input.type === "checkbox" && input.checked) ||
        (input.type !== "checkbox" && input.value.trim() !== "")
      ) {
        params.set(input.name, input.value.trim());
      }
    });

    // Agregar especie (select) si tiene valor distinto a vacío
    const especieSelect = filtrosActivos.querySelector(
      "select[name='especie']"
    );
    if (especieSelect && especieSelect.value) {
      params.set(especieSelect.name, especieSelect.value);
    }

    // Redirigir a /buscar con los parámetros
    window.location.href = "/buscar?" + params.toString();
  }

  // Interceptar submit para armar GET con todos los filtros
  searchForm.addEventListener("submit", function (e) {
    e.preventDefault(); // evitar submit normal
    ejecutarBusqueda();
  });

  // Detectar el enter
  searchForm.querySelectorAll("input").forEach((input) => {
    input.addEventListener("keypress", function (e) {
      if (e.key === "Enter") {
        e.preventDefault();
        ejecutarBusqueda();
      }
    });
  });

  // Boton para limpiar filtros
  const clearBtn = document.getElementById("clearFilters");
  if (clearBtn) {
    clearBtn.addEventListener("click", () => {
      // Guardar el modo seleccionado
      let modoActual = "paciente";
      if (tutorBtn.checked) modoActual = "tutor";
      else if (consultaBtn.checked) modoActual = "consulta";

      // Selecciona todos los inputs a limpiar
      const allInputs = document.querySelectorAll(
        "#searchForm input, #filtrosAvanzados input"
      );

      allInputs.forEach((input) => {
        if (input.name === "modo") return;

        if (input.type === "checkbox") {
          input.checked = false;
        } else if (input.type === "file") {
          input.value = "";
        } else {
          input.value = "";
        }
      });
       
      // Limpiar el select
      const especieSelect = filtrosPaciente.querySelector("select[name='especie']");
      if (especieSelect) especieSelect.selectedIndex = 0;

      if (modoActual === "paciente") pacienteBtn.checked = true;
      if (modoActual === "tutor") tutorBtn.checked = true;
      if (modoActual === "consulta") consultaBtn.checked = true;
      
      actualizarFiltros();

      // window.location.href = window.location.pathname + "?modo=" + modoActual;
    });
  }
});