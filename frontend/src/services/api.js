import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8001",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000,
});

export const getMediaUrl = (imagePath) => {
  if (!imagePath) {
    return "";
  }

  if (/^https?:\/\//i.test(imagePath)) {
    return imagePath;
  }

  if (imagePath.startsWith("/media/")) {
    return `${api.defaults.baseURL}${imagePath}`;
  }

  const normalizedPath = imagePath.replaceAll("\\", "/");
  const resultsIndex = normalizedPath.indexOf("/results/");

  if (resultsIndex >= 0) {
    return `${api.defaults.baseURL}/media/${normalizedPath.slice(resultsIndex + "/results/".length)}`;
  }

  if (normalizedPath.toLowerCase().startsWith("results/")) {
    return `${api.defaults.baseURL}/media/${normalizedPath.slice("results/".length)}`;
  }

  if (normalizedPath.toLowerCase().startsWith("yolo/results/")) {
    return `${api.defaults.baseURL}/media/${normalizedPath.slice("yolo/results/".length)}`;
  }

  return `${api.defaults.baseURL}/media/${normalizedPath.replace(/^\/+/, "")}`;
};

export const getLostItems = async () => {
  const response = await api.get("/api/lost-items");
  return response.data;
};

export const createLostItem = async (item) => {
  const response = await api.post("/api/lost-items", item);
  return response.data;
};

export const getDetections = async () => {
  const response = await api.get("/api/detections");
  return response.data;
};

export const getMatches = async () => {
  const response = await api.get("/api/matches");
  return response.data;
};

export const getMatch = async (matchId) => {
  const response = await api.get(`/api/matches/${matchId}`);
  return response.data;
};

export const getAlerts = async () => {
  const response = await api.get("/api/alerts");
  return response.data;
};

export default api;