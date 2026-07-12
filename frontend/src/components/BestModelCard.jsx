import { FaTrophy } from "react-icons/fa";

const BestModelCard = ({ tuning, uploadResult }) => {
  if (!tuning || tuning.length === 0) return null;

  const bestModel = tuning[0];

  return (
    <div
      style={{
        background: "#ffffff",
        borderRadius: "15px",
        padding: "25px",
        marginBottom: "25px",
        boxShadow: "0 8px 20px rgba(0,0,0,0.1)",
        borderLeft: "8px solid #16a34a",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "15px",
          marginBottom: "20px",
        }}
      >
        <FaTrophy size={40} color="#f59e0b" />

        <div>
          <h2 style={{ margin: 0 }}>Best Model</h2>
          <p style={{ margin: 0, color: "#555" }}>
            Highest accuracy after hyperparameter tuning
          </p>
        </div>
      </div>

      <hr />

      <h1
        style={{
          color: "#2563eb",
          marginTop: "20px",
        }}
      >
        {bestModel.model}
      </h1>

      <h2 style={{ color: "#16a34a" }}>
        Accuracy : {(bestModel.best_score * 100).toFixed(2)}%
      </h2>

      {uploadResult && (
        <>
          <h3>Dataset Information</h3>

          <p>
            <b>Name :</b> {uploadResult.data.dataset_name}
          </p>

          <p>
            <b>Rows :</b> {uploadResult.data.meta_features.rows}
          </p>

          <p>
            <b>Columns :</b> {uploadResult.data.meta_features.columns}
          </p>

          <p>
            <b>Classes :</b> {uploadResult.data.meta_features.nr_class}
          </p>
        </>
      )}

      <h3>Best Hyperparameters</h3>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
        }}
      >
        <tbody>
          {Object.entries(bestModel.parameters).map(([key, value]) => (
            <tr key={key}>
              <td
                style={{
                  border: "1px solid #ddd",
                  padding: "10px",
                  fontWeight: "bold",
                }}
              >
                {key}
              </td>

              <td
                style={{
                  border: "1px solid #ddd",
                  padding: "10px",
                }}
              >
                {String(value)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default BestModelCard;