import {
    FaMedal,
    FaDatabase,
    FaRobot,
    FaBullseye,
  } from "react-icons/fa";
  
  const colors = [
    "#FFD700", // Gold
    "#B8B8C0", // Silver (slightly cooler/brighter than plain grey)
    "#CD7F32", // Bronze
  ];
  
  const getMedalColor = (index) => colors[index] || "#94a3b8";
  
  const RecommendationCards = ({ recommendation }) => {
    if (!recommendation || recommendation.length === 0) return null;
  
    return (
      <div
        style={{
          marginTop: "30px",
          marginBottom: "30px",
        }}
      >
        <h2
          style={{
            textAlign: "center",
            marginBottom: "25px",
          }}
        >
          AI Recommendations
        </h2>
  
        <div
          style={{
            display: "grid",
  
            gridTemplateColumns:
              "repeat(auto-fit,minmax(320px,1fr))",
  
            gap: "25px",
          }}
        >
          {recommendation.map((item, index) => (
            <div
              className="card-hover"
              key={index}
              style={{
                width: "100%",
                transition: "all .35s ease",
                background: "#fff",
                borderRadius: "15px",
                padding: "20px",
                boxShadow: "0 5px 15px rgba(0,0,0,.12)",
                borderTop: `8px solid ${getMedalColor(index)}`,
              }}
            >
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "10px",
                }}
              >
                <FaMedal size={28} color={getMedalColor(index)} />
  
                <h3
                  style={{
                    fontWeight: "bold",
                    color: "#1e293b",
                  }}
                >
                  Recommendation #{index + 1}
                </h3>
              </div>
  
              <hr />
  
              <p>
                <FaDatabase /> <b>Dataset</b>
              </p>
  
              <h3>{item.dataset}</h3>
  
              <p>
                <FaRobot /> <b>Recommended Model</b>
              </p>
  
              <h3>{item.model}</h3>
  
              <p>
                <FaBullseye /> <b>Historical Accuracy</b>
              </p>
  
              <h2
                style={{
                  color: "#16a34a",
                }}
              >
                {(item.score * 100).toFixed(2)}%
              </h2>
  
              <p>
                <b>Similarity Distance</b>
              </p>
  
              <h3>{item.distance}</h3>
  
              <div
                style={{
                  marginTop: "20px",
                  background: "#eff6ff",
                  padding: "12px",
                  borderRadius: "10px",
                  color: "#1d4ed8",
                }}
              >
                Most similar historical dataset based on extracted
                meta-features.
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };
  
  export default RecommendationCards;