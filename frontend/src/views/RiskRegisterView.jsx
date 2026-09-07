import { useMemo, useState } from "react";
import StatCard from "../components/common/StatCard";
import RiskTable from "../components/risk/RiskTable";

const EMPTY_FORM = {
  code: "",
  name: "",
  description: "",
  category: "",
  probability: 1,
  impact: 1,
  risk_score: 1,
  risk_level: "Low",
  status: "Active",
  process_id: "",
  area_id: "",
  location_id: ""
};

export default function RiskRegisterView({
  risks = [],
  loading = false,
  selectedRisk,
  handleAnalyze,
  handleCreateRisk,
  handleUpdateRisk,
  handleDeleteRisk,
  statistics = {}
}) {
  const [showForm, setShowForm] = useState(false);
  const [editingRisk, setEditingRisk] = useState(null);
  const [form, setForm] = useState(EMPTY_FORM);
  const [saving, setSaving] = useState(false);
  const [search, setSearch] = useState("");
  const [levelFilter, setLevelFilter] = useState("All");
  const [statusFilter, setStatusFilter] = useState("All");

  const filteredRisks = useMemo(() => {
    const query = search.trim().toLowerCase();

    return risks.filter((risk) => {
      const matchesSearch =
        !query ||
        String(risk.code || "").toLowerCase().includes(query) ||
        String(risk.name || "").toLowerCase().includes(query) ||
        String(risk.category || "").toLowerCase().includes(query);

      const matchesLevel =
        levelFilter === "All" ||
        String(risk.risk_level || "") === levelFilter;

      const matchesStatus =
        statusFilter === "All" ||
        String(risk.status || "") === statusFilter;

      return matchesSearch && matchesLevel && matchesStatus;
    });
  }, [risks, search, levelFilter, statusFilter]);

  function openCreateForm() {
    setEditingRisk(null);
    setForm(EMPTY_FORM);
    setShowForm(true);
  }

  function openEditForm(risk) {
    setEditingRisk(risk);

    setForm({
      code: risk.code || "",
      name: risk.name || "",
      description: risk.description || "",
      category: risk.category || "",
      probability: risk.probability ?? 1,
      impact: risk.impact ?? 1,
      risk_score: risk.risk_score ?? 1,
      risk_level: risk.risk_level || "Low",
      status: risk.status || "Active",
      process_id: risk.process_id ?? "",
      area_id: risk.area_id ?? "",
      location_id: risk.location_id ?? ""
    });

    setShowForm(true);
  }

  function closeForm() {
    if (saving) return;

    setShowForm(false);
    setEditingRisk(null);
    setForm(EMPTY_FORM);
  }

  function handleChange(event) {
    const { name, value } = event.target;

    setForm((current) => ({
      ...current,
      [name]: value
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    if (!form.code.trim() || !form.name.trim()) {
      return;
    }

    const probability = Number(form.probability);
    const impact = Number(form.impact);

    const payload = {
      code: form.code.trim(),
      name: form.name.trim(),
      description: form.description.trim() || null,
      category: form.category.trim() || null,
      probability,
      impact,
      risk_score: Number(form.risk_score),
      risk_level: form.risk_level,
      status: form.status
    };

    if (form.process_id !== "") {
      payload.process_id = Number(form.process_id);
    }

    if (form.area_id !== "") {
      payload.area_id = Number(form.area_id);
    }

    if (form.location_id !== "") {
      payload.location_id = Number(form.location_id);
    }

    try {
      setSaving(true);

      if (editingRisk) {
        await handleUpdateRisk(editingRisk.id, payload);
      } else {
        await handleCreateRisk(payload);
      }

      closeForm();
    } catch (error) {
      console.error("Error saving risk:", error);
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete(risk) {
    const confirmed = window.confirm(
      `¿Seguro que deseas eliminar el riesgo ${risk.code}?\n\n${risk.name}`
    );

    if (!confirmed) return;

    try {
      await handleDeleteRisk(risk.id);
    } catch (error) {
      console.error("Error deleting risk:", error);
    }
  }

  return (
    <>
      <section className="stats-grid">
        <StatCard
          title="Total Risks"
          value={statistics.total ?? risks.length}
          icon="◈"
          description="Registered risks"
        />

        <StatCard
          title="Critical"
          value={statistics.critical ?? 0}
          icon="!"
          variant="critical"
          description="Immediate attention"
        />

        <StatCard
          title="High"
          value={statistics.high ?? 0}
          icon="▲"
          variant="high"
          description="Requires control"
        />

        <StatCard
          title="Low / Medium"
          value={(statistics.low ?? 0) + (statistics.medium ?? 0)}
          icon="●"
          description="Lower priority risks"
        />
      </section>

      <div className="panel">
        <div className="panel-header risk-register-header">
          <div>
            <h2>Complete Risk Register</h2>
            <p>
              Occupational risks currently registered in RiskGuard.
            </p>
          </div>

          <div className="risk-register-actions">
            <span className="count-badge">
              {filteredRisks.length} / {risks.length} risks
            </span>

            <button
              type="button"
              className="secondary-button"
              onClick={() => window.location.reload()}
            >
              ↻ Refresh
            </button>

            <button
              type="button"
              className="primary-button"
              onClick={openCreateForm}
            >
              + New Risk
            </button>
          </div>
        </div>

        <div className="risk-filters">
          <input
            type="search"
            placeholder="Search by code, name or category..."
            value={search}
            onChange={(event) => setSearch(event.target.value)}
          />

          <select
            value={levelFilter}
            onChange={(event) => setLevelFilter(event.target.value)}
          >
            <option value="All">All levels</option>
            <option value="Critical">Critical</option>
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
          </select>

          <select
            value={statusFilter}
            onChange={(event) => setStatusFilter(event.target.value)}
          >
            <option value="All">All status</option>
            <option value="Active">Active</option>
            <option value="Inactive">Inactive</option>
          </select>
        </div>

        <RiskTable
          risks={filteredRisks}
          loading={loading}
          selectedRisk={selectedRisk}
          handleAnalyze={handleAnalyze}
          handleEdit={openEditForm}
          handleDelete={handleDelete}
        />
      </div>

      {showForm && (
        <div className="modal-backdrop" onMouseDown={closeForm}>
          <div
            className="risk-modal"
            onMouseDown={(event) => event.stopPropagation()}
          >
            <div className="modal-header">
              <div>
                <h2>{editingRisk ? "Edit Risk" : "New Risk"}</h2>
                <p>
                  {editingRisk
                    ? "Update the registered occupational risk."
                    : "Register a new occupational risk in RiskGuard."}
                </p>
              </div>

              <button
                type="button"
                className="modal-close"
                onClick={closeForm}
                disabled={saving}
              >
                ×
              </button>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="form-grid">
                <label>
                  Code *
                  <input
                    name="code"
                    value={form.code}
                    onChange={handleChange}
                    placeholder="RISK-002"
                    required
                  />
                </label>

                <label>
                  Name *
                  <input
                    name="name"
                    value={form.name}
                    onChange={handleChange}
                    placeholder="Risk name"
                    required
                  />
                </label>

                <label className="form-full">
                  Description
                  <textarea
                    name="description"
                    value={form.description}
                    onChange={handleChange}
                    rows="3"
                    placeholder="Describe the occupational risk..."
                  />
                </label>

                <label>
                  Category
                  <input
                    name="category"
                    value={form.category}
                    onChange={handleChange}
                    placeholder="Electrical"
                  />
                </label>

                <label>
                  Status
                  <select
                    name="status"
                    value={form.status}
                    onChange={handleChange}
                  >
                    <option value="Active">Active</option>
                    <option value="Inactive">Inactive</option>
                  </select>
                </label>

                <label>
                  Probability (1–5)
                  <input
                    type="number"
                    name="probability"
                    min="1"
                    max="5"
                    value={form.probability}
                    onChange={handleChange}
                  />
                </label>

                <label>
                  Impact (1–5)
                  <input
                    type="number"
                    name="impact"
                    min="1"
                    max="5"
                    value={form.impact}
                    onChange={handleChange}
                  />
                </label>

                <label>
                  Risk Score (1–25)
                  <input
                    type="number"
                    name="risk_score"
                    min="1"
                    max="25"
                    value={form.risk_score}
                    onChange={handleChange}
                  />
                </label>

                <label>
                  Risk Level
                  <select
                    name="risk_level"
                    value={form.risk_level}
                    onChange={handleChange}
                  >
                    <option value="Low">Low</option>
                    <option value="Medium">Medium</option>
                    <option value="High">High</option>
                    <option value="Critical">Critical</option>
                  </select>
                </label>

                <label>
                  Process ID
                  <input
                    type="number"
                    name="process_id"
                    value={form.process_id}
                    onChange={handleChange}
                    placeholder="Optional"
                  />
                </label>

                <label>
                  Area ID
                  <input
                    type="number"
                    name="area_id"
                    value={form.area_id}
                    onChange={handleChange}
                    placeholder="Optional"
                  />
                </label>

                <label>
                  Location ID
                  <input
                    type="number"
                    name="location_id"
                    value={form.location_id}
                    onChange={handleChange}
                    placeholder="Optional"
                  />
                </label>
              </div>

              <div className="modal-footer">
                <button
                  type="button"
                  className="secondary-button"
                  onClick={closeForm}
                  disabled={saving}
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  className="primary-button"
                  disabled={saving}
                >
                  {saving
                    ? "Saving..."
                    : editingRisk
                      ? "Save Changes"
                      : "Create Risk"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
}
