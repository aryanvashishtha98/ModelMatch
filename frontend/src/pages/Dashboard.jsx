import { useState } from "react";
import { toast } from "react-toastify";
import "../dashboard.css";
import Navbar from "../components/Navbar";
import DatasetSummary from "../components/DatasetSummary";
import StatusBadge from "../components/StatusBadge";
import RecommendationCards from "../components/RecommendationCards";
import BestModelCard from "../components/BestModelCard";
import AccuracyChart from "../components/AccuracyChart";
import ModelRanking from "../components/ModelRanking";
import HistoryTable from "../components/HistoryTable";
import DownloadPDFButton from "../components/DownloadPDFButton";
import LoadingOverlay from "../components/LoadingOverlay";

import {
  FaCloudUploadAlt,
} from "react-icons/fa";

import {
  uploadDataset,
  getRecommendation,
  runTuning,
  getHistory,
} from "../services/api";

const Dashboard = () => {

  const [selectedFile, setSelectedFile] = useState(null);

  const [uploadResult, setUploadResult] = useState(null);

  const [recommendation, setRecommendation] = useState(null);

  const [tuning, setTuning] = useState(null);

  const [history, setHistory] = useState([]);

  const [loading, setLoading] = useState(false);

  const [loadingRecommendation, setLoadingRecommendation] = useState(false);

  const [loadingTuning, setLoadingTuning] = useState(false);

  const [loadingHistory, setLoadingHistory] = useState(false);

  // Loading Stage (will become animated in next step)

  const [loadingText, setLoadingText] = useState("");

  const [progress, setProgress] = useState(0);



  const handleUpload = async () => {

    if (!selectedFile) {

      toast.warning("Please choose a CSV file.");

      return;

    }

    try {

      setLoading(true);

      setProgress(10);

      setLoadingText("Uploading Dataset...");

      const response = await uploadDataset(selectedFile);

      setUploadResult(response);
      toast.success("Dataset uploaded successfully.");

      setProgress(30);

      setLoadingText("Extracting Meta Features...");



      // Recommendation

      setLoadingRecommendation(true);

      setProgress(50);

      setLoadingText("Finding Similar Datasets...");

      const rec = await getRecommendation(response.data.dataset_id);

      setRecommendation(rec.data);
      toast.success("Recommendations generated.");

      setLoadingRecommendation(false);



      // Tuning

      setLoadingTuning(true);

      setProgress(75);

      setLoadingText("Running Hyperparameter Optimization...");

      const tuningResult = await runTuning(response.data.dataset_id);

      setTuning(tuningResult.verified_results.verified_results);
      toast.success("Hyperparameter tuning completed.");

      setLoadingTuning(false);



      // History

      setLoadingHistory(true);

      setProgress(95);

      setLoadingText("Saving History...");

      const historyResult = await getHistory();

      setHistory(historyResult.history);
      toast.success("History updated.");

      setLoadingHistory(false);



      setProgress(100);

      setLoadingText("Completed Successfully");

      await new Promise((resolve) =>
        setTimeout(resolve, 700)
      );

    }

    catch (err) {

      console.log(err);

      toast.error("Upload failed.");

    }

    finally {

      setLoading(false);

    }

  };



  return (

    <div
      style={{
        minHeight: "100vh",

        padding: "20px",

        background:
          "linear-gradient(135deg,#eef2ff,#f8fafc,#e0f2fe)",

        fontFamily: "Arial",
      }}
    >

      <Navbar />

      <DatasetSummary

        uploadResult={uploadResult}

        tuning={tuning}

      />

      <StatusBadge />



      {/* Upload Section */}

      <div style={uploadCard}>

        <FaCloudUploadAlt

          size={55}

          color="#2563eb"

        />

        <h2>

          Upload Dataset

        </h2>

        <p>

          Upload any CSV dataset and let ModelMatch

          automatically recommend the best ML models.

        </p>

        <input

          type="file"

          accept=".csv"

          onChange={(e) =>
            setSelectedFile(e.target.files[0])
          }

        />

        <br />

        <br />

        <button

          style={button}

          onClick={handleUpload}

        >

          {loading ? loadingText : "Upload Dataset"}

        </button>

        {uploadResult && (

          <div
            style={{
              marginTop: 25,
            }}
          >

            <strong>

              Dataset Uploaded Successfully

            </strong>

            <br />

            {uploadResult.data.dataset_name}

          </div>

        )}

      </div>

      {/* Recommendation */}

      <RecommendationCards

        recommendation={recommendation?.recommendations}

      />

      {/* Best Model */}

      <BestModelCard

        tuning={tuning}

        uploadResult={uploadResult}

      />
            {/* Accuracy Comparison */}

            <AccuracyChart tuning={tuning} />

{/* Final Ranking */}

<ModelRanking tuning={tuning} />

{/* History */}

<div
  style={{
    background: "#fff",
    borderRadius: "20px",
    padding: "25px",
    marginTop: "35px",
    boxShadow: "0 8px 20px rgba(0,0,0,.08)",
  }}
>
  <div
    style={{
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      marginBottom: "20px",
    }}
  >
    <h2
      style={{
        margin: 0,
      }}
    >
      Recent Training History
    </h2>

    {history.length > 5 && (
      <span
        style={{
          color: "#2563eb",
          fontWeight: "bold",
        }}
      >
        Showing Latest 5 of {history.length}
      </span>
    )}
  </div>

  <HistoryTable history={history.slice(0, 5)} />
</div>

{/* PDF */}

<DownloadPDFButton
  uploadResult={uploadResult}
  recommendation={recommendation}
  tuning={tuning}
  history={history}
/>

{/* Footer */}

<div
  style={{
    marginTop: "50px",
    padding: "30px",
    textAlign: "center",
    color: "#555",
  }}
>
  <h2
    style={{
      color: "#2563eb",
      marginBottom: "8px",
    }}
  >
    ModelMatch
  </h2>

  <p>
    AI Powered Meta Learning AutoML Recommendation System
  </p>

  <p>
    Hackathon Edition • Version 1.0
  </p>

  <p>
    Developed by <b>Aryan Vashishtha</b>
  </p>
</div>

<LoadingOverlay

  loading={loading}

  loadingText={loadingText}

  progress={progress}

/>

</div>

);

};

const uploadCard = {

background: "#ffffff",

borderRadius: "22px",

padding: "40px",

textAlign: "center",

boxShadow: "0 10px 25px rgba(0,0,0,.08)",

marginBottom: "35px",

};

const button = {

background: "linear-gradient(90deg,#2563eb,#4f46e5)",

color: "white",

border: "none",

padding: "15px 30px",

borderRadius: "10px",

fontSize: "17px",

cursor: "pointer",

fontWeight: "bold",

};

export default Dashboard;