import { useCallback, useEffect, useState } from "react";

import {
  getRisks,
  getIncidents,
  getSemanticStatus,
  synchronizeSemanticGraph
} from "../api";

export function useRisks({ setSelectedRisk, setError }) {
  const [risks, setRisks] = useState([]);
  const [incidents, setIncidents] = useState([]);
  const [semantic, setSemantic] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadDashboard = useCallback(async () => {
    try {
      setLoading(true);
      setError("");

      const [riskData, incidentData, semanticData] = await Promise.all([
        getRisks(),
        getIncidents(),
        getSemanticStatus()
      ]);

      const safeRisks = Array.isArray(riskData)
        ? riskData
        : [];

      const safeIncidents = Array.isArray(incidentData)
        ? incidentData
        : [];

      setRisks(safeRisks);
      setIncidents(safeIncidents);
      setSemantic(semanticData);

      setSelectedRisk((current) => {
        if (!current && safeRisks.length > 0) {
          return safeRisks[0];
        }

        return current;
      });
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [setError, setSelectedRisk]);

  const handleSemanticSync = useCallback(async () => {
    try {
      setError("");

      await synchronizeSemanticGraph();

      const status = await getSemanticStatus();

      setSemantic(status);
    } catch (err) {
      console.error(err);
      setError(err.message);
    }
  }, [setError]);

  useEffect(() => {
    loadDashboard();
  }, [loadDashboard]);

  return {
    risks,
    incidents,
    semantic,
    loading,
    loadDashboard,
    handleSemanticSync
  };
}
