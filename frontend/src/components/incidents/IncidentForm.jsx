import { useEffect, useState } from "react";

const EMPTY_FORM = {
  code: "",
  title: "",
  description: "",
  incident_date: "",
  incident_type: "",
  severity: "",
  location_id: "",
  status: "Open"
};

export default function IncidentForm({
  initialData = null,
  saving = false,
  onCreate,
  onUpdate,
  onCancel
}) {
  const [form, setForm] = useState(EMPTY_FORM);
  const [formError, setFormError] = useState("");

  const isEditing = Boolean(initialData?.id);

  useEffect(() => {
    if (!initialData) {
      setForm(EMPTY_FORM);
      setFormError("");
      return;
    }

    setForm({
      code: initialData.code || "",
      title: initialData.title || "",
      description: initialData.description || "",
      incident_date: initialData.incident_date || "",
      incident_type: initialData.incident_type || "",
      severity: initialData.severity || "",
      location_id:
        initialData.location_id !== null &&
        initialData.location_id !== undefined
          ? String(initialData.location_id)
          : "",
      status: initialData.status || "Open"
    });

    setFormError("");
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
    setFormError("");

    if (!form.code.trim()) {
      setFormError("El código del incidente es obligatorio.");
      return;
    }

    if (!form.title.trim()) {
      setFormError("El título del incidente es obligatorio.");
      return;
    }

    const payload = {
      code: form.code.trim(),
      title: form.title.trim(),
      description: form.description.trim() || null,
      incident_date: form.incident_date || null,
      incident_type: form.incident_type.trim() || null,
      severity: form.severity || null,
      location_id: form.location_id
        ? Number(form.location_id)
        : null,
      status: form.status || "Open"
    };

    try {
      if (isEditing) {
        await onUpdate(initialData.id, payload);
      } else {
        await onCreate(payload);
      }

      setForm(EMPTY_FORM);
      setFormError("");
    } catch (error) {
      console.error(error);
      setFormError(
        error.message || "No se pudo guardar el incidente."
      );
    }
  };

  const handleCancel = () => {
    setForm(EMPTY_FORM);
    setFormError("");
    onCancel?.();
  };

  return (
    <div className="panel">
      <div className="panel-header">
        {isEditing ? "Edit Incident" : "New Incident"}
      </div>

      <form onSubmit={handleSubmit}>
        <div className="form-grid">
          <label>
            Code
            <input
              name="code"
              value={form.code}
              onChange={handleChange}
              placeholder="INC-003"
            />
          </label>

          <label>
            Title
            <input
              name="title"
              value={form.title}
              onChange={handleChange}
              placeholder="Incident title"
            />
          </label>

          <label>
            Incident Date
            <input
              type="date"
              name="incident_date"
              value={form.incident_date}
              onChange={handleChange}
            />
          </label>

          <label>
            Incident Type
            <input
              name="incident_type"
              value={form.incident_type}
              onChange={handleChange}
              placeholder="Electrical Failure"
            />
          </label>

          <label>
            Severity
            <select
              name="severity"
              value={form.severity}
              onChange={handleChange}
            >
              <option value="">Select severity</option>
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
              <option value="Critical">Critical</option>
            </select>
          </label>

          <label>
            Status
            <select
              name="status"
              value={form.status}
              onChange={handleChange}
            >
              <option value="Open">Open</option>
              <option value="Closed">Closed</option>
            </select>
          </label>

          <label>
            Location ID
            <input
              type="number"
              name="location_id"
              value={form.location_id}
              onChange={handleChange}
              min="1"
            />
          </label>

          <label className="form-full">
            Description
            <textarea
              name="description"
              value={form.description}
              onChange={handleChange}
              rows="4"
              placeholder="Describe the incident..."
            />
          </label>
        </div>

        {formError && (
          <div className="error-message">
            {formError}
          </div>
        )}

        <div className="table-actions">
          <button
            type="submit"
            className="primary-button"
            disabled={saving}
          >
            {saving
              ? "Saving..."
              : isEditing
                ? "Update Incident"
                : "Create Incident"}
          </button>

          {isEditing && (
            <button
              type="button"
              className="secondary-button"
              onClick={handleCancel}
              disabled={saving}
            >
              Cancel
            </button>
          )}
        </div>
      </form>
    </div>
  );
}
