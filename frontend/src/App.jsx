import React, { useState } from "react";
import axios from "axios";

export default function App() {
  const [file, setFile] = useState(null);
  const [transcript, setTranscript] = useState("");
  const [summary, setSummary] = useState("");
  const [keywords, setKeywords] = useState([]);
  const [questions, setQuestions] = useState([]);

  const onFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const onTranscribe = async () => {
    if (!file) return;
    const form = new FormData();
    form.append("audio", file);
    const res = await axios.post(
      "http://127.0.0.1:8000/transcribe",
      form
    );
    setTranscript(res.data.text);
    // clear downstream state
    setSummary("");
    setKeywords([]);
    setQuestions([]);
  };

  const onSummarize = async () => {
    if (!transcript) return;
    // write the transcript to the server's samples folder first:
    // we assume backend already wrote transcript.txt
    const res = await axios.post(
      "http://127.0.0.1:8000/summarize",
      { path: "backend/samples/transcript.txt" }
    );
    setSummary(res.data.summary);
    setKeywords(res.data.keywords);
  };

  const onQuiz = async () => {
    if (!transcript) return;
    const res = await axios.post(
      "http://127.0.0.1:8000/quiz",
      { text: transcript }
    );
    setQuestions(res.data.questions);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>AI Note & Quiz App</h1>

      <input type="file" accept="audio/*" onChange={onFileChange} />
      <button
        onClick={onTranscribe}
        disabled={!file}
        style={{ marginLeft: "1rem" }}
      >
        Transcribe
      </button>

      {transcript && (
        <>
          <div style={{ marginTop: "2rem" }}>
            <h2>Transcript</h2>
            <p>{transcript}</p>
          </div>

          <div style={{ marginTop: "1rem" }}>
            <button onClick={onSummarize}>Summarize</button>
            <button
              onClick={onQuiz}
              style={{ marginLeft: "1rem" }}
            >
              Generate Quiz
            </button>
          </div>

          {summary && (
            <div style={{ marginTop: "1rem" }}>
              <h2>Summary</h2>
              <p>{summary}</p>
              <h3>Keywords</h3>
              <ul>
                {keywords.map((kw) => (
                  <li key={kw}>{kw}</li>
                ))}
              </ul>
            </div>
          )}

          {questions.length > 0 && (
            <div style={{ marginTop: "1rem" }}>
              <h2>Quiz</h2>
              {questions.map((q, i) => (
                <div key={i} style={{ marginBottom: "1rem" }}>
                  <p>
                    <strong>Q{i + 1}:</strong> {q.question}?
                  </p>
                  <ol>
                    {q.choices.map((c, idx) => (
                      <li key={idx}>{c}</li>
                    ))}
                  </ol>
                  <p>
                    <em>Answer: {q.answer}</em>
                  </p>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}

