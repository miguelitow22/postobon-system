console.log("Frontend MOVIMIENTOS conectado ✅");

const tablaMovimientos = document.querySelector("#tablaMovimientos tbody");
const form = document.querySelector("#formMovimiento");
const selectEnvases = document.querySelector("#id_envase");

// 1️⃣ Cargar datos iniciales
window.addEventListener("DOMContentLoaded", () => {
  cargarEnvases();
  cargarMovimientos();
});

// 2️⃣ Cargar lista de envases para el select
function cargarEnvases() {
  fetch("/api/envases")
    .then((res) => res.json())
    .then((data) => {
      selectEnvases.innerHTML =
        '<option value="" disabled selected>Selecciona un Envase</option>';
      data.forEach((env) => {
        const option = document.createElement("option");
        option.value = env.id_envase;
        option.textContent = `${env.id_envase} - ${env.tipo} (${env.estado})`;
        selectEnvases.appendChild(option);
      });
    });
}

// 3️⃣ Cargar movimientos en tabla
function cargarMovimientos() {
  fetch("/api/movimientos")
    .then((res) => res.json())
    .then((data) => {
      tablaMovimientos.innerHTML = "";
      data.forEach((m) => {
        const fila = `
          <tr>
            <td>${m.id_registro}</td>
            <td>${m.id_envase}</td>
            <td>${m.tipo_movimiento}</td>
            <td>${m.origen_id}</td>
            <td>${m.destino_id}</td>
            <td>${m.fecha}</td>
            <td>${m.operador}</td>
            <td>${m.observaciones || ""}</td>
          </tr>`;
        tablaMovimientos.innerHTML += fila;
      });
    });
}

// 4️⃣ Registrar nuevo movimiento
form.addEventListener("submit", (e) => {
  e.preventDefault();
  const nuevo = {
    id_envase: selectEnvases.value,
    tipo_movimiento: document.querySelector("#tipo_movimiento").value,
    origen_id: document.querySelector("#origen_id").value,
    destino_id: document.querySelector("#destino_id").value,
    operador: document.querySelector("#operador").value,
    observaciones: document.querySelector("#observaciones").value,
  };

  fetch("/api/movimientos", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(nuevo),
  })
    .then((res) => res.json())
    .then(() => {
      form.reset();
      cargarMovimientos();
    });
});
