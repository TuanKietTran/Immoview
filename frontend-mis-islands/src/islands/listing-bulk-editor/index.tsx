import { createRoot } from "react-dom/client";
import { ListingBulkEditor } from "./ListingBulkEditor";
import type { ListingBulkEditorProps } from "@shared/types";

const el = document.getElementById("listing-bulk-editor-root");
if (el) {
  const props = JSON.parse(el.dataset["props"] ?? "{}") as ListingBulkEditorProps;
  createRoot(el).render(<ListingBulkEditor {...props} />);
}
