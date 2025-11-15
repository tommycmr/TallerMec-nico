import React from "react";
import "./App.css";
import ClientesList from "./components/clientes/ClientesList";

function App() {
  React.useEffect(() => {
    // Esto es solo para testear
    console.log("API URL:", process.env.REACT_APP_API_URL);
  }, []);

  return (
    <div className="App">
      <h1>Taller Mecánico</h1>
      <ClientesList />
    </div>
  );
}

export default App;
