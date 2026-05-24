export interface LogEntry {
  timestamp: string;
  level: string;
  service: string;
  function_name: string;
  message: string;
  [key: string]: unknown;
}

const SERVICE = "serverless-aws";
const FUNCTION_NAME = process.env.AWS_LAMBDA_FUNCTION_NAME ?? "local";

function emit(level: string, message: string, extra: Record<string, unknown> = {}): void {
  const entry: LogEntry = {
    timestamp: new Date().toISOString(),
    level,
    service: SERVICE,
    function_name: FUNCTION_NAME,
    message,
    ...extra,
  };
  // Lambda captures stdout → CloudWatch Logs → Datadog log forwarder picks it up
  console.log(JSON.stringify(entry));
}

export const logger = {
  info:  (msg: string, extra?: Record<string, unknown>) => emit("INFO",  msg, extra),
  warn:  (msg: string, extra?: Record<string, unknown>) => emit("WARN",  msg, extra),
  error: (msg: string, extra?: Record<string, unknown>) => emit("ERROR", msg, extra),
};
