document.getElementById("saveBtn").addEventListener("click", async function (e) {
  e.preventDefault(); // evita envío automático

  const form = document.getElementById("editarTutorForm");
  const tutorId = form.dataset.id;
  const pacienteId = form.dataset.pacienteId;

  // Forzamos a que todos los campos estén sincronizados
  form.querySelectorAll("input").forEach(input => input.dispatchEvent(new Event("change")));

  // Ahora sí generamos el FormData actualizado
  const data = new FormData(form);

  const nombre = data.get("nombre")?.trim();
  const apellido = data.get("apellido")?.trim();
  const telefono = data.get("telefono")?.trim();
  const email = data.get("email")?.trim();
  const direccion = data.get("direccion")?.trim();

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
