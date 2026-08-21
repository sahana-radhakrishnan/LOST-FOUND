import { useEffect, useState } from "react";
import { getAlerts } from "../services/api";

function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadAlerts = async () => {
      try {
        const data = await getAlerts();

        setAlerts(
          Array.isArray(data) ? data : [],
        );
      } catch (error) {
        console.log("Alerts API unavailable:", error);
        setAlerts([]);
      } finally {
        setLoading(false);
      }
    };

    loadAlerts();
  }, []);

  const getAlertClass = (type) => {
    if (type === "MATCH_FOUND") {
      return "alert-success";
    }

    if (type === "POSSIBLE_MATCH") {
      return "alert-warning";
    }

    return "alert-info";
  };

  return (
    <>
      <div className="page-header">
        <h1>Alerts</h1>
        <p>
          Notifications generated during investigations.
        </p>
      </div>

      {loading ? (
        <div className="card empty-state">
          <div className="loading-spinner" />
          <p>Loading alerts...</p>
        </div>
      ) : alerts.length === 0 ? (
        <div className="card empty-state large-empty">
          <div className="empty-icon">!</div>

          <h2>No active alerts</h2>

          <p>
            Strong matches and investigation events will
            appear here.
          </p>
        </div>
      ) : (
        <div className="alerts-list">
          {alerts.map((alert) => (
            <div
              className={`alert-card ${getAlertClass(
                alert.alert_type,
              )}`}
              key={alert.alert_id}
            >
              <div className="alert-icon">
                !
              </div>

              <div className="alert-content">
                <div className="alert-title-row">
                  <h3>
                    {alert.alert_type ||
                      "Investigation Alert"}
                  </h3>

                  <span className="badge badge-info">
                    {alert.status || "PENDING"}
                  </span>
                </div>

                <p>
                  {alert.message ||
                    "An investigation event requires attention."}
                </p>

                {alert.match_id && (
                  <div className="alert-match">
                    Match #{alert.match_id}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </>
  );
}

export default Alerts;