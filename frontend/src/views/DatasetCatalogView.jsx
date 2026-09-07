import { useEffect, useState } from "react";

import {
  getDatasets,
  createDataset,
  updateDataset,
  deleteDataset
} from "../api";

const EMPTY_FORM = {
  code: "",
  name: "",
  description: "",
  source_type: "csv",
  source_location: "",
  record_count: 0,
  active: true
};

function DatasetCatalogView() {
  const [datasets, setDatasets] = useState([]);
  const [form, setForm] = useState(EMPTY_FORM);
  const [editingId, setEditingId] = useState(null);

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  async function loadDatasets() {
    try {
      setLoading(true);
      setError("");

      const data = await getDatasets();

      setDatasets(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDatasets();
  }, []);

  function handleChange(event) {
    const { name, value, type, checked } = event.target;

    setForm((current) => ({
      ...current,
      [name]:
        type === "checkbox"
          ? checked
          : name === "record_count"
            ? Number(value)
            : value
    }));
  }

  function resetForm() {
    setForm(EMPTY_FORM);
    setEditingId(null);
  }

  function handleEdit(dataset) {
    setEditingId(dataset.id);

    setForm({
      code: dataset.code || "",
      name: dataset.name || "",
      description: dataset.description || "",
      source_type: dataset.source_type || "csv",
      source_location: dataset.source_location || "",
      record_count: Number(dataset.record_count || 0),
      active: Boolean(dataset.active)
    });

    setMessage("");
    setError("");
  }

  async function handleSubmit(event) {
    event.preventDefault();

    try {
      setSaving(true);
      setError("");
      setMessage("");

      const payload = {
        code: form.code.trim(),
        name: form.name.trim(),
        description: form.description.trim(),
        source_type: form.source_type,
        source_location: form.source_location.trim(),
        record_count: Number(form.record_count || 0),
        active: Boolean(form.active)
      };

      if (editingId !== null) {
        await updateDataset(editingId, payload);
        setMessage("Dataset actualizado correctamente.");
      } else {
        await createDataset(payload);
        setMessage("Dataset creado correctamente.");
      }

      resetForm();
      await loadDatasets();
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete(dataset) {
    const confirmed = window.confirm(
      `¿Eliminar del catálogo el dataset "${dataset.name}"?`
    );

    if (!confirmed) {
      return;
    }

    try {
      setError("");
      setMessage("");

      await deleteDataset(dataset.id);

      setMessage("Dataset eliminado del catálogo.");

      if (editingId === dataset.id) {
        resetForm();
      }

      await loadDatasets();
    } catch (err) {
      console.error(err);
      setError(err.message);
    }
  }

  return (
    <section className="view-section">
      <div className="section-header">
        <div>
          <div className="eyebrow">DATA MANAGEMENT</div>
          <h2>Dataset Catalog</h2>
          <p>
            Administración de metadatos y fuentes de datos utilizadas por
            RiskGuard.
          </p>
        </div>
      </div>

      {error && (
        <div
          className="error-banner"
          style={{
            color: "#b91c1c",
            marginBottom: "1rem",
            padding: "0.75rem",
            border: "1px solid #fecaca",
            borderRadius: "8px"
          }}
        >
          {error}
        </div>
      )}

      {message && (
        <div
          style={{
            marginBottom: "1rem",
            padding: "0.75rem",
            border: "1px solid #bbf7d0",
            borderRadius: "8px"
          }}
        >
          {message}
        </div>
      )}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "minmax(320px, 0.8fr) minmax(500px, 1.4fr)",
          gap: "1.5rem",
          alignItems: "start"
        }}
      >
        <div className="card">
          <div className="card-header">
            <h3>
              {editingId !== null
                ? "Editar dataset"
                : "Registrar dataset"}
            </h3>
          </div>

          <form onSubmit={handleSubmit}>
            <div style={{ display: "grid", gap: "1rem" }}>
              <label>
                <strong>Código</strong>
                <input
                  name="code"
                  value={form.code}
                  onChange={handleChange}
                  placeholder="RG-CATALOG-001"
                  required
                  style={{ width: "100%", marginTop: "0.35rem" }}
                />
              </label>

              <label>
                <strong>Nombre</strong>
                <input
                  name="name"
                  value={form.name}
                  onChange={handleChange}
                  placeholder="Catálogo de riesgos"
                  required
                  style={{ width: "100%", marginTop: "0.35rem" }}
                />
              </label>

              <label>
                <strong>Descripción</strong>
                <textarea
                  name="description"
                  value={form.description}
                  onChange={handleChange}
                  rows="3"
                  placeholder="Descripción de la fuente"
                  style={{ width: "100%", marginTop: "0.35rem" }}
                />
              </label>

              <label>
                <strong>Tipo de fuente</strong>
                <select
                  name="source_type"
                  value={form.source_type}
                  onChange={handleChange}
                  style={{ width: "100%", marginTop: "0.35rem" }}
                >
                  <option value="csv">CSV</option>
                  <option value="json">JSON</option>
                  <option value="api">API</option>
                </select>
              </label>

              <label>
                <strong>Ubicación de fuente</strong>
                <input
                  name="source_location"
                  value={form.source_location}
                  onChange={handleChange}
                  placeholder="data/riesgos.csv"
                  required
                  style={{ width: "100%", marginTop: "0.35rem" }}
                />
              </label>

              <label>
                <strong>Cantidad de registros</strong>
                <input
                  type="number"
                  min="0"
                  name="record_count"
                  value={form.record_count}
                  onChange={handleChange}
                  style={{ width: "100%", marginTop: "0.35rem" }}
                />
              </label>

              <label
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "0.5rem"
                }}
              >
                <input
                  type="checkbox"
                  name="active"
                  checked={form.active}
                  onChange={handleChange}
                />
                <strong>Fuente activa</strong>
              </label>

              <div style={{ display: "flex", gap: "0.75rem" }}>
                <button
                  type="submit"
                  className="primary-button"
                  disabled={saving}
                >
                  {saving
                    ? "Guardando..."
                    : editingId !== null
                      ? "Actualizar"
                      : "Registrar"}
                </button>

                {editingId !== null && (
                  <button
                    type="button"
                    className="secondary-button"
                    onClick={resetForm}
                    disabled={saving}
                  >
                    Cancelar
                  </button>
                )}
              </div>
            </div>
          </form>
        </div>

        <div className="card">
          <div className="card-header">
            <h3>Datasets catalogados</h3>
            <span>{datasets.length} fuentes</span>
          </div>

          {loading ? (
            <p>Cargando catálogo...</p>
          ) : datasets.length === 0 ? (
            <p>No hay datasets registrados en el catálogo.</p>
          ) : (
            <div style={{ overflowX: "auto" }}>
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Código</th>
                    <th>Nombre</th>
                    <th>Fuente</th>
                    <th>Registros</th>
                    <th>Estado</th>
                    <th>Acciones</th>
                  </tr>
                </thead>

                <tbody>
                  {datasets.map((dataset) => (
                    <tr key={dataset.id}>
                      <td>{dataset.code}</td>

                      <td>
                        <strong>{dataset.name}</strong>

                        {dataset.description && (
                          <div
                            style={{
                              fontSize: "0.85rem",
                              opacity: 0.75,
                              marginTop: "0.25rem"
                            }}
                          >
                            {dataset.description}
                          </div>
                        )}
                      </td>

                      <td>
                        <div>{dataset.source_type}</div>
                        <div
                          style={{
                            fontSize: "0.8rem",
                            opacity: 0.7
                          }}
                        >
                          {dataset.source_location}
                        </div>
                      </td>

                      <td>
                        {Number(dataset.record_count || 0).toLocaleString()}
                      </td>

                      <td>
                        {dataset.active ? "Activo" : "Inactivo"}
                      </td>

                      <td>
                        <div
                          style={{
                            display: "flex",
                            gap: "0.5rem",
                            flexWrap: "wrap"
                          }}
                        >
                          <button
                            type="button"
                            className="secondary-button"
                            onClick={() => handleEdit(dataset)}
                          >
                            Editar
                          </button>

                          <button
                            type="button"
                            className="secondary-button"
                            onClick={() => handleDelete(dataset)}
                          >
                            Eliminar
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}

export default DatasetCatalogView;
