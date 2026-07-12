import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
    CartesianGrid,
  } from "recharts";
  
  const AccuracyChart = ({ tuning }) => {
    if (!tuning || tuning.length === 0) return null;
  
    const data = tuning.map((item) => ({
      name: item.model,
      Accuracy: Number((item.best_score * 100).toFixed(2)),
    }));
  
    return (
      <div className="card-hover"
        style={{
          background: "#fff",
          padding: "25px",
          borderRadius: "15px",
          marginTop: "25px",
          boxShadow: "0 5px 15px rgba(0,0,0,0.1)",
        }}
      >
        <h2
          style={{
            textAlign: "center",
            marginBottom: "20px",
          }}
        >
          Accuracy Comparison
        </h2>
  
        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
  
            <XAxis dataKey="name" />
  
            <YAxis domain={[0, 100]} />
  
            <Tooltip />
  
            <Bar dataKey="Accuracy" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    );
  };
  
  export default AccuracyChart;