import { Link, useLocation } from "react-router-dom";

function MatchDetails() {
  const location = useLocation();
  const match = location.state?.match;

  if (!match) {
    return (
      <>
        <div className="page-header">
          <h1>Match Details</h1>
          <p>
            Detailed investigation information.
          </p>
        </div>

        <div className="card empty-state large-empty">
          <div className="empty-icon">⌕</div>

          <h2>No match selected</h2>

          <p>
            Select a match from the Possible Matches page.
          </p>

          <Link
            to="/matches"
            className="primary-button inline-button"
          >
            Back to Matches
          </Link>
        </div>
      </>
    );
  }

  const score =
    Number(match.match_score || 0) * 100;

  const decision =
    match.decision || "POSSIBLE_MATCH";

  const decisionClass =
    decision === "MATCH_FOUND"
      ? "badge-success"
      : decision === "POSSIBLE_MATCH"
        ? "badge-warning"
        : "badge-danger";

  return (
    <>
      <div className="page-header">
        <div className="breadcrumb">
          <Link to="/matches">Possible Matches</Link>
          <span>/</span>
          <span>Match #{match.match_id}</span>
        </div>

        <h1>Match Investigation</h1>

        <p>
          Detailed analysis performed by the investigation
          agent.
        </p>
      </div>

      <div className="match-detail-grid">
        <div className="card match-result-card">
          <div className="result-icon">⌕</div>

          <span
            className={`badge ${decisionClass}`}
          >
            {decision}
          </span>

          <div className="large-score">
            {score.toFixed(1)}%
          </div>

          <div className="score-label">
            Overall Match Confidence
          </div>

          <div className="score-bar large-score-bar">
            <div
              className="score-fill"
              style={{
                width: `${score}%`,
              }}
            />
          </div>
        </div>

        <div className="card">
          <h2 className="card-title">
            Investigation Summary
          </h2>

          <p className="detail-reason">
            {match.reason ||
              "No investigation reason was provided."}
          </p>

          <div className="detail-list">
            <div className="detail-row">
              <span>Match ID</span>
              <strong>#{match.match_id}</strong>
            </div>

            <div className="detail-row">
              <span>Lost Item</span>
              <strong>
                #{match.lost_item_id}
              </strong>
            </div>

            <div className="detail-row">
              <span>Detection</span>
              <strong>
                #{match.detection_id}
              </strong>
            </div>

            <div className="detail-row">
              <span>Decision</span>
              <strong>{decision}</strong>
            </div>
          </div>
        </div>
      </div>

      <div className="card investigation-note">
        <div className="info-banner-icon">i</div>

        <div>
          <strong>Agent Analysis</strong>

          <p>
            This match was evaluated using object similarity,
            description similarity, location similarity,
            timestamp similarity, and detection confidence.
          </p>
        </div>
      </div>
    </>
  );
}

export default MatchDetails;