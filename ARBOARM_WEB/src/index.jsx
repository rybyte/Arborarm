import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { ElementX } from "./screens/ElementX";

createRoot(document.getElementById("app")).render(
  <StrictMode>
    
    <ElementX />
  </StrictMode>,
);
