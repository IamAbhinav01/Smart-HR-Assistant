import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/home';
import Analysis from './pages/Analysis';
import Questions from './pages/questions';
export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/analysis" element={<Analysis />} />
        <Route path="/questions" element={<Questions />} />
      </Routes>
    </Router>
  );
}
