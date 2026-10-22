import { useState } from "react";

import { useEvidence } from "../hooks/useEvidence";
import EvidenceForm from "../components/evidence/EvidenceForm";
import EvidenceTable from "../components/evidence/EvidenceTable";

export default function EvidenceView() {
  const {
    evidence,
    loading,
    saving,
    error,
    create,
    update,
    remove
  } = useEvidence();

  const [editingEvidence, setEditingEvidence] = useState(null);
  const [showForm, setShowForm] = useState(false);

  const handleCreate = async (data) => {
    const success = await create(data);

    if (success) {
      setShowForm(false);
      setEditingEvidence(null);
    }
  };

  const handleUpdate = async (data) => {
    if (!editingEvidence) {
      return;
    }

    const success = await update(editingEvidence.code, data);

    if (success) {
      setEditingEvidence(null);
      setShowForm(false);
    }
  };

  const handleEdit = (item) => {
    setEditingEvidence(item);
    setShowForm(true);
  };

  const handleCancel = () => {
    setEditingEvidence(null);
    setShowForm(false);
  };

  return (
    <div className="page-section">
      <div className="section-header">
        <div>
          <h2>Evidence Management</h2>
          <p>
            Gestión de evidencias asociadas a riesgos y controles ISO 27001.
          </p>
        </div>

        {!showForm && (
          <button
            type="button"
            onClick={() => {
              setEditingEvidence(null);
              setShowForm(true);
            }}
          >
            + Nueva evidencia
          </button>
        )}
      </div>

      {error && (
        <div className="panel">
          <p>{error}</p>
        </div>
      )}

      {showForm && (
        <EvidenceForm
          initialData={editingEvidence}
          saving={saving}
          onSubmit={
            editingEvidence
              ? handleUpdate
              : handleCreate
          }
          onCancel={handleCancel}
        />
      )}

      <EvidenceTable
        evidence={evidence}
        loading={loading}
        onEdit={handleEdit}
        onDelete={remove}
      />
    </div>
  );
}
