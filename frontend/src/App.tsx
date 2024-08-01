import { useState, useEffect } from "react";

function App() {
  const [leftReps, setLeftReps] = useState(0);
  const [rightReps, setRightReps] = useState(0);
  const [leftStage, setLeftStage] = useState("");
  const [rightStage, setRightStage] = useState("");

  const startPoseDetection = (mode: string) => {
    fetch("http://localhost:5000/start", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ mode }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data.message);
      })
      .catch((error) => console.error("Error:", error));
  };

  const stopPoseDetection = () => {
    fetch("http://localhost:5000/stop", {
      method: "POST",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data.message);
      })
      .catch((error) => console.error("Error:", error));
  };

  useEffect(() => {
    const interval = setInterval(() => {
      fetch("http://localhost:5000/status")
        .then((response) => response.json())
        .then((data) => {
          setLeftReps(data.left_reps);
          setRightReps(data.right_reps);
          setLeftStage(data.left_stage);
          setRightStage(data.right_stage);
        })
        .catch((error) => console.error("Error:", error));
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <h1>Exercise Tracker</h1>
      <div>
        <button onClick={() => startPoseDetection("biceps")}>Start Biceps</button>
        <button onClick={() => startPoseDetection("triceps")}>Start Triceps</button>
        <button onClick={() => startPoseDetection("quads")}>Start Quads</button>
        <button onClick={() => startPoseDetection("hamstrings")}>Start Hamstrings</button>
        <button onClick={() => startPoseDetection("chest")}>Start Chest</button>
        <button onClick={stopPoseDetection}>Stop</button>
      </div>
      <div>
        <h2>Left Side</h2>
        <p>Stage: {leftStage}</p>
        <p>Reps: {leftReps}</p>
      </div>
      <div>
        <h2>Right Side</h2>
        <p>Stage: {rightStage}</p>
        <p>Reps: {rightReps}</p>
      </div>
    </div>
  );
}

export default App;
