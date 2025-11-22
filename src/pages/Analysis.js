import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';

export default function Analysis() {
  const [progress, setProgress] = useState(0);
  const location = useLocation();
  const { file, jobDescription } = location.state || {};
  console.log('jD:', jobDescription);
  console.log('jD:', jobDescription);
  // Example dynamic backend-like data
  const scoreData = {
    total: 30,
    breakdown: {
      Content: 80,
      Structure: 60,
      ATS: 30,
      Tailoring: 50,
    },
  };

  const reasons = [
    'Your experience aligns strongly with the core job responsibilities.',
    'You have relevant technical skills that match the role requirements.',
    'Your accomplishments demonstrate measurable impact.',
  ];

  // Smooth meter animation
  useEffect(() => {
    let current = 0;
    const target = scoreData.total;
    const timer = setInterval(() => {
      current += 1;
      if (current <= target) setProgress(current);
      else clearInterval(timer);
    }, 15);

    return () => clearInterval(timer);
  }, []);

  const radius = 40;
  const circumference = 2 * Math.PI * radius;
  const filled = (progress / 100) * circumference;

  const getColor = (value) =>
    value >= 80
      ? 'text-green-600'
      : value >= 50
      ? 'text-amber-500'
      : 'text-red-600';

  return (
    <div className="flex gap-10 p-10 bg-[#F5F7FC] min-h-screen">
      {/* LEFT SCORE CARD */}
      <div className="w-80 bg-white rounded-3xl p-8 shadow-md border border-gray-200">
        <h2 className="text-2xl font-bold text-gray-800 mb-6 tracking-tight">
          ATS Score Overview
        </h2>

        {/* SCORE METER */}
        <div className="flex justify-center mb-4">
          <svg width="160" height="100" viewBox="0 0 160 100">
            {/* Base Arc */}
            <path
              d="M 20 100 A 60 60 0 0 1 140 100"
              fill="none"
              stroke="#E5E7EB"
              strokeWidth="12"
              strokeLinecap="round"
            />

            {/* Filled Arc */}
            <path
              d="M 20 100 A 60 60 0 0 1 140 100"
              fill="none"
              stroke="#6366F1"
              strokeWidth="12"
              strokeLinecap="round"
              strokeDasharray="188"
              strokeDashoffset={188 - (188 * progress) / 100}
              style={{ transition: 'stroke-dashoffset 0.5s ease-out' }}
            />

            {/* Score Text */}
            <text
              x="80"
              y="90"
              textAnchor="middle"
              className="text-xl font-bold fill-gray-900"
            >
              {progress}%
            </text>
          </svg>
        </div>

        <p className="text-center text-sm text-gray-600 mb-4">
          This score reflects how well your resume matches the job description.
        </p>

        <hr className="my-6" />

        {/* BREAKDOWN SECTION */}
        <div className="space-y-5">
          {Object.entries(scoreData.breakdown).map(([title, value]) => (
            <div key={title}>
              <div className="flex justify-between text-sm font-semibold text-gray-700">
                <span>{title}</span>
                <span className={getColor(value)}>{value}%</span>
              </div>

              {/* Progress Bar */}
              <div className="h-2 w-full bg-gray-200 rounded-full mt-1">
                <div
                  className={`h-2 rounded-full transition-all duration-500 ${
                    value >= 80
                      ? 'bg-green-500'
                      : value >= 50
                      ? 'bg-amber-500'
                      : 'bg-red-500'
                  }`}
                  style={{ width: `${value}%` }}
                />
              </div>
            </div>
          ))}
        </div>

        <hr className="my-6" />
      </div>
      {/* RIGHT SIDE MESSAGE + REASONS */}
      <div className="flex-1">
        {/* Message */}
        <div
          className={`text-xl font-semibold mb-4 ${
            progress >= 70 ? 'text-green-600' : 'text-red-600'
          }`}
        >
          {progress >= 70
            ? 'Great news! Your CV is a strong match for this job because:'
            : 'Your CV needs improvement to better match the job description:'}
        </div>

        {/* Reasons */}
        <ul className="list-disc ml-6 space-y-3">
          {reasons.length > 0 ? (
            reasons.map((reason, index) => (
              <li
                key={index}
                className="text-gray-700 text-[15px] leading-relaxed flex items-start gap-2"
              >
                <span className="text-indigo-600 font-bold">
                  {progress < 70 ? '❌' : '✔'}
                </span>

                <span>{reason}</span>
              </li>
            ))
          ) : (
            <li className="text-gray-500 italic">Generating insights...</li>
          )}
        </ul>

        {/* ⭐ SKILL TEST BOX — now correctly under REASONS */}
        <div className="mt-8 w-full max-w-xl bg-white border border-gray-200 rounded-2xl p-6 shadow-md">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">
            Would you like to take a quick skill test to evaluate your knowledge
            for this job description?
          </h3>

          <div className="flex gap-4 mt-4">
            {/* YES BUTTON */}
            <button
              className="
          flex-1 px-6 py-3 bg-indigo-600 text-white rounded-xl 
          text-base font-semibold shadow-md hover:bg-indigo-700 
          hover:scale-[1.02] transition duration-300
        "
            >
              Yes, Start Test
            </button>

            {/* NO BUTTON */}
            <button
              className="
          flex-1 px-6 py-3 bg-gray-200 text-gray-800 rounded-xl 
          text-base font-semibold shadow-md hover:bg-gray-300 
          hover:scale-[1.02] transition duration-300
        "
            >
              Maybe Later
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
