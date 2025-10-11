document.getElementById("saveBtn").addEventListener("click", async function () {
  const form = document.getElementById("editarTutorForm");
  const tutorId = form.dataset.id;
  const pacienteId = form.dataset.pacienteId;
  const data = new FormData(form);

  // Validar campos obligatorios
  const nombre = form.querySelector("input[name='nombre']").value.trim();
  const apellido = form.querySelector("input[name='apellido']").value.trim();
  const telefono = form.querySelector("input[name='telefono']").value.trim();
  const email = form.querySelector("input[name='email']").value.trim();
  const direccion = form.querySelector("input[name='direccion']").value.trim();

  if (!nombre || !apellido || !telefono || !email || !direccion) {
    alert("Todos los campos son obligatorios");
    return;
  }
  const resp = await fetch(`/tutor/${tutorId}`, {
    method: "PUT",
    body: data,
  });
  if (resp.ok) {
    location.href = `/paciente/${pacienteId}`;
  } else {
    alert("Error al actualizar el tutor");
  }
});
