import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

// ==============================
// Upload Dataset
// ==============================

export const uploadDataset = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await API.post("/upload-dataset/", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

// ==============================
// Recommendation
// ==============================

export const getRecommendation = async (datasetId) => {
  const response = await API.get(
    `/get-recommendation/${datasetId}`
  );

  return response.data;
};

// ==============================
// Hyperparameter Tuning
// ==============================

export const runTuning = async (datasetId) => {
  const response = await API.post(
    `/run-tuning/${datasetId}`
  );

  return response.data;
};

// ==============================
// History
// ==============================
console.log("API FILE LOADED");

export const getHistory = async () => {
  const response = await API.get("/get-history/");

  return response.data;
};

export default API;