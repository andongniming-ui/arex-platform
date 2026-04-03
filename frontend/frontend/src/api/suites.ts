import client from './client'
import type { DiffRule, AssertionRule } from './replays'

export interface SuiteCreate {
  name: string
  description?: string
  case_ids?: string[]
  default_target_app_id?: string
  default_environment?: string
  default_override_host?: string
  default_concurrency?: number
  default_delay_ms?: number
  default_ignore_fields?: string[]
  default_diff_rules?: DiffRule[]
  default_assertions?: AssertionRule[]
  default_perf_threshold_ms?: number
}

export interface Suite extends SuiteCreate {
  id: string
  case_ids: string[]
  default_concurrency: number
  default_delay_ms: number
  created_at: string
  updated_at: string
}

export interface SuiteRunRequest {
  target_app_id: string
  environment?: string
  override_host?: string
  concurrency?: number
  ignore_fields?: string[]
  diff_rules?: DiffRule[]
  assertions?: AssertionRule[]
  perf_threshold_ms?: number
}

export interface SuiteRun {
  id: string
  suite_id: string
  target_app_id: string
  status: string
  total_cases: number
  passed_cases: number
  failed_cases: number
  total_requests: number
  passed_requests: number
  overall_pass_rate: number
  job_ids: string[]
  started_at?: string
  finished_at?: string
  created_at: string
}

export const suiteApi = {
  list: () => client.get<Suite[]>('/suites'),
  get: (id: string) => client.get<Suite>(`/suites/${id}`),
  create: (data: SuiteCreate) => client.post<Suite>('/suites', data),
  update: (id: string, data: Partial<SuiteCreate>) => client.put<Suite>(`/suites/${id}`, data),
  delete: (id: string) => client.delete(`/suites/${id}`),
  run: (id: string, data: SuiteRunRequest) => client.post<SuiteRun>(`/suites/${id}/runs`, data),
  listRuns: (id: string) => client.get<SuiteRun[]>(`/suites/${id}/runs`),
  getRun: (id: string, runId: string) => client.get<SuiteRun>(`/suites/${id}/runs/${runId}`),
}
