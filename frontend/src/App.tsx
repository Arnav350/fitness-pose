import { useState, useEffect } from "react";

function App() {
  const [stage, setStage] = useState(null);
  const [reps, setReps] = useState(0);

  const startScript = async () => {
    try {
      const response = await fetch("http://localhost:5000/start", { method: "POST" });
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
    }
  };

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const response = await fetch("http://localhost:5000/status");
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        setStage(data.stage);
        setReps(data.reps);
      } catch (error) {
        console.error("There was a problem with the fetch operation:", error);
      }
    }, 1000); // Poll every second

    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h1>Pose Detection</h1>
      <button onClick={startScript}>Start</button>
      <div>
        <p>Stage: {stage}</p>
        <p>Reps: {reps}</p>
      </div>
    </div>
  );
}

export default App;
