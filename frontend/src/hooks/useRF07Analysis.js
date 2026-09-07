import { useCallback, useEffect, useState } from "react";
import { getRF07Analysis } from "../api/rf07";

export function useRF07Analysis({ enabled = true } = {}) {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadAnalysis = useCallback(async () => {
    console.log("[RF07] INICIO");

    setLoading(true);
    setError("");

    try {
      console.log("[RF07] GET /api/rf07/analysis");

      const data = await getRF07Analysis();

      console.log("[RF07] RESPUESTA OK", {
        records: data?.summary?.records,
        workers: data?.summary?.total_workers,
        accidents: data?.summary?.reported_accidents,
        municipalities: data?.municipalities?.length,
        activities: data?.activities?.length,
        trends: data?.trends?.length,
      });

      setAnalysis(data);

      console.log("[RF07] setAnalysis OK");

      return data;
    } catch (err) {
      console.error("[RF07] ERROR", err);

      setError(
        err?.message || "Error cargando análisis RF-07"
      );

      throw err;
    } finally {
      setLoading(false);
      console.log("[RF07] FIN");
    }
  }, []);

  useEffect(() => {
    console.log("[RF07] useEffect", { enabled });

    if (!enabled) {
      console.log("[RF07] DESHABILITADO");
      return;
    }

    loadAnalysis().catch((err) => {
      console.error("[RF07] ERROR CAPTURADO", err);
    });
  }, [enabled, loadAnalysis]);

  return {
    analysis,
    loading,
    error,
    loadAnalysis,
  };
}
