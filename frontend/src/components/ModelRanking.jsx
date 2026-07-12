import { FaMedal } from "react-icons/fa";

const medals = [
  {
    color: "#FFD700",
    title: "🥇 1st Place",
  },
  {
    color: "#C0C0C0",
    title: "🥈 2nd Place",
  },
  {
    color: "#CD7F32",
    title: "🥉 3rd Place",
  },
];

const ModelRanking = ({ tuning }) => {
  if (!tuning || tuning.length === 0) return null;

  return (
    <div
      style={{
        background: "#fff",
        marginTop: "25px",
        padding: "25px",
        borderRadius: "15px",
        boxShadow: "0 5px 15px rgba(0,0,0,0.1)",
      }}
    >
      <h2
        style={{
          textAlign: "center",
          marginBottom: "25px",
        }}
      >
        Final Model Ranking
      </h2>

      <div
        style={{
          display: "flex",
          gap: "20px",
          justifyContent: "center",
          flexWrap: "wrap",
        }}
      >
        {tuning.map((model, index) => (
          <div
            key={index}
            style={{
              width: "260px",
              borderRadius: "15px",
              padding: "20px",
              background: medals[index]?.color || "#eee",
              color: "#222",
              textAlign: "center",
              boxShadow: "0 5px 12px rgba(0,0,0,0.12)",
            }}
          >
            <FaMedal size={40} />

            <h3>{medals[index]?.title || `Rank ${index + 1}`}</h3>

            <h2>{model.model}</h2>

            <h3>
              {(model.best_score * 100).toFixed(2)}%
            </h3>

            <p>Best Accuracy</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ModelRanking;