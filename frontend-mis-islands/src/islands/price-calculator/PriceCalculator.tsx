import { useState } from "react";
import { api } from "@shared/api";
import type { PriceCalculatorProps, ValuationRequest, ValuationResponse } from "@shared/types";

const CANTONS = [
  "AG","AI","AR","BE","BL","BS","FR","GE","GL","GR",
  "JU","LU","NE","NW","OW","SG","SH","SO","SZ","TG",
  "TI","UR","VD","VS","ZG","ZH",
];

const PROPERTY_TYPES = [
  { value: "apartment", label: "Apartment" },
  { value: "house", label: "House" },
  { value: "commercial", label: "Commercial" },
  { value: "land", label: "Land" },
  { value: "parking", label: "Parking" },
];

const OFFER_TYPES = [
  { value: "sale", label: "Sale" },
  { value: "rent", label: "Rent" },
];

type Status = "idle" | "loading" | "success" | "error";

export function PriceCalculator({ canton: defaultCanton }: PriceCalculatorProps) {
  const [form, setForm] = useState<ValuationRequest>({
    canton: defaultCanton || "ZH",
    property_type: "apartment",
    offer_type: "sale",
    area_m2: 80,
    rooms: 3.5,
  });
  const [result, setResult] = useState<ValuationResponse | null>(null);
  const [status, setStatus] = useState<Status>("idle");
  const [error, setError] = useState("");

  const set = (field: keyof ValuationRequest, value: string | number) =>
    setForm((f) => ({ ...f, [field]: value }));

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setStatus("loading");
    setError("");
    try {
      const res = await api.post<ValuationResponse>("/valuations/estimate/", form);
      setResult(res);
      setStatus("success");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
      setStatus("error");
    }
  }

  function fmt(chf: string) {
    return `CHF ${Number(chf).toLocaleString("de-CH", { maximumFractionDigits: 0 })}`;
  }

  const rangeWidth =
    result
      ? Math.round(
          ((Number(result.estimate_chf) - Number(result.range_low_chf)) /
            (Number(result.range_high_chf) - Number(result.range_low_chf))) *
            100
        )
      : 50;

  return (
    <div>
      <form onSubmit={handleSubmit} className="row g-2">
        <div className="col-md-2">
          <label className="form-label small">Canton</label>
          <select
            className="form-select form-select-sm"
            value={form.canton}
            onChange={(e) => set("canton", e.target.value)}
          >
            {CANTONS.map((c) => <option key={c}>{c}</option>)}
          </select>
        </div>

        <div className="col-md-2">
          <label className="form-label small">Property type</label>
          <select
            className="form-select form-select-sm"
            value={form.property_type}
            onChange={(e) => set("property_type", e.target.value)}
          >
            {PROPERTY_TYPES.map((t) => (
              <option key={t.value} value={t.value}>{t.label}</option>
            ))}
          </select>
        </div>

        <div className="col-md-2">
          <label className="form-label small">Offer type</label>
          <select
            className="form-select form-select-sm"
            value={form.offer_type}
            onChange={(e) => set("offer_type", e.target.value)}
          >
            {OFFER_TYPES.map((t) => (
              <option key={t.value} value={t.value}>{t.label}</option>
            ))}
          </select>
        </div>

        <div className="col-md-2">
          <label className="form-label small">Area (m²)</label>
          <input
            type="number"
            className="form-control form-control-sm"
            value={form.area_m2}
            min={5}
            max={2000}
            onChange={(e) => set("area_m2", Number(e.target.value))}
          />
        </div>

        <div className="col-md-2">
          <label className="form-label small">Rooms</label>
          <input
            type="number"
            className="form-control form-control-sm"
            value={form.rooms ?? ""}
            min={0.5}
            max={20}
            step={0.5}
            onChange={(e) => set("rooms", Number(e.target.value))}
          />
        </div>

        <div className="col-md-2 d-flex align-items-end">
          <button
            type="submit"
            className="btn btn-primary btn-sm w-100"
            disabled={status === "loading"}
          >
            {status === "loading" ? "…" : "Estimate"}
          </button>
        </div>
      </form>

      {status === "error" && (
        <div className="alert alert-danger mt-3 py-2 small">{error}</div>
      )}

      {result && status === "success" && (
        <div className="mt-3">
          <div className="text-center mb-2">
            <span className="fs-4 fw-bold text-primary">{fmt(result.estimate_chf)}</span>
            <span className="text-muted small ms-2">estimated value</span>
          </div>

          <div className="d-flex justify-content-between small text-muted mb-1">
            <span>{fmt(result.range_low_chf)}</span>
            <span>±15% confidence band</span>
            <span>{fmt(result.range_high_chf)}</span>
          </div>

          <div className="progress" style={{ height: "8px" }}>
            <div
              className="progress-bar bg-primary"
              style={{ width: `${rangeWidth}%` }}
              role="progressbar"
            />
          </div>

          <div className="mt-2 small text-muted text-center">
            {result.area_m2} m² · {result.property_type} · {result.offer_type} · {result.canton}
          </div>
        </div>
      )}
    </div>
  );
}
