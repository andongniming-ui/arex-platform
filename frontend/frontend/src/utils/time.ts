/**
 * Format a UTC datetime string (from backend) to local time.
 * Backend stores datetimes without timezone info, treating them as UTC.
 * Adding 'Z' makes JS parse them as UTC and toLocaleString converts to local.
 */
export function fmtTime(utcStr?: string | null): string {
  if (!utcStr) return ''
  const s = utcStr.includes('T') ? utcStr : utcStr.replace(' ', 'T')
  const d = new Date(s.endsWith('Z') ? s : s + 'Z')
  if (isNaN(d.getTime())) return utcStr
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`
}
