import { useEffect, useState, useCallback } from "react";
import { api } from "@shared/api";
import type { Listing, ListingBulkEditorProps, PaginatedResponse } from "@shared/types";

const STATUS_BADGE: Record<string, string> = {
  draft: "secondary",
  published: "success",
  reserved: "warning",
  sold: "dark",
  archived: "light",
};

type BulkAction = "publish" | "archive";

export function ListingBulkEditor({ agencyId }: ListingBulkEditorProps) {
  const [listings, setListings] = useState<Listing[]>([]);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [actionLoading, setActionLoading] = useState<BulkAction | null>(null);
  const [toast, setToast] = useState("");

  const load = useCallback(async () => {
    try {
      setLoading(true);
      const res = await api.get<PaginatedResponse<Listing>>(
        `/listings/?agency_id=${agencyId}&page_size=50`
      );
      setListings(res.results);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load listings");
    } finally {
      setLoading(false);
    }
  }, [agencyId]);

  useEffect(() => { load(); }, [load]);

  function toggleAll() {
    if (selected.size === listings.length) {
      setSelected(new Set());
    } else {
      setSelected(new Set(listings.map((l) => l.id)));
    }
  }

  function toggle(id: string) {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }

  async function runBulkAction(action: BulkAction) {
    if (selected.size === 0) return;
    setActionLoading(action);
    const ids = [...selected];
    let ok = 0;
    let fail = 0;

    await Promise.allSettled(
      ids.map(async (id) => {
        try {
          await api.post(`/listings/${id}/${action}/`, {});
          ok++;
        } catch {
          fail++;
        }
      })
    );

    setToast(`${action}: ${ok} updated${fail > 0 ? `, ${fail} failed` : ""}`);
    setTimeout(() => setToast(""), 3000);
    setSelected(new Set());
    setActionLoading(null);
    await load();
  }

  if (loading) return <p className="text-muted small">Loading listings…</p>;
  if (error) return <div className="alert alert-danger py-2 small">{error}</div>;

  const allChecked = selected.size === listings.length && listings.length > 0;
  const someChecked = selected.size > 0 && selected.size < listings.length;

  return (
    <div>
      {toast && (
        <div className="alert alert-success py-2 small mb-2">{toast}</div>
      )}

      <div className="d-flex gap-2 mb-2 align-items-center">
        <span className="small text-muted">{selected.size} selected</span>
        <button
          className="btn btn-sm btn-outline-success"
          disabled={selected.size === 0 || actionLoading !== null}
          onClick={() => runBulkAction("publish")}
        >
          {actionLoading === "publish" ? "Publishing…" : "Publish"}
        </button>
        <button
          className="btn btn-sm btn-outline-secondary"
          disabled={selected.size === 0 || actionLoading !== null}
          onClick={() => runBulkAction("archive")}
        >
          {actionLoading === "archive" ? "Archiving…" : "Archive"}
        </button>
        <button className="btn btn-sm btn-link ms-auto" onClick={load}>
          Refresh
        </button>
      </div>

      <div className="table-responsive" style={{ maxHeight: "360px", overflowY: "auto" }}>
        <table className="table table-sm table-hover mb-0">
          <thead className="table-light sticky-top">
            <tr>
              <th style={{ width: 32 }}>
                <input
                  type="checkbox"
                  className="form-check-input"
                  checked={allChecked}
                  ref={(el) => { if (el) el.indeterminate = someChecked; }}
                  onChange={toggleAll}
                />
              </th>
              <th>Title</th>
              <th>Type</th>
              <th>Price</th>
              <th>Status</th>
              <th>Views</th>
            </tr>
          </thead>
          <tbody>
            {listings.map((l) => (
              <tr
                key={l.id}
                className={selected.has(l.id) ? "table-active" : ""}
                style={{ cursor: "pointer" }}
                onClick={() => toggle(l.id)}
              >
                <td onClick={(e) => e.stopPropagation()}>
                  <input
                    type="checkbox"
                    className="form-check-input"
                    checked={selected.has(l.id)}
                    onChange={() => toggle(l.id)}
                  />
                </td>
                <td className="text-truncate" style={{ maxWidth: 220 }} title={l.title}>
                  {l.title}
                </td>
                <td>
                  <span className="badge bg-light text-dark border">{l.property_type}</span>
                </td>
                <td className="text-nowrap">{l.price_display}</td>
                <td>
                  <span className={`badge bg-${STATUS_BADGE[l.status] ?? "secondary"}`}>
                    {l.status}
                  </span>
                </td>
                <td>{l.view_count}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
