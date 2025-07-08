import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import TaskCreationPage from "./pages/TaskCreationPage";
import ApproverActionPage from "./pages/ApproverActionPage";
import CompletedTasksPage from "./pages/CompletedTasksPage"; // ✅ New page

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <nav className="bg-white shadow py-4 mb-6">
          <div className="container mx-auto flex justify-center space-x-6">
            <Link to="/" className="text-blue-600 font-semibold hover:underline">
              Task Creation
            </Link>
            <Link to="/approver" className="text-blue-600 font-semibold hover:underline">
              Approver Action
            </Link>
            <Link to="/completed" className="text-blue-600 font-semibold hover:underline">
              Completed Tasks
            </Link>
          </div>
        </nav>

        <main className="container mx-auto px-4">
          <Routes>
            <Route path="/" element={<TaskCreationPage />} />
            <Route path="/approver" element={<ApproverActionPage />} />
            <Route path="/completed" element={<CompletedTasksPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
