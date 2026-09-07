import { useCallback, useEffect, useState } from "react";

import {
  getEvidence,
  createEvidence,
  updateEvidence,
  deleteEvidence
} from "../api";

export function useEvidence() {
  const [evidence, setEvidence] = useState([]);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  const loadEvidence = useCallback(async () => {
    try {
      setLoading(true);
      setError("");

      const data = await getEvidence();

      setEvidence(
        Array.isArray(data)
          ? data
          : Array.isArray(data?.items)
            ? data.items
            : Array.isArray(data?.data)
              ? data.data
              : []
      );
    } catch (err) {
      console.error("Error loading evidence:", err);
      setError(err.message || "Error cargando evidencias");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadEvidence();
  }, [loadEvidence]);

  const create = useCallback(async (data) => {
    try {
      setSaving(true);
      setError("");

      await createEvidence(data);
      await loadEvidence();

      return true;
    } catch (err) {
      console.error("Error creating evidence:", err);
      setError(err.message || "Error creando evidencia");
      return false;
    } finally {
      setSaving(false);
    }
  }, [loadEvidence]);

  const update = useCallback(async (code, data) => {
    try {
      setSaving(true);
      setError("");

      await updateEvidence(code, data);
      await loadEvidence();

      return true;
    } catch (err) {
      console.error("Error updating evidence:", err);
      setError(err.message || "Error actualizando evidencia");
      return false;
    } finally {
      setSaving(false);
    }
  }, [loadEvidence]);

  const remove = useCallback(async (code) => {
    if (!window.confirm(`¿Eliminar la evidencia ${code}?`)) {
      return false;
    }

    try {
      setSaving(true);
      setError("");

      await deleteEvidence(code);
      await loadEvidence();

      return true;
    } catch (err) {
      console.error("Error deleting evidence:", err);
      setError(err.message || "Error eliminando evidencia");
      return false;
    } finally {
      setSaving(false);
    }
  }, [loadEvidence]);

  return {
    evidence,
    loading,
    saving,
    error,
    loadEvidence,
    create,
    update,
    remove
  };
}
