import { useEffect, useState } from "react";
import { getDetections } from "../services/api";

function DetectionFeed() {
  const [detections, setDetections] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadDetections = async () => {
      try {
        const data = await getDetections();
        setDetections(Array.isArray(data) ? data : []);
      } catch (error) {
        console.error("Failed to load detections:", error);
      } finally {
        setLoading(false);
      }
    };

    loadDetections();
  }, []);

  if (loading) {
    return <p>Loading detections...</p>;
  }

  return (
    <div>
      <h1>Found Item / Detection Feed</h1>

      {detections.length === 0 ? (
        <p>No detections available.</p>
      ) : (
        detections.map((detection) => (
          <div key={detection.detection_id}>
            <h3>{detection.object_name}</h3>

            <p>
              Confidence:{" "}
              {detection.confidence !== undefined
                ? `${(detection.confidence * 100).toFixed(1)}%`
                : "N/A"}
            </p>

            <p>Location: {detection.location || "Unknown"}</p>

            <p>
              Detected: {detection.detected_at || "Unknown"}
            </p>
          </div>
        ))
      )}
    </div>
  );
}

export default DetectionFeed;