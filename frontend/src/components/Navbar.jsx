import { FaRobot } from "react-icons/fa";

const Navbar = () => {
  return (
    <div
      style={{
        background: "linear-gradient(90deg, #2563eb, #1d4ed8)",
        color: "white",
        padding: "20px 40px",
        borderRadius: "12px",
        marginBottom: "30px",
        boxShadow: "0 8px 20px rgba(0,0,0,0.15)",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "15px",
        }}
      >
        <FaRobot size={45} />

        <div>
          <h1
            style={{
              margin: 0,
              fontSize: "32px",
              fontWeight: "bold",
            }}
          >
            ModelMatch
          </h1>

          <p
            style={{
              margin: "5px 0 0",
              opacity: 0.9,
              fontSize: "15px",
            }}
          >
            AI-Powered Meta Learning & AutoML Recommendation System
          </p>
        </div>
      </div>

      <div
        style={{
          textAlign: "right",
        }}
      >
        <div
          style={{
            fontSize: "15px",
            fontWeight: "bold",
          }}
        >
          Backend
        </div>

        <div
          style={{
            color: "#86efac",
            fontWeight: "bold",
            marginTop: "5px",
          }}
        >
          ● Connected
        </div>
      </div>
    </div>
  );
};

export default Navbar;