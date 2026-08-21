import { BrowserRouter, NavLink, Route, Routes } from "react-router-dom";
import "./App.css";

import Dashboard from "./pages/Dashboard";
import ReportLostItem from "./pages/ReportLostItem";
import DetectionFeed from "./pages/DetectionFeed";
import PossibleMatches from "./pages/PossibleMatches";
import MatchDetails from "./pages/MatchDetails";
import Alerts from "./pages/Alerts";

function App() {
  const navigation = [
    {
      to: "/",
      label: "Dashboard",
      icon: "⌂",
      end: true,
    },
    {
      to: "/report-lost",
      label: "Report Lost",
      icon: "＋",
    },
    {
      to: "/detections",
      label: "Detection Feed",
      icon: "◉",
    },
    {
      to: "/matches",
      label: "Possible Matches",
      icon: "⌕",
    },
    {
      to: "/alerts",
      label: "Alerts",
      icon: "!",
    },
  ];

  return (
    <BrowserRouter>
      <div className="app">
        <aside className="sidebar">
          <div className="logo">
            <div className="logo-icon">⌕</div>

            <div>
              <div className="logo-text">Lost & Found</div>
              <div className="logo-subtitle">
                Investigation System
              </div>
            </div>
          </div>

          <div className="nav-section">
            <div className="nav-title">Workspace</div>

            {navigation.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.end}
                className={({ isActive }) =>
                  `nav-link ${isActive ? "active" : ""}`
                }
              >
                <span className="nav-icon">{item.icon}</span>
                <span>{item.label}</span>
              </NavLink>
            ))}
          </div>
        </aside>

        <div className="main">
          <header className="topbar">
            <div className="topbar-title">
              Lost & Found Investigation
            </div>

            <div className="user-profile">
              <span>Investigator</span>
              <div className="avatar">S</div>
            </div>
          </header>

          <main className="content">
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

              <Route
                path="/alerts"
                element={<Alerts />}
              />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;