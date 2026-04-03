import client from './client'

export interface TrendPoint {
  date: string
  total: number
  pass: number
  fail: number
  error: number
  pass_rate: number | null
}

export interface Summary {
  job_count: number
  total_sent: number
  total_pass: number
  total_fail: number
  total_error: number
  avg_pass_rate: number
}

export interface DailyJob {
  id: string
  case_id: string
  target_app_id: string
  status: string
  environment: string | null
  total_count: number
  sent_count: number
  success_count: number
  fail_count: number
  finished_at: string | null
}

export const statsApi = {
  trend: (params?: { app_id?: string; days?: number }) =>
    client.get<TrendPoint[]>('/stats/trend', { params }),
  summary: (params?: { app_id?: string }) =>
    client.get<Summary>('/stats/summary', { params }),
  dailyJobs: (date: string, app_id?: string | null) =>
    client.get<DailyJob[]>('/stats/daily-jobs', { params: { date, app_id: app_id || undefined } }),
}
