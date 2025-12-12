import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';

export default function App() {
  return (
    <div className="font-sans min-h-screen bg-gray-50 p-6 flex justify-center">
      <TestWithSummary />
    </div>
  );
}

function TestWithSummary() {
  const [evaluations, setEvaluations] = useState([]);
  const [active, setActive] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [generatedQuestions, setGeneratedQuestions] = useState([]);
  const [showAnswer, setShowAnswer] = useState(false);
  const [loading, setLoading] = useState(true);

  const location = useLocation();
  const { jobDescription } = location.state || {};
  const API_URL = 'https://smart-hr-assistant-backend.onrender.com';
  // Fetch questions on load
  useEffect(() => {
    if (!jobDescription) return;

    const fetchData = async () => {
      setLoading(true);

      const formData = new FormData();
      formData.append('job_description', jobDescription);

      // const res = await fetch('http://localhost:8000/practice_question/', {
      //   method: 'POST',
      //   body: formData,
      // });
      const res = await fetch(`${API_URL}/practice_question/`, {
        method: 'POST',
        body: formData,
      });

      const data = await res.json();

      setGeneratedQuestions(data.questions || []);
      setAnswers(Array((data.questions || []).length).fill(''));
      setEvaluations(Array((data.questions || []).length).fill([]));

      setLoading(false);
    };

    fetchData();
  }, [jobDescription]);

  async function handleNext() {
    if (!showAnswer) {
      setShowAnswer(true);

      const q = generatedQuestions[active].q;
      const ans = answers[active];

      const fd = new FormData();
      fd.append('question', q);
      fd.append('answer', ans);

      // const res = await fetch('http://localhost:8000/analyse_answer/', {
      //   method: 'POST',
      //   body: fd,
      // });
      const res = await fetch(`${API_URL}/analyse_answer/`, {
        method: 'POST',
        body: fd,
      });

      const data = await res.json();

      const copy = [...evaluations];
      copy[active] = data.response || [];
      setEvaluations(copy);

      return;
    }

    setShowAnswer(false);
    setActive(active + 1);
  }

  const handleAnswer = (value) => {
    const copy = [...answers];
    copy[active] = value;
    setAnswers(copy);
  };

  if (loading) {
    return <h2 className="text-xl font-bold">Loading Questions...</h2>;
  }

  if (generatedQuestions.length === 0) {
    return <h2 className="text-xl text-red-600">No questions received.</h2>;
  }

  const progress = ((active + 1) / generatedQuestions.length) * 100;

  return (
    <div className="w-full max-w-3xl">
      {/* Progress Bar */}
      <div className="w-full bg-gray-300 rounded-full h-2 mb-6">
        <div
          className="h-2 bg-blue-600 rounded-full"
          style={{ width: `${progress}%` }}
        />
      </div>

      {/* Question Navigation */}
      <div className="flex gap-3 mb-6">
        {generatedQuestions.map((_, idx) => (
          <button
            key={idx}
            className={`px-4 py-2 rounded-full ${
              active === idx
                ? 'bg-blue-600 text-white'
                : 'bg-white border text-gray-600'
            }`}
            onClick={() => {
              setActive(idx);
              setShowAnswer(false);
            }}
          >
            Q{idx + 1}
          </button>
        ))}
      </div>

      {/* Question Card */}
      <div className="bg-white p-6 shadow-lg rounded-xl">
        <h2 className="text-2xl font-bold mb-4 text-blue-700">
          {generatedQuestions[active].q}
        </h2>

        <textarea
          value={answers[active]}
          onChange={(e) => handleAnswer(e.target.value)}
          className="w-full min-h-40 border p-4 rounded-xl"
          placeholder="Enter your answer"
        />

        {/* Feedback */}
        {showAnswer && evaluations[active].length > 0 && (
          <div className="bg-blue-50 p-4 rounded-xl mt-4 border">
            <h3 className="font-semibold mb-2">Feedback:</h3>

            <ul className="list-disc pl-6">
              {evaluations[active].map((item, i) => (
                <li key={i}>{item.a}</li>
              ))}
            </ul>
          </div>
        )}

        <div className="flex justify-end mt-6">
          <button
            onClick={handleNext}
            className="px-6 py-3 bg-blue-600 text-white rounded-xl"
          >
            {showAnswer ? 'Next →' : 'Show Evaluation'}
          </button>
        </div>
      </div>
    </div>
  );
}
