import { createRoot } from "react-dom/client";
import { LeadFunnelChart } from "./LeadFunnelChart";
import type { LeadFunnelProps } from "@shared/types";

const el = document.getElementById("lead-funnel-root");
if (el) {
  const props = JSON.parse(el.dataset["props"] ?? "{}") as LeadFunnelProps;
  createRoot(el).render(<LeadFunnelChart {...props} />);
}
