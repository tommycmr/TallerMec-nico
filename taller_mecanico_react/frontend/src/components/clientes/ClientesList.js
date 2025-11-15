import React, { useEffect, useState } from "react";
import {
  fetchClientes,
  fetchVehiculos,
  fetchReparaciones,
  createCliente,
  updateCliente,
  deleteCliente,
  createVehiculo,
  updateVehiculo,
  deleteVehiculo,
} from "../../services/api";
import "./ClienteLista.css";

const ClientesList = () => {
  const [clientes, setClientes] = useState([]);
  const [vehiculos, setVehiculos] = useState([]);
  const [reparaciones, setReparaciones] = useState([]);
  const [clienteSeleccionado, setClienteSeleccionado] = useState(null);

  const [nombre, setNombre] = useState("");
  const [telefono, setTelefono] = useState("");
  const [email, setEmail] = useState("");
  const [direccion, setDireccion] = useState("");
  const [vehiculosEdicion, setVehiculosEdicion] = useState([]);

  const [modoEdicion, setModoEdicion] = useState(false);
  const [clienteIdEdicion, setClienteIdEdicion] = useState(null);

  useEffect(() => {
    obtenerDatos();
  }, []);

  const obtenerDatos = async () => {
    try {
      const [clientesData, vehiculosData, reparacionesData] = await Promise.all([
        fetchClientes(),
        fetchVehiculos(),
        fetchReparaciones(),
      ]);
      setClientes(clientesData);
      setVehiculos(vehiculosData);
      setReparaciones(reparacionesData);
    } catch (error) {
      console.error("Error al obtener datos:", error);
      alert("Hubo un error al cargar los datos desde el servidor.");
    }
  };

  const toggleClienteSeleccionado = (clienteId) => {
    setClienteSeleccionado(clienteSeleccionado === clienteId ? null : clienteId);
  };

  const handleEditarCliente = (cliente) => {
    setModoEdicion(true);
    setClienteIdEdicion(cliente.id);
    setNombre(cliente.nombre);
    setTelefono(cliente.telefono);
    setEmail(cliente.email);
    setDireccion(cliente.direccion);

    const vehiculosCliente = vehiculos.filter((v) => v.cliente_id === cliente.id);
    setVehiculosEdicion(vehiculosCliente);
  };

  const handleEliminarCliente = async (clienteId) => {
    if (!window.confirm("¿Seguro que deseas eliminar este cliente y todos sus vehículos?")) return;

    try {
      await deleteCliente(clienteId);
      alert("Cliente eliminado correctamente");
      obtenerDatos();
    } catch (error) {
      console.error("Error al eliminar cliente:", error);
      alert("No se pudo eliminar el cliente.");
    }
  };

  const handleAgregarClienteYVehiculo = async (e) => {
    e.preventDefault();
    if (!nombre || !telefono || !email || !direccion) {
      alert("Todos los campos son obligatorios");
      return;
    }

    try {
      let cliente;
      if (modoEdicion) {
        cliente = await updateCliente(clienteIdEdicion, { nombre, telefono, email, direccion });
        for (const vehiculo of vehiculosEdicion) {
          if (vehiculo.id) {
            await updateVehiculo(vehiculo.id, vehiculo);
          } else {
            await createVehiculo({ ...vehiculo, cliente_id: cliente.id });
          }
        }
        alert("Cliente y vehículos actualizados correctamente");
      } else {
        cliente = await createCliente({ nombre, telefono, email, direccion });
        for (const vehiculo of vehiculosEdicion) {
          await createVehiculo({ ...vehiculo, cliente_id: cliente.id });
        }
        alert("Cliente y vehículos creados correctamente");
      }

      // Limpiar formulario
      setNombre("");
      setTelefono("");
      setEmail("");
      setDireccion("");
      setVehiculosEdicion([]);
      setModoEdicion(false);
      setClienteIdEdicion(null);

      obtenerDatos();
    } catch (error) {
      console.error("Error al agregar o editar cliente:", error);
      alert("Hubo un error al guardar los datos.");
    }
  };

  const handleAgregarVehiculo = () => {
    setVehiculosEdicion([...vehiculosEdicion, { marca: "", modelo: "", patente: "", anio: "" }]);
  };

  const handleEliminarVehiculo = (index) => {
    const nuevosVehiculos = vehiculosEdicion.filter((_, i) => i !== index);
    setVehiculosEdicion(nuevosVehiculos);
  };

  const handleVehiculoChange = (index, field, value) => {
    const nuevosVehiculos = [...vehiculosEdicion];
    nuevosVehiculos[index][field] = value;
    setVehiculosEdicion(nuevosVehiculos);
  };

  return (
    <div>
      <h2>Gestión de Clientes</h2>

      <form onSubmit={handleAgregarClienteYVehiculo}>
        <h3>{modoEdicion ? "Editar Cliente y Vehículos" : "Agregar Cliente y Vehículos"}</h3>
        <input type="text" placeholder="Nombre" value={nombre} onChange={(e) => setNombre(e.target.value)} />
        <input type="text" placeholder="Teléfono" value={telefono} onChange={(e) => setTelefono(e.target.value)} />
        <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input type="text" placeholder="Dirección" value={direccion} onChange={(e) => setDireccion(e.target.value)} />

        <h4>Vehículos</h4>
        {vehiculosEdicion.map((vehiculo, index) => (
          <div key={index} style={{ marginBottom: "10px" }}>
            <input type="text" placeholder="Marca" value={vehiculo.marca} onChange={(e) => handleVehiculoChange(index, "marca", e.target.value)} />
            <input type="text" placeholder="Modelo" value={vehiculo.modelo} onChange={(e) => handleVehiculoChange(index, "modelo", e.target.value)} />
            <input type="text" placeholder="Patente" value={vehiculo.patente} onChange={(e) => handleVehiculoChange(index, "patente", e.target.value)} />
            <input type="number" placeholder="Año" value={vehiculo.anio} onChange={(e) => handleVehiculoChange(index, "anio", e.target.value)} />
            <button type="button" onClick={() => handleEliminarVehiculo(index)}>Eliminar Vehículo</button>
          </div>
        ))}
        <button type="button" onClick={handleAgregarVehiculo}>Agregar Vehículo</button>
        <button type="submit">{modoEdicion ? "Guardar Cambios" : "Agregar Cliente"}</button>
        {modoEdicion && <button type="button" onClick={() => setModoEdicion(false)}>Cancelar</button>}
      </form>

      <table border="1" style={{ width: "100%", textAlign: "left", marginTop: "20px" }}>
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Teléfono</th>
            <th>Email</th>
            <th>Dirección</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {clientes.map((cliente) => (
            <React.Fragment key={cliente.id}>
              <tr>
                <td>{cliente.nombre}</td>
                <td>{cliente.telefono}</td>
                <td>{cliente.email}</td>
                <td>{cliente.direccion}</td>
                <td>
                  <button onClick={() => toggleClienteSeleccionado(cliente.id)}>
                    {clienteSeleccionado === cliente.id ? "Cerrar" : "Ver Más"}
                  </button>
                  <button onClick={() => handleEditarCliente(cliente)}>Editar</button>
                  <button onClick={() => handleEliminarCliente(cliente.id)}>Eliminar</button>
                </td>
              </tr>
              {clienteSeleccionado === cliente.id && (
                <tr>
                  <td colSpan="5">
                    <div>
                      <h4>Vehículos</h4>
                      <ul>
                        {vehiculos.filter((v) => v.cliente_id === cliente.id).map((v) => (
                          <li key={v.id}>{v.marca} {v.modelo} - {v.patente} ({v.anio})</li>
                        ))}
                      </ul>
                      <h4>Reparaciones</h4>
                      <ul>
                        {reparaciones
                          .filter((r) => vehiculos.some((v) => v.id === r.vehiculo_id && v.cliente_id === cliente.id))
                          .map((r) => (
                            <li key={r.id}>{r.fecha}: {r.descripcion_problema} - ${r.costo}</li>
                          ))}
                      </ul>
                    </div>
                  </td>
                </tr>
              )}
            </React.Fragment>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ClientesList;
