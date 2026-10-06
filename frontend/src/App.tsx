import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Queue from "./pages/Queue";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/queue/:roomCode" element={<Queue />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
