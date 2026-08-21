import { useEffect, useState } from "react";
import { getAlerts } from "../services/api";

function Alerts() {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const loadAlerts = async () => {
      try {
        const data = await getAlerts();
        setAlerts(Array.isArray(data) ? data : []);
      } catch (error) {
        console.error("Failed to load alerts:", error);
      }
    };

    loadAlerts();
  }, []);

  return (
    <div>
      <h1>Alerts</h1>

      {alerts.length === 0 ? (
        <p>No alerts.</p>
      ) : (
        alerts.map((alert) => (
          <div key={alert.alert_id}>
            <h3>{alert.alert_type}</h3>
            <p>{alert.message}</p>
            <p>Status: {alert.status}</p>
          </div>
        ))
      )}
    </div>
  );
}

export default Alerts;