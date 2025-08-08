import './App.css'
import { Route, Routes, BrowserRouter as Router } from 'react-router-dom'
import { Home } from './pages/Home'

function App() {
  return (
    <div className="w-full">
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
      </Router>
    </div>
  )
}

export default App
