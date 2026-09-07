import { useState } from "react";

import IncidentStats from "../components/incidents/IncidentStats";
import IncidentForm from "../components/incidents/IncidentForm";
import IncidentTable from "../components/incidents/IncidentTable";

export default function IncidentsView({
  incidents = [],
  statistics,
  onCreateIncident,
  onUpdateIncident,
  onDeleteIncident
}) {
  const [editingIncident, setEditingIncident] = useState(null);
  const [saving, setSaving] = useState(false);
  const [deletingId, setDeletingId] = useState(null);

  const handleCreate = async (data) => {
    try {
      setSaving(true);
      await onCreateIncident(data);
    } finally {
      setSaving(false);
    }
  };

  const handleUpdate = async (id, data) => {
    try {
      setSaving(true);
      await onUpdateIncident(id, data);
      setEditingIncident(null);
    } finally {
      setSaving(false);
    }
  };

  const handleEdit = (incident) => {
    setEditingIncident(incident);
  };

  const handleCancelEdit = () => {
    setEditingIncident(null);
  };

  const handleDelete = async (incident) => {
    const confirmed = window.confirm(
      `¿Eliminar el incidente ${incident.code || incident.id}?`
    );

    if (!confirmed) {
      return;
    }

    try {
      setDeletingId(incident.id);

      await onDeleteIncident(incident.id);

      if (editingIncident?.id === incident.id) {
        setEditingIncident(null);
      }
    } finally {
      setDeletingId(null);
    }
  };

  return (
    <>
      <IncidentStats
        incidents={incidents}
        statistics={statistics}
      />

      <IncidentForm
        initialData={editingIncident}
        saving={saving}
        onCreate={handleCreate}
        onUpdate={handleUpdate}
        onCancel={handleCancelEdit}
      />

      <IncidentTable
        incidents={incidents}
        onEdit={handleEdit}
        onDelete={handleDelete}
        deletingId={deletingId}
      />
    </>
  );
}
