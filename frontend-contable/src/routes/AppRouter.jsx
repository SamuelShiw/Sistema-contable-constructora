import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom"

import DashboardPage from "../pages/DashboardPage"

function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={<DashboardPage />}
        />
      </Routes>
    </BrowserRouter>
  )
}

export default AppRouter