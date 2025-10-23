import { useState, useRef } from 'react';

export default function App() {
  const [fileName, setFileName] = useState('');
  const [jobInput, setJobInput] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const fileInputRef = useRef(null);

  const jobRoles = [
    'Software Engineer',
    'Data Scientist',
    'AI Engineer',
    'Frontend Developer',
    'Backend Developer',
    'ML Researcher',
  ];

  // Handle file upload click
  const handleClick = () => {
    fileInputRef.current.click();
  };

  // Handle file select
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) setFileName(`✅ Uploaded: ${file.name}`);
    else setFileName('');
  };

  // Handle drag & drop
  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) setFileName(`✅ Uploaded: ${file.name}`);
  };

  // Handle job role suggestions
  const handleJobInput = (e) => {
    const value = e.target.value.toLowerCase();
    setJobInput(e.target.value);
    if (!value) {
      setSuggestions([]);
      return;
    }
    const matches = jobRoles.filter((role) =>
      role.toLowerCase().includes(value)
    );
    setSuggestions(matches);
  };

  const handleSuggestionClick = (role) => {
    setJobInput(role);
    setSuggestions([]);
  };

  return (
    <div className="bg-white min-h-screen flex flex-col">
      {/* Header */}
      <header className="p-6">
        <a className="font-bold text-xl sm:text-2xl md:text-[25px]" href="/">
          Smart HR<span className="text-[#335DC8]"> Assistant</span>
        </a>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-8 py-10 flex flex-col lg:flex-row items-start gap-10">
        {/* Left Side */}
        <div className="w-full lg:w-1/2">
          <h1 className="text-4xl mt-3.5 font-bold tracking-tight sm:text-6xl text-black leading-tight">
            Personalised Resume Analyzer
          </h1>
          <p className="text-base md:text-lg text-gray-600 mt-4 mb-6">
            The Smart HR Assistant uses advanced AI to evaluate your resume,
            highlight strengths, and provide actionable feedback tailored to
            your target role.
          </p>
          <ul className="space-y-3 text-gray-700 text-base">
            <li>✅ ATS-friendly optimization suggestions</li>
            <li>📊 Keyword & skills match analysis</li>
            <li>🧠 Personalized career recommendations</li>
            <li>🚀 Designed to help you stand out to recruiters</li>
          </ul>
        </div>

        {/* Right Side */}
        <div className="shadow-md rounded-md w-full lg:w-1/2 p-6 lg:p-8 border border-gray-100">
          <h2 className="text-[20px] font-bold mb-4">Start Your Analysis</h2>

          <div className="mb-6 relative">
            <label
              htmlFor="job-role"
              className="block text-gray-700 text-base font-semibold mb-2"
            >
              What kind of job role are you looking for?
            </label>
            <input
              type="text"
              id="job-role"
              value={jobInput}
              onChange={handleJobInput}
              placeholder="e.g. Data Analyst, Frontend Developer, Marketing Manager..."
              className="w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-[#335DC8]"
            />
            <ul className="absolute max-w-[250px] bg-white border border-gray-300 p-1 list-none">
              {suggestions.map((role) => (
                <li
                  key={role}
                  className="cursor-pointer hover:bg-gray-100 px-2 py-1"
                  onClick={() => handleSuggestionClick(role)}
                >
                  {role}
                </li>
              ))}
            </ul>
          </div>

          <h3 className="text-lg font-semibold mb-2">Upload your Resume</h3>
          <p className="text-gray-600 mb-4 text-sm">
            Submit your latest resume in PDF format for an instant analysis.
          </p>

          <div
            className="border-2 border-dashed rounded-lg px-4 py-8 flex flex-col text-center items-center justify-center gap-3 cursor-pointer border-[#518EF8] hover:bg-[#f7faff] transition"
            onClick={handleClick}
            onDrop={handleDrop}
            onDragOver={(e) => e.preventDefault()}
          >
            <p className="text-[#313136] text-lg md:text-xl font-normal">
              Drag and Drop your resume here
            </p>
            <span className="font-normal text-sm md:text-base text-[#31313680]">
              or click browse (PDF only)
            </span>
            <input
              type="file"
              className="hidden"
              ref={fileInputRef}
              accept=".pdf,application/pdf"
              onChange={handleFileChange}
            />
            <span>{fileName}</span>
          </div>

          <div className="mt-8 flex flex-col items-center">
            <button className="bg-[#335DC8] text-white px-6 py-3 rounded-lg text-lg font-semibold hover:bg-[#2748a2] transition-all w-full md:w-auto">
              Start Analysis
            </button>
            <p className="text-sm text-gray-500 mt-3 text-center">
              🔒 Your data is private and never stored. Maximum file size: 5 MB.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
