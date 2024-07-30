import { useState, useEffect } from "react";

function App() {
  const [stage, setStage] = useState(null);
  const [reps, setReps] = useState(0);

  const startScript = async (side: string) => {
    try {
      const response = await fetch("http://localhost:5000/start", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ side }),
      });
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
    }
  };

  const stopScript = async () => {
    try {
      const response = await fetch("http://localhost:5000/stop", { method: "POST" });
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
      <button onClick={() => startScript("left")}>Start Left</button>
      <button onClick={() => startScript("right")}>Start Right</button>
      <button onClick={stopScript}>Stop</button>
      <div>
        <p>Stage: {stage}</p>
        <p>Reps: {reps}</p>
      </div>
    </div>
  );
}

export default App;
