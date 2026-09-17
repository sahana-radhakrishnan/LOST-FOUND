import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getMatches, getMediaUrl } from "../services/api";

function PossibleMatches() {
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadMatches = async () => {
      try {
        const data = await getMatches();

        setMatches(
          Array.isArray(data) ? data : [],
        );
      } catch (error) {
        console.log("Matches API unavailable:", error);
        setMatches([]);
      } finally {
        setLoading(false);
      }
    };

    loadMatches();
  }, []);

  const getDecisionClass = (decision) => {
    if (decision === "MATCH" || decision === "MATCH_FOUND") {
      return "badge-success";
    }

    if (decision === "POSSIBLE_MATCH") {
      return "badge-warning";
    }

    return "badge-danger";
  };

  return (
    <>
      <div className="page-header">
        <h1>Possible Matches</h1>
        <p>
          Review matches identified by the investigation agent.
        </p>
      </div>

      {loading ? (
        <div className="card empty-state">
          <div className="loading-spinner" />
          <p>Searching for matches...</p>
        </div>
      ) : matches.length === 0 ? (
        <div className="card empty-state large-empty">
          <div className="empty-icon">⌕</div>

          <h2>No matches found</h2>

          <p>
            Matches created by the investigation agent will
            appear here.
          </p>
        </div>
      ) : (
        <div className="matches-list">
          {matches.map((match) => {
            const score =
              Number(match.match_score || 0) * 100;

            return (
              <div
                className="match-card"
                key={match.id}
              >
                {(match.detection?.image_url || match.detection?.image_path) && (
                  <img
                    className="match-thumbnail"
                    src={getMediaUrl(
                      match.detection.image_url || match.detection.image_path,
                    )}
                    alt={`Detected ${match.detection.object || "matched item"}`}
                  />
                )}

                <div className="match-main">
                  <div className="match-icon">⌕</div>

                  <div className="match-information">
                    <div className="match-title-row">
                      <h3>
                        Match #{match.id}
                      </h3>

                      <span
                        className={`badge ${getDecisionClass(
                          match.decision,
                        )}`}
                      >
                        {match.decision ||
                          "POSSIBLE_MATCH"}
                      </span>
                    </div>

                    <p>
                      {match.reason ||
                        "The agent identified similarities between the lost item and detection."}
                    </p>

                    <div className="match-ids">
                      <span>
                        Lost Item:{" "}
                        <strong>
                          #{match.lost_item_id}
                        </strong>
                      </span>

                      <span>
                        Detection:{" "}
                        <strong>
                          #{match.detection_id}
                        </strong>
                      </span>
                    </div>

                    <div className="matched-detection-summary">
                      <strong>Matched Detection</strong>
                      <span>{match.detection?.object || "Object unavailable"}</span>
                      <span>
                        {match.detection
                          ? `${(Number(match.detection.confidence) * 100).toFixed(1)}% confidence`
                          : "Confidence unavailable"}
                      </span>
                      <span>{match.detection?.location || "Location unavailable"}</span>
                      <span>{match.detection?.timestamp || "Time unavailable"}</span>
                    </div>
                  </div>
                </div>

                <div className="match-score">
                  <div className="score">
                    {score.toFixed(1)}%
                  </div>

                  <div className="score-label">
                    Match confidence
                  </div>

                  <div className="score-bar">
                    <div
                      className="score-fill"
                      style={{
                        width: `${score}%`,
                      }}
                    />
                  </div>

                  <Link
                    className="secondary-button"
                    to={`/matches/${match.id}`}
                    state={{ match }}
                  >
                    View Details
                  </Link>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </>
  );
}

export default PossibleMatches;