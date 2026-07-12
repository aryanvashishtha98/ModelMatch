import {
    FaDatabase,
    FaTable,
    FaLayerGroup,
    FaBullseye,
    FaCheckCircle,
    FaRobot,
  } from "react-icons/fa";
  
  const cardStyle = (color) => ({
    background: color,
    color: "white",
    borderRadius: "15px",
    padding: "20px",
    flex: "1",
    minWidth: "180px",
    textAlign: "center",
    boxShadow: "0 5px 15px rgba(0,0,0,0.15)",
  });
  
  const DatasetSummary = ({ uploadResult, tuning }) => {
    if (!uploadResult) return null;
  
    const meta = uploadResult.data.meta_features;
  
    const bestModel =
      tuning && tuning.length > 0
        ? tuning[0].model
        : "Not Tuned";
  
    const bestAccuracy =
      tuning && tuning.length > 0
        ? (tuning[0].best_score * 100).toFixed(2) + "%"
        : "--";
  
    return (
        <div
        style={{
            display: "grid",
            gridTemplateColumns:
                "repeat(auto-fit,minmax(220px,1fr))",
            gap: "20px",
            marginBottom: "30px",
        }}
    >
        <div style={cardStyle("#2563eb")}>
          <FaDatabase size={35} />
          <h3>Dataset</h3>
          <h4>{uploadResult.data.dataset_name}</h4>
        </div>
  
        <div style={cardStyle("#16a34a")}>
          <FaTable size={35} />
          <h3>Rows</h3>
          <h2>{meta.rows}</h2>
        </div>
  
        <div style={cardStyle("#9333ea")}>
          <FaLayerGroup size={35} />
          <h3>Columns</h3>
          <h2>{meta.columns}</h2>
        </div>
  
        <div style={cardStyle("#f97316")}>
          <FaBullseye size={35} />
          <h3>Classes</h3>
          <h2>{meta.nr_class}</h2>
        </div>
  
        <div style={cardStyle("#059669")}>
          <FaRobot size={35} />
          <h3>Best Model</h3>
          <h4>{bestModel}</h4>
        </div>
  
        <div style={cardStyle("#dc2626")}>
          <FaCheckCircle size={35} />
          <h3>Accuracy</h3>
          <h2>{bestAccuracy}</h2>
        </div>
      </div>
    );
  };
  
  export default DatasetSummary;