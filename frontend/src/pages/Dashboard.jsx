import { useEffect, useState } from "react";
import {
  getLostItems,
  getDetections,
  getMatches,
  getAlerts,
} from "../services/api";

function Dashboard() {
  const [stats, setStats] = useState({
    lostItems: 0,
    detections: 0,
    matches: 0,
    alerts: 0,
  });

  useEffect(() => {
    const loadStats = async () => {
      try {
        const [lostItems, detections, matches, alerts] =
          await Promise.all([
            getLostItems(),
            getDetections(),
            getMatches(),
            getAlerts(),
          ]);

        setStats({
          lostItems: Array.isArray(lostItems) ? lostItems.length : 0,
          detections: Array.isArray(detections) ? detections.length : 0,
          matches: Array.isArray(matches) ? matches.length : 0,
          alerts: Array.isArray(alerts) ? alerts.length : 0,
        });
      } catch (error) {
        console.error("Failed to load dashboard:", error);
      }
    };

    loadStats();
  }, []);

  return (
    <div>
      <h1>Lost & Found Investigation</h1>

      <div className="dashboard-grid">
        <div>
          <h3>Lost Items</h3>
          <p>{stats.lostItems}</p>
        </div>

        <div>
          <h3>Detections</h3>
          <p>{stats.detections}</p>
        </div>

        <div>
          <h3>Possible Matches</h3>
          <p>{stats.matches}</p>
        </div>

        <div>
          <h3>Alerts</h3>
          <p>{stats.alerts}</p>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;