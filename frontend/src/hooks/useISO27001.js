import { useCallback, useEffect, useState } from "react";

import {
  getISO27001Status,
  getISO27001Controls,
  getISO27001Compliance,
  getISO27001SoA,
  updateISO27001Control,
  getRiskISOControls,
  createRiskISOControl,
  deleteRiskISOControl,
  updateRiskISOControl
} from "../api";

export function useISO27001({
  selectedRisk,
  setError
}) {
  const [isoStatus, setIsoStatus] = useState(null);
  const [isoControls, setIsoControls] = useState([]);
  const [isoCompliance, setIsoCompliance] = useState(null);
  const [isoSoA, setIsoSoA] = useState(null);

  const [isoLoading, setIsoLoading] = useState(false);
  const [isoSaving, setIsoSaving] = useState(null);

  const [riskISOControls, setRiskISOControls] = useState([]);
  const [riskISOLoading, setRiskISOLoading] = useState(false);
  const [riskISOSaving, setRiskISOSaving] = useState(false);

  const loadISO27001 = useCallback(async () => {
    try {
      setIsoLoading(true);
      setError("");

      const [
        statusData,
        controlsData,
        complianceData,
        soaData
      ] = await Promise.all([
        getISO27001Status(),
        getISO27001Controls(),
        getISO27001Compliance(),
        getISO27001SoA()
      ]);

      setIsoStatus(statusData);

      setIsoControls(
        Array.isArray(controlsData)
          ? controlsData
          : []
      );

      setIsoCompliance(complianceData);
      setIsoSoA(soaData);
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setIsoLoading(false);
    }
  }, [setError]);

  const saveISOControl = useCallback(async (code, data) => {
    try {
      setIsoSaving(code);
      setError("");

      await updateISO27001Control(code, data);

      await loadISO27001();
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setIsoSaving(null);
    }
  }, [loadISO27001, setError]);

  const loadRiskISOControls = useCallback(async (risk) => {
    if (!risk?.code) {
      setRiskISOControls([]);
      return;
    }

    try {
      setRiskISOLoading(true);
      setError("");

      const data = await getRiskISOControls(risk.code);

      setRiskISOControls(
        Array.isArray(data?.iso_controls)
          ? data.iso_controls
          : []
      );
    } catch (err) {
      console.error(err);
      setError(err.message);
      setRiskISOControls([]);
    } finally {
      setRiskISOLoading(false);
    }
  }, [setError]);

  const handleCreateRiskISOControl = useCallback(async (data) => {
    if (!selectedRisk?.code) {
      setError("Debe seleccionar un riesgo.");
      return;
    }

    try {
      setRiskISOSaving(true);
      setError("");

      await createRiskISOControl(
        selectedRisk.code,
        data
      );

      await loadRiskISOControls(selectedRisk);
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setRiskISOSaving(false);
    }
  }, [selectedRisk, loadRiskISOControls, setError]);

  const handleDeleteRiskISOControl = useCallback(async (isoControlCode) => {
    if (!selectedRisk?.code) {
      setError("Debe seleccionar un riesgo.");
      return;
    }

    try {
      setRiskISOSaving(true);
      setError("");

      await deleteRiskISOControl(
        selectedRisk.code,
        isoControlCode
      );

      await loadRiskISOControls(selectedRisk);
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setRiskISOSaving(false);
    }
  }, [selectedRisk, loadRiskISOControls, setError]);

  const handleUpdateRiskISOControl = useCallback(async (isoControlCode, data) => {
    if (!selectedRisk?.code) {
      setError("Debe seleccionar un riesgo.");
      return;
    }

    try {
      setRiskISOSaving(true);
      setError("");

      await updateRiskISOControl(
        selectedRisk.code,
        isoControlCode,
        data
      );

      await loadRiskISOControls(selectedRisk);
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setRiskISOSaving(false);
    }
  }, [selectedRisk, loadRiskISOControls, setError]);

  useEffect(() => {
    loadISO27001();
  }, [loadISO27001]);

  useEffect(() => {
    if (selectedRisk?.code) {
      loadRiskISOControls(selectedRisk);
    }
  }, [selectedRisk?.code, loadRiskISOControls]);

  return {
    isoStatus,
    isoControls,
    isoCompliance,
    isoSoA,
    isoLoading,
    isoSaving,

    riskISOControls,
    riskISOLoading,
    riskISOSaving,

    loadISO27001,
    saveISOControl,
    loadRiskISOControls,
    handleCreateRiskISOControl,
    handleDeleteRiskISOControl,
    handleUpdateRiskISOControl
  };
}
