import { useEffect, useState } from "react";

const EMPTY_FORM = {
  code: "",
  title: "",
  description: "",
  evidence_type: "",
  file_path: "",
  source: "",
  hash_sha256: "",
  status: "Active",
  collected_at: "",
  owner: "",
  iso_control_id: "",
  risk_id: "",
  event_id: ""
};

export default function EvidenceForm({
  initialData = null,
  saving = false,
  onSubmit,
  onCancel
}) {
  const [form, setForm] = useState(EMPTY_FORM);

  useEffect(() => {
    if (!initialData) {
      setForm(EMPTY_FORM);
      return;
    }

    setForm({
      code: initialData.code ?? "",
      title: initialData.title ?? "",
      description: initialData.description ?? "",
      evidence_type: initialData.evidence_type ?? "",
      file_path: initialData.file_path ?? "",
      source: initialData.source ?? "",
      hash_sha256: initialData.hash_sha256 ?? "",
      status: initialData.status ?? "Active",
      collected_at: initialData.collected_at ?? "",
      owner: initialData.owner ?? "",
      iso_control_id: initialData.iso_control_id ?? "",
      risk_id: initialData.risk_id ?? "",
      event_id: initialData.event_id ?? ""
    });
  }, [initialData]);

  const handleChange = (event) => {
    const { name, value } = event.target;

    setForm((current) => ({
      ...current,
      [name]: value
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const payload = {
      ...form,
      iso_control_id: form.iso_control_id
        ? Number(form.iso_control_id)
        : null,
      risk_id: form.risk_id
        ? Number(form.risk_id)
        : null,
      event_id: form.event_id
        ? Number(form.event_id)
        : null,
      collected_at: form.collected_at || null,
      hash_sha256: form.hash_sha256 || null
    };

    await onSubmit?.(payload);
  };

  const editing = Boolean(initialData);

  return (
    <div className="panel">
      <div className="panel-header">
        <div>
          <h3>{editing ? "Editar evidencia" : "Nueva evidencia"}</h3>
          <p>
            Registra evidencia relacionada con riesgos y controles.
          </p>
        </div>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="form-grid">
          <label>
            Código
            <input
              name="code"
              value={form.code}
              onChange={handleChange}
              placeholder="EV-001"
              required
            />
          </label>

          <label>
            Título
            <input
              name="title"
              value={form.title}
              onChange={handleChange}
              placeholder="Evidencia de control de acceso"
              required
            />
          </label>

          <label>
            Tipo de evidencia
            <input
              name="evidence_type"
              value={form.evidence_type}
              onChange={handleChange}
              placeholder="Documento, Log, Captura..."
            />
          </label>

          <label>
            Estado
            <select
              name="status"
              value={form.status}
              onChange={handleChange}
            >
              <option value="Active">Active</option>
              <option value="Inactive">Inactive</option>
              <option value="Archived">Archived</option>
            </select>
          </label>

          <label>
            Responsable
            <input
              name="owner"
              value={form.owner}
              onChange={handleChange}
              placeholder="Responsable de la evidencia"
            />
          </label>

          <label>
            Fuente
            <input
              name="source"
              value={form.source}
              onChange={handleChange}
              placeholder="Sistema, auditoría, documento..."
            />
          </label>

          <label>
            Fecha de recolección
            <input
              type="date"
              name="collected_at"
              value={form.collected_at}
              onChange={handleChange}
            />
          </label>

          <label>
            Ruta del archivo
            <input
              name="file_path"
              value={form.file_path}
              onChange={handleChange}
              placeholder="/evidence/EV-001.pdf"
            />
          </label>

          <label>
            ID Riesgo
            <input
              type="number"
              name="risk_id"
              value={form.risk_id}
              onChange={handleChange}
              min="1"
            />
          </label>

          <label>
            ID Control ISO
            <input
              type="number"
              name="iso_control_id"
              value={form.iso_control_id}
              onChange={handleChange}
              min="1"
            />
          </label>

          <label>
            ID Evento
            <input
              type="number"
              name="event_id"
              value={form.event_id}
              onChange={handleChange}
              min="1"
            />
          </label>

          <label>
            SHA-256
            <input
              name="hash_sha256"
              value={form.hash_sha256}
              onChange={handleChange}
              placeholder="64 caracteres hexadecimales"
              maxLength={64}
            />
          </label>
        </div>

        <label>
          Descripción
          <textarea
            name="description"
            value={form.description}
            onChange={handleChange}
            rows={4}
            placeholder="Describe qué demuestra esta evidencia..."
          />
        </label>

        <div className="table-actions">
          <button type="submit" disabled={saving}>
            {saving
              ? "Guardando..."
              : editing
                ? "Actualizar evidencia"
                : "Crear evidencia"}
          </button>

          {editing && (
            <button
              type="button"
              onClick={onCancel}
              disabled={saving}
            >
              Cancelar
            </button>
          )}
        </div>
      </form>
    </div>
  );
}
