export default function EvidenceTable({
  evidence = [],
  loading = false,
  onEdit,
  onDelete
}) {
  if (loading) {
    return (
      <div className="panel">
        <p>Cargando evidencias...</p>
      </div>
    );
  }

  if (!evidence.length) {
    return (
      <div className="panel">
        <p>No hay evidencias registradas.</p>
      </div>
    );
  }

  return (
    <div className="panel">
      <div className="panel-header">
        <div>
          <h3>Evidence Register</h3>
          <p>Registro de evidencias asociadas a riesgos y controles.</p>
        </div>

        <span className="badge">
          {evidence.length} evidencias
        </span>
      </div>

      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Código</th>
              <th>Título</th>
              <th>Tipo</th>
              <th>Estado</th>
              <th>Riesgo</th>
              <th>ISO Control</th>
              <th>Responsable</th>
              <th>Acciones</th>
            </tr>
          </thead>

          <tbody>
            {evidence.map((item) => (
              <tr key={item.id ?? item.code}>
                <td>
                  <strong>{item.code}</strong>
                </td>

                <td>{item.title}</td>

                <td>
                  {item.evidence_type || "—"}
                </td>

                <td>
                  <span className="status-badge">
                    {item.status || "Active"}
                  </span>
                </td>

                <td>
                  {item.risk_id ?? "—"}
                </td>

                <td>
                  {item.iso_control_id ?? "—"}
                </td>

                <td>
                  {item.owner || "—"}
                </td>

                <td>
                  <div className="table-actions">
                    <button
                      type="button"
                      onClick={() => onEdit?.(item)}
                    >
                      Editar
                    </button>

                    <button
                      type="button"
                      onClick={() => onDelete?.(item.code)}
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
    </div>
  );
}
