const LoadingOverlay = ({ loading, loadingText, progress }) => {
    if (!loading) return null;
  
    return (
      <div
        style={{
          position: "fixed",
          inset: 0,
          background: "rgba(15,23,42,.65)",
          backdropFilter: "blur(6px)",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          zIndex: 9999,
        }}
      >
        <div
          style={{
            width: "500px",
            background: "#ffffff",
            borderRadius: "20px",
            padding: "35px",
            textAlign: "center",
            boxShadow: "0 15px 40px rgba(0,0,0,.25)",
          }}
        >
          <h2
            style={{
              color: "#2563eb",
              marginBottom: "25px",
            }}
          >
            ModelMatch
          </h2>
  
          <div
            style={{
              fontSize: "19px",
              fontWeight: "bold",
              marginBottom: "25px",
            }}
          >
            {loadingText}
          </div>
  
          <div
            style={{
              width: "100%",
              height: "18px",
              background: "#e5e7eb",
              borderRadius: "20px",
              overflow: "hidden",
            }}
          >
            <div
              style={{
                width: `${progress}%`,
                height: "100%",
                background:
                  "linear-gradient(90deg,#2563eb,#4f46e5,#7c3aed)",
                transition: "width .6s ease",
              }}
            />
          </div>
  
          <h1
            style={{
              marginTop: "20px",
              color: "#2563eb",
            }}
          >
            {progress}%
          </h1>
  
          <p
            style={{
              color: "#555",
              marginTop: "15px",
            }}
          >
            Please wait while ModelMatch analyzes your dataset...
          </p>
        </div>
      </div>
    );
  };
  
  export default LoadingOverlay;