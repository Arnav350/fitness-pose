import { useState, useEffect } from "react";

function App() {
  const [leftStage, setLeftStage] = useState(null);
  const [rightStage, setRightStage] = useState(null);
  const [leftReps, setLeftReps] = useState(0);
  const [rightReps, setRightReps] = useState(0);

  const startScript = async (mode: string) => {
    try {
      const response = await fetch("http://localhost:5000/start", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ mode }),
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
        setLeftStage(data.left_stage);
        setRightStage(data.right_stage);
        setLeftReps(data.left_reps);
        setRightReps(data.right_reps);
      } catch (error) {
        console.error("There was a problem with the fetch operation:", error);
      }
    }, 1000); // Poll every second

    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h1>Pose Detection</h1>
      <button onClick={() => startScript("biceps")}>Start Biceps</button>
      <button onClick={() => startScript("triceps")}>Start Triceps</button>
      <button onClick={() => startScript("quads")}>Start Quads</button>
      <button onClick={() => startScript("hamstrings")}>Start Hamstrings</button>
      <button onClick={stopScript}>Stop</button>
      <div>
        <h2>Left Arm</h2>
        <p>Stage: {leftStage}</p>
        <p>Reps: {leftReps}</p>
      </div>
      <div>
        <h2>Right Arm</h2>
        <p>Stage: {rightStage}</p>
        <p>Reps: {rightReps}</p>
      </div>
    </div>
  );
}

export default App;
