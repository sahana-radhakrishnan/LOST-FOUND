import { useLocation, useNavigate } from "react-router-dom";

function MatchDetails() {
  const location = useLocation();
  const navigate = useNavigate();

  const match = location.state?.match;

  if (!match) {
    return (
      <div>
        <h1>Match Details</h1>
        <p>No match selected.</p>

        <button onClick={() => navigate("/matches")}>
          Back to Matches
        </button>
      </div>
    );
  }

  return (
    <div>
      <h1>Match Details</h1>

      <p>
        <strong>Decision:</strong> {match.decision}
      </p>

      <p>
        <strong>Score:</strong>{" "}
        {(match.match_score * 100).toFixed(1)}%
      </p>

      <p>
        <strong>Reason:</strong> {match.reason}
      </p>

      <p>
        <strong>Lost Item:</strong> {match.lost_item_id}
      </p>

      <p>
        <strong>Detection:</strong> {match.detection_id}
      </p>
    </div>
  );
}

export default MatchDetails;