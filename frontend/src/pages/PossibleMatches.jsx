import { useEffect, useState } from "react";
import { getMatches } from "../services/api";

function PossibleMatches() {
  const [matches, setMatches] = useState([]);

  useEffect(() => {
    const loadMatches = async () => {
      try {
        const data = await getMatches();
        setMatches(Array.isArray(data) ? data : []);
      } catch (error) {
        console.error("Failed to load matches:", error);
      }
    };

    loadMatches();
  }, []);

  return (
    <div>
      <h1>Possible Matches</h1>

      {matches.length === 0 ? (
        <p>No matches found.</p>
      ) : (
        matches.map((match) => (
          <div key={match.match_id}>
            <h3>
              {match.decision || "MATCH"}
            </h3>

            <p>
              Score:{" "}
              {match.match_score !== undefined
                ? `${(match.match_score * 100).toFixed(1)}%`
                : "N/A"}
            </p>

            <p>{match.reason}</p>
          </div>
        ))
      )}
    </div>
  );
}

export default PossibleMatches;