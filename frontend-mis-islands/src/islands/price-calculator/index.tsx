import { createRoot } from "react-dom/client";
import { PriceCalculator } from "./PriceCalculator";
import type { PriceCalculatorProps } from "@shared/types";

const el = document.getElementById("price-calculator-root");
if (el) {
  const props = JSON.parse(el.dataset["props"] ?? "{}") as PriceCalculatorProps;
  createRoot(el).render(<PriceCalculator {...props} />);
}
