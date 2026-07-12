import axios from "axios";

const API = axios.create({
  baseURL: "https://modelmatch-backend-dsc8.onrender.com",
  headers: {
    "Content-Type": "application/json",
  },
});

// ==========================
// Upload Dataset
// ==========================

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

// ==========================
// Recommendation
// ==========================

export const getRecommendation = async (datasetId) => {
  const response = await API.get(`/recommendation/${datasetId}`);
  return response.data;
};

// ==========================
// Run Hyperparameter Tuning
// ==========================

export const runTuning = async (datasetId) => {
  const response = await API.post(`/run-tuning/${datasetId}`);
  return response.data;
};

// ==========================
// Training History
// ==========================

export const getHistory = async () => {
  const response = await API.get("/get-history/");
  return response.data;
};

export default API;