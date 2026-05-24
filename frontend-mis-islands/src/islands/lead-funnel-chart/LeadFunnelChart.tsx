import { useEffect, useState } from "react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Cell,
} from "recharts";
import { api } from "@shared/api";
import type { Lead, LeadFunnelProps, PaginatedResponse } from "@shared/types";

const FUNNEL_STAGES = [
  { status: "new",               label: "New",               color: "#6c757d" },
  { status: "contacted",         label: "Contacted",         color: "#0d6efd" },
  { status: "qualified",         label: "Qualified",         color: "#0dcaf0" },
  { status: "viewing_scheduled", label: "Viewing scheduled", color: "#ffc107" },
  { status: "offer_made",        label: "Offer made",        color: "#fd7e14" },
  { status: "closed_won",        label: "Won",               color: "#198754" },
  { status: "closed_lost",       label: "Lost",              color: "#dc3545" },
] as const;

interface ChartDatum {
  label: string;
  count: number;
  color: string;
}

export function LeadFunnelChart({ agencyId }: LeadFunnelProps) {
  const [data, setData] = useState<ChartDatum[]>([]);
  const [total, setTotal] = useState(0);
  const [avgScore, setAvgScore] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function load() {
      try {
        // Fetch up to 200 leads — enough for a meaningful funnel without pagination
        const res = await api.get<PaginatedResponse<Lead>>(
          `/leads/?agency_id=${agencyId}&page_size=200`
        );
        if (cancelled) return;

        const counts = new Map<string, number>();
        let scoreSum = 0;
        let scoreCount = 0;

        for (const lead of res.results) {
          counts.set(lead.status, (counts.get(lead.status) ?? 0) + 1);
          if (lead.score !== null) {
            scoreSum += lead.score;
            scoreCount++;
          }
        }

        setData(
          FUNNEL_STAGES.map((s) => ({
            label: s.label,
            count: counts.get(s.status) ?? 0,
            color: s.color,
          }))
        );
        setTotal(res.count);
        setAvgScore(scoreCount > 0 ? Math.round(scoreSum / scoreCount) : null);
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Failed to load leads");
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    load();
    return () => { cancelled = true; };
  }, [agencyId]);

  if (loading) return <p className="text-muted small">Loading lead data…</p>;
  if (error) return <div className="alert alert-danger py-2 small">{error}</div>;

  const conversionRate =
    total > 0
      ? Math.round(((data.find((d) => d.label === "Won")?.count ?? 0) / total) * 100)
      : 0;

  return (
    <div>
      <div className="d-flex gap-4 mb-3">
        <div className="text-center">
          <div className="fs-5 fw-bold">{total}</div>
          <div className="small text-muted">Total leads</div>
        </div>
        <div className="text-center">
          <div className="fs-5 fw-bold text-success">{conversionRate}%</div>
          <div className="small text-muted">Conversion rate</div>
        </div>
        {avgScore !== null && (
          <div className="text-center">
            <div className="fs-5 fw-bold text-primary">{avgScore}</div>
            <div className="small text-muted">Avg. score</div>
          </div>
        )}
      </div>

      <ResponsiveContainer width="100%" height={200}>
        <BarChart data={data} layout="vertical" margin={{ left: 110, right: 20, top: 4, bottom: 4 }}>
          <CartesianGrid strokeDasharray="3 3" horizontal={false} />
          <XAxis type="number" tick={{ fontSize: 11 }} />
          <YAxis
            type="category"
            dataKey="label"
            tick={{ fontSize: 12 }}
            width={105}
          />
          <Tooltip
            formatter={(value: number) => [value, "leads"]}
            contentStyle={{ fontSize: 12 }}
          />
          <Bar dataKey="count" radius={[0, 3, 3, 0]}>
            {data.map((entry, i) => (
              <Cell key={i} fill={entry.color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
