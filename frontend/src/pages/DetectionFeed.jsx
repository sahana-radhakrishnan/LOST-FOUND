import { useEffect, useState } from "react";
import { getDetections } from "../services/api";

function DetectionFeed() {
  const [detections, setDetections] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadDetections = async () => {
      try {
        const data = await getDetections();

        setDetections(
          Array.isArray(data) ? data : [],
        );
      } catch (error) {
        console.log("Detection API unavailable:", error);
        setDetections([]);
      } finally {
        setLoading(false);
      }
    };

    loadDetections();
  }, []);

  return (
    <>
      <div className="page-header page-header-row">
        <div>
          <h1>Detection Feed</h1>
          <p>
            Objects detected by the computer vision system.
          </p>
        </div>

        <div className="live-indicator">
          <span className="live-dot" />
          Detection Feed
        </div>
      </div>

      {loading ? (
        <div className="card empty-state">
          <div className="loading-spinner" />
          <p>Loading detections...</p>
        </div>
      ) : detections.length === 0 ? (
        <div className="card empty-state large-empty">
          <div className="empty-icon">◉</div>

          <h2>No detections yet</h2>

          <p>
            Detected objects from the YOLO system will appear
            here when the detection API is available.
          </p>
        </div>
      ) : (
        <div className="items-grid">
          {detections.map((detection) => {
            const confidence =
              Number(detection.confidence || 0) * 100;

            return (
              <div
                className="item-card detection-card"
                key={detection.detection_id}
              >
                <div className="detection-card-top">
                  <div className="detection-object-icon">
                    ◉
                  </div>

                  <span className="badge badge-info">
                    DETECTED
                  </span>
                </div>

                <h3>
                  {detection.object_name ||
                    "Unknown Object"}
                </h3>

                <div className="item-meta">
                  <div>
                    <strong>Location:</strong>{" "}
                    {detection.location || "Unknown"}
                  </div>

                  <div>
                    <strong>Camera:</strong>{" "}
                    {detection.camera_id || "Unknown"}
                  </div>

                  <div>
                    <strong>Time:</strong>{" "}
                    {detection.detected_at || "Unknown"}
                  </div>
                </div>

                <div className="confidence-section">
                  <div className="confidence-header">
                    <span>Confidence</span>
                    <strong>
                      {confidence.toFixed(1)}%
                    </strong>
                  </div>

                  <div className="score-bar">
                    <div
                      className="score-fill"
                      style={{
                        width: `${confidence}%`,
                      }}
                    />
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </>
  );
}

export default DetectionFeed;