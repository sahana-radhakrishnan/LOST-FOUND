import { BrowserRouter, Link, Route, Routes } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import ReportLostItem from "./pages/ReportLostItem";
import DetectionFeed from "./pages/DetectionFeed";
import PossibleMatches from "./pages/PossibleMatches";
import MatchDetails from "./pages/MatchDetails";
import Alerts from "./pages/Alerts";

function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Dashboard</Link>{" "}
        <Link to="/report-lost">Report Lost</Link>{" "}
        <Link to="/detections">Detection Feed</Link>{" "}
        <Link to="/matches">Possible Matches</Link>{" "}
        <Link to="/alerts">Alerts</Link>
      </nav>

      <main>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route
            path="/report-lost"
            element={<ReportLostItem />}
          />
          <Route
            path="/detections"
            element={<DetectionFeed />}
          />
          <Route
            path="/matches"
            element={<PossibleMatches />}
          />
          <Route
            path="/matches/:id"
            element={<MatchDetails />}
          />
          <Route path="/alerts" element={<Alerts />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}

export default App;