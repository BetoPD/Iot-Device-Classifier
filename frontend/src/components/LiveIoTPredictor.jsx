import { useState } from "react";
import axios from "axios";

export default function LiveIoTPredictor() {
  const [inputData, setInputData] = useState("{}");
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    try {
      setLoading(true);
      const response = await axios.post("http://localhost:8000/predict", {
        features: JSON.parse(inputData),
      });
      setPrediction(response.data);
    } catch (error) {
      console.error("Prediction error:", error);
      setPrediction({ error: "Failed to get prediction" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black text-purple-300 font-mono p-6">
      <div className="max-w-4xl mx-auto bg-zinc-900 border border-purple-500 rounded-2xl p-8 shadow-xl shadow-purple-500/10">
        <h1 className="text-3xl font-bold text-purple-400 mb-6">
          IoT Device Category Predictor
        </h1>

        <textarea
          className="w-full bg-black text-purple-200 border border-purple-500 rounded-md p-4 mb-4 resize-none focus:outline-none focus:ring-2 focus:ring-purple-600"
          rows={10}
          value={inputData}
          onChange={(e) => setInputData(e.target.value)}
          placeholder="Enter JSON input with selected features"
        />

        <button
          onClick={handleSubmit}
          disabled={loading}
          className="bg-purple-700 hover:bg-purple-600 text-white font-semibold py-2 px-6 rounded transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? "Predicting..." : "Predict"}
        </button>

        {prediction && (
          <div className="mt-8 bg-zinc-800 p-6 rounded-lg border border-purple-500">
            <h2 className="text-xl font-semibold text-purple-300 mb-2">
              Prediction Result:
            </h2>
            <pre className="text-purple-100 text-sm whitespace-pre-wrap">
              {JSON.stringify(prediction, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}
