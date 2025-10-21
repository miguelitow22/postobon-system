console.log("Frontend Postobón conectado 💪");

// Elementos
const tablaEnvases = document.querySelector("#tablaEnvases tbody");
const formNuevo = document.querySelector("#formEnvase");
const formEditar = document.querySelector("#formEditar");
const filtroTipo = document.querySelector("#filtroTipo");
const filtroEstado = document.querySelector("#filtroEstado");

// Cargar datos al inicio
window.addEventListener("DOMContentLoaded", cargarEnvases);
filtroTipo.addEventListener("change", cargarEnvases);
filtroEstado.addEventListener("change", cargarEnvases);

// Cargar Envases
function cargarEnvases() {
  fetch("/api/envases")
    .then((res) => res.json())
    .then((data) => {
      let filtrados = data;
      if (filtroTipo.value) filtrados = filtrados.filter(e => e.tipo === filtroTipo.value);
      if (filtroEstado.value) filtrados = filtrados.filter(e => e.estado === filtroEstado.value);

      tablaEnvases.innerHTML = "";
      filtrados.forEach((e) => {
        const fila = `
          <tr>
            <td>${e.id_envase}</td>
            <td>${e.tipo}</td>
            <td>${e.capacidad_ml}</td>
            <td>${e.estado}</td>
            <td>
              <button class="btn btn-warning btn-sm me-1" onclick="editarEnvase('${e.id_envase}')">Editar</button>
              <button class="btn btn-danger btn-sm" onclick="eliminarEnvase('${e.id_envase}')">Eliminar</button>
            </td>
          </tr>`;
        tablaEnvases.innerHTML += fila;
      });
    });
}

// Crear nuevo
formNuevo.addEventListener("submit", (e) => {
  e.preventDefault();
  const nuevo = {
    id_envase: document.querySelector("#id_envase").value,
    tipo: document.querySelector("#tipo").value,
    capacidad_ml: document.querySelector("#capacidad_ml").value,
  };

  fetch("/api/envases", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(nuevo),
  })
    .then((res) => res.json())
    .then(() => {
      const modal = bootstrap.Modal.getInstance(document.querySelector("#modalNuevo"));
      modal.hide();
      formNuevo.reset();
      cargarEnvases();
    });
});

// Eliminar
function eliminarEnvase(id) {
  if (!confirm("¿Eliminar este envase?")) return;
  fetch(`/api/envases/${id}`, { method: "DELETE" })
    .then((res) => res.json())
    .then(() => cargarEnvases());
}

// Editar
function editarEnvase(id) {
  fetch("/api/envases")
    .then((res) => res.json())
    .then((data) => {
      const env = data.find((e) => e.id_envase === id);
      document.querySelector("#edit_id_envase").value = env.id_envase;
      document.querySelector("#edit_tipo").value = env.tipo;
      document.querySelector("#edit_capacidad_ml").value = env.capacidad_ml;
      document.querySelector("#edit_estado").value = env.estado;
      new bootstrap.Modal(document.querySelector("#modalEditar")).show();
    });
}

// Actualizar
formEditar.addEventListener("submit", (e) => {
  e.preventDefault();
  const id = document.querySelector("#edit_id_envase").value;
  const actualizado = {
    tipo: document.querySelector("#edit_tipo").value,
    capacidad_ml: document.querySelector("#edit_capacidad_ml").value,
    estado: document.querySelector("#edit_estado").value,
  };

  fetch(`/api/envases/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(actualizado),
  })
    .then((res) => res.json())
    .then(() => {
      const modal = bootstrap.Modal.getInstance(document.querySelector("#modalEditar"));
      modal.hide();
      cargarEnvases();
    });
});
