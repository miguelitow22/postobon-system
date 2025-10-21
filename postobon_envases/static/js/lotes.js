console.log("Frontend LOTES conectado ✅");

const tablaLotes = document.querySelector("#tablaLotes tbody");
const formLote = document.querySelector("#formLote");
const formEditarLote = document.querySelector("#formEditarLote");

// Cargar lotes al iniciar
window.addEventListener("DOMContentLoaded", cargarLotes);

function cargarLotes() {
  fetch("/api/lotes")
    .then((res) => res.json())
    .then((data) => {
      tablaLotes.innerHTML = "";
      data.forEach((l) => {
        const fila = `
          <tr>
            <td>${l.id_lote}</td>
            <td>${l.fecha_salida || "-"}</td>
            <td>${l.punto_origen_id || "-"}</td>
            <td>${l.estado}</td>
            <td>
              <button class="btn btn-warning btn-sm me-1" onclick="editarLote('${l.id_lote}')">Editar</button>
              <button class="btn btn-danger btn-sm" onclick="eliminarLote('${l.id_lote}')">Eliminar</button>
            </td>
          </tr>`;
        tablaLotes.innerHTML += fila;
      });
    });
}

// Crear lote
formLote.addEventListener("submit", (e) => {
  e.preventDefault();
  const nuevo = {
    id_lote: document.querySelector("#id_lote").value,
    punto_origen_id: document.querySelector("#punto_origen_id").value,
    estado: document.querySelector("#estado").value,
  };

  fetch("/api/lotes", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(nuevo),
  })
    .then((res) => res.json())
    .then(() => {
      formLote.reset();
      cargarLotes();
    });
});

// Editar lote
function editarLote(id) {
  fetch(`/api/lotes/${id}`)
    .then((res) => res.json())
    .then((l) => {
      document.querySelector("#edit_id_lote").value = l.id_lote;
      document.querySelector("#edit_punto_origen_id").value = l.punto_origen_id || "";
      document.querySelector("#edit_estado").value = l.estado;
      new bootstrap.Modal(document.querySelector("#modalEditarLote")).show();
    });
}

// Guardar edición
formEditarLote.addEventListener("submit", (e) => {
  e.preventDefault();
  const id = document.querySelector("#edit_id_lote").value;
  const actualizado = {
    punto_origen_id: document.querySelector("#edit_punto_origen_id").value,
    estado: document.querySelector("#edit_estado").value,
  };

  fetch(`/api/lotes/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(actualizado),
  })
    .then((res) => res.json())
    .then(() => {
      const modal = bootstrap.Modal.getInstance(document.querySelector("#modalEditarLote"));
      modal.hide();
      cargarLotes();
    });
});

// Eliminar
function eliminarLote(id) {
  if (!confirm("¿Eliminar este lote?")) return;
  fetch(`/api/lotes/${id}`, { method: "DELETE" })
    .then((res) => res.json())
    .then(() => cargarLotes());
}
