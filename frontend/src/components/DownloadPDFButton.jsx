import { generatePDF } from "../utils/generatePDF";
import { FaFilePdf } from "react-icons/fa";

const DownloadPDFButton = ({
  uploadResult,
  recommendation,
  tuning,
  history,
}) => {
  return (
    <div
      style={{
        textAlign: "center",
        marginTop: "30px",
        marginBottom: "30px",
      }}
    >
      <button
        onClick={() =>
          generatePDF(
            uploadResult,
            recommendation,
            tuning,
            history
          )
        }
        style={{
          background: "#dc2626",
          color: "white",
          padding: "15px 30px",
          border: "none",
          borderRadius: "10px",
          cursor: "pointer",
          fontSize: "18px",
          fontWeight: "bold",
          display: "inline-flex",
          alignItems: "center",
          gap: "10px",
        }}
      >
        <FaFilePdf />
        Download PDF Report
      </button>
    </div>
  );
};

export default DownloadPDFButton;