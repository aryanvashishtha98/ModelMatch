import { FaCheckCircle } from "react-icons/fa";

const statuses = [
  {
    title: "Backend",
    value: "Online",
  },
  {
    title: "Database",
    value: "Connected",
  },
  {
    title: "AutoML Engine",
    value: "Ready",
  },
  {
    title: "Recommendation",
    value: "Ready",
  },
];

const StatusBadge = () => {
  return (
    <div
      style={{
        display:"grid",

gridTemplateColumns:
"repeat(auto-fit,minmax(220px,1fr))",

gap:"20px",
        gap: "15px",
        flexWrap: "wrap",
        marginBottom: "30px",
      }}
    >
      {statuses.map((item) => (
        <div
          key={item.title}
          style={{
            background: "#ffffff",
            flex: 1,
            minWidth: "220px",
            borderRadius: "12px",
            padding: "18px",
            display: "flex",
            alignItems: "center",
            gap: "15px",
            boxShadow: "0 5px 15px rgba(0,0,0,.08)",
          }}
        >
          <FaCheckCircle
            color="#16a34a"
            size={30}
          />

          <div>
            <div
              style={{
                fontWeight: "bold",
                fontSize: "17px",
              }}
            >
              {item.title}
            </div>

            <div
              style={{
                color: "#16a34a",
              }}
            >
              {item.value}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default StatusBadge;