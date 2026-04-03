import client from './client'

export interface Schedule {
  id: string
  name: string
  case_id: string
  target_app_id: string
  cron_expr: string
  enabled: boolean
  concurrency: number
  delay_ms: number
  environment?: string
  override_host?: string
  perf_threshold_ms?: number
  ignore_fields?: string[]
  webhook_url?: string
  notify_type?: string
  last_run_at?: string
  last_job_id?: string
  created_at: string
  updated_at: string
}

export const scheduleApi = {
  list: () => client.get<Schedule[]>('/schedules'),
  get: (id: string) => client.get<Schedule>(`/schedules/${id}`),
  create: (data: Omit<Schedule, 'id' | 'created_at' | 'updated_at' | 'last_run_at' | 'last_job_id'>) =>
    client.post<Schedule>('/schedules', data),
  update: (id: string, data: Partial<Schedule>) => client.put<Schedule>(`/schedules/${id}`, data),
  delete: (id: string) => client.delete(`/schedules/${id}`),
  batchDelete: (ids: string[]) => client.delete('/schedules/batch', { data: { ids } }),
  runNow: (id: string) => client.post<{ triggered: boolean }>(`/schedules/${id}/run-now`),
}
