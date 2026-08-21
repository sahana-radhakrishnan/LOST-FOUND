import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Lost items
export const getLostItems = async () => {
  const response = await api.get("/api/lost-items");
  return response.data;
};

export const createLostItem = async (item) => {
  const response = await api.post("/api/lost-items", item);
  return response.data;
};

// YOLO detections
export const getDetections = async () => {
  const response = await api.get("/api/detections");
  return response.data;
};

// Matches
export const getMatches = async () => {
  const response = await api.get("/api/matches");
  return response.data;
};

// Alerts
export const getAlerts = async () => {
  const response = await api.get("/api/alerts");
  return response.data;
};

export default api;