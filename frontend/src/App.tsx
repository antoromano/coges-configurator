import { useState } from "react";

import ConfiguratorFinestre from "./pages/ConfiguratorFinestre";
import ConfiguratorPergole from "./pages/ConfiguratorPergole";
import ConfiguratorPortoncini from "./pages/ConfiguratorPortoncini";
import HomePage from "./pages/HomePage";
import StaffQuoteRequests from "./pages/StaffQuoteRequests";

type View = "home" | "finestre" | "portoncini" | "pergole" | "staff";

export default function App() {
  const [view, setView] = useState<View>("home");

  return (
    <div className="min-h-screen bg-paper">
      {view === "home" && <HomePage onSelect={(slug) => setView(slug as View)} />}
      {view === "finestre" && <ConfiguratorFinestre onBack={() => setView("home")} />}
      {view === "portoncini" && <ConfiguratorPortoncini onBack={() => setView("home")} />}
      {view === "pergole" && <ConfiguratorPergole onBack={() => setView("home")} />}
      {view === "staff" && <StaffQuoteRequests onBack={() => setView("home")} />}
    </div>
  );
}
