<template>
  <n-card title="回放历史">
    <template #header-extra>
      <n-space align="center">
        <n-input
          v-model:value="filterKeyword"
          placeholder="搜索用例名称"
          clearable
          style="width: 160px"
          @update:value="onFilterChange"
          @clear="onFilterChange"
        />
        <n-select
          v-model:value="filterCaseId"
          :options="caseOptions"
          placeholder="按用例筛选"
          clearable
          filterable
          style="width: 160px"
          @update:value="onFilterChange"
        />
        <n-select
          v-model:value="filterAppId"
          :options="appOptions"
          placeholder="按应用筛选"
          clearable
          style="width: 160px"
          @update:value="onFilterChange"
        />
        <n-select
          v-model:value="filterStatus"
          :options="statusOptions"
          placeholder="按状态筛选"
          clearable
          style="width: 130px"
          @update:value="onFilterChange"
        />
        <n-button size="small" @click="loadJobs">刷新</n-button>
      </n-space>
    </template>
    <n-space align="center" style="margin-bottom:10px">
      <span style="color:#999;font-size:13px">共 {{ jobTotal }} 条</span>
    </n-space>
    <n-data-table
      :columns="jobColumns"
      :data="jobs"
      :loading="jobsLoading"
      :pagination="jobPagination"
      :scroll-x="900"
      :row-key="(r: any) => r.id"
      :checked-row-keys="selectedIds"
      @update:checked-row-keys="selectedIds = $event as string[]"
    />
    <n-space v-if="selectedIds.length > 0" align="center" style="margin-top:10px">
      <span>已选 {{ selectedIds.length }} 条</span>
      <n-button size="small" type="error" :loading="batchDeleting" @click="deleteSelected">批量删除</n-button>
    </n-space>
  </n-card>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, h } from 'vue'
import { useRouter } from 'vue-router'
import {
  NCard, NSpace, NDataTable, NTag, NButton, NInput, NSelect, NPopconfirm, useMessage, useDialog,
} from 'naive-ui'
import { replayApi, type ReplayJob } from '@/api/replays'
import { fmtTime } from '@/utils/time'
import { testCaseApi } from '@/api/testCases'
import { applicationApi } from '@/api/applications'

const router = useRouter()
const message = useMessage()
const dialog = useDialog()

const caseOptions = ref<{ label: string; value: string }[]>([])
const appOptions = ref<{ label: string; value: string }[]>([])
const caseMap = ref<Record<string, string>>({})
const appMap = ref<Record<string, string>>({})
const jobs = ref<ReplayJob[]>([])
const jobsLoading = ref(false)
const jobTotal = ref(0)
const selectedIds = ref<string[]>([])
const batchDeleting = ref(false)

// 回放历史筛选
const filterKeyword = ref('')
const filterCaseId = ref<string | null>(null)
const filterAppId = ref<string | null>(null)
const filterStatus = ref<string | null>(null)
const statusOptions = [
  { label: '已完成', value: 'DONE' },
  { label: '运行中', value: 'RUNNING' },
  { label: '失败', value: 'FAILED' },
  { label: '待处理', value: 'PENDING' },
  { label: '已取消', value: 'CANCELLED' },
]

const jobPagination = reactive({
  page: 1,
  pageSize: 10,
  showSizePicker: true,
  pageSizes: [10, 20, 50],
  itemCount: 0,
  onChange: (page: number) => {
    jobPagination.page = page
    loadJobs()
  },
  onUpdatePageSize: (size: number) => {
    jobPagination.pageSize = size
    jobPagination.page = 1
    loadJobs()
  },
})

const statusColor: Record<string, any> = {
  DONE: 'success', RUNNING: 'info', PENDING: 'default', FAILED: 'error', CANCELLED: 'warning',
}

const statusLabel: Record<string, string> = {
  DONE: '已完成', RUNNING: '运行中', PENDING: '待处理', FAILED: '失败', CANCELLED: '已取消',
}

const jobColumns = [
  { type: 'selection' as const, width: 40 },
  {
    title: '用例',
    key: 'case_id',
    render: (r: ReplayJob) => caseMap.value[r.case_id] || r.case_id.slice(0, 8),
  },
  {
    title: '目标应用',
    key: 'target_app_id',
    width: 150,
    render: (r: ReplayJob) => appMap.value[r.target_app_id] || r.target_app_id.slice(0, 8),
    ellipsis: { tooltip: true },
  },
  {
    title: '状态',
    key: 'status',
    render: (r: ReplayJob) =>
      h(NTag, { size: 'small', type: statusColor[r.status] || 'default' }, () => statusLabel[r.status] || r.status),
  },
  {
    title: '通过率',
    key: 'progress',
    width: 160,
    render: (r: ReplayJob) => {
      const sent = r.sent_count ?? 0
      const pass = r.success_count ?? 0
      const fail = r.fail_count ?? 0
      if (!sent) return h('span', { style: 'color:#999' }, '-')
      const pct = Math.round(pass / sent * 100)
      const color = pct >= 90 ? '#18a058' : pct >= 60 ? '#f0a020' : '#d03050'
      return h('span', { style: `color:${color};font-weight:bold` },
        `${pass}/${sent} (${pct}%) 失败:${fail}`)
    },
  },
  { title: '环境', key: 'environment', render: (r: ReplayJob) => r.environment || '-' },
  {
    title: 'Mock',
    key: 'mock',
    width: 70,
    render: (r: ReplayJob) =>
      r.use_sub_invocation_mocks
        ? h(NTag, { size: 'small', type: 'warning' }, () => 'Mock')
        : h('span', { style: 'color:#ccc' }, '-'),
  },
  { title: '创建时间', key: 'created_at', render: (r: ReplayJob) => fmtTime(r.created_at) },
  {
    title: '操作',
    key: 'actions',
    width: 160,
    render: (r: ReplayJob) =>
      h(NSpace, { size: 'small' }, () => [
        h(NButton, {
          size: 'small',
          onClick: () => router.push(`/results/${r.id}`),
        }, () => '查看结果'),
        h(NPopconfirm, { onPositiveClick: () => deleteJob(r.id) }, {
          trigger: () => h(NButton, { size: 'small', type: 'error' }, () => '删除'),
          default: () => '确认删除该回放记录？',
        }),
      ]),
  },
]

// 当筛选条件变化时重置到第一页再加载
function onFilterChange() {
  jobPagination.page = 1
  selectedIds.value = []
  loadJobs()
}

async function loadJobs() {
  jobsLoading.value = true
  try {
    // case_id: 若有关键字则不传 case_id（本地过滤），否则精确传
    const res = await replayApi.list({
      case_id: (!filterKeyword.value && filterCaseId.value) ? filterCaseId.value : undefined,
      app_id: filterAppId.value || undefined,
      status: filterStatus.value || undefined,
      limit: filterKeyword.value ? 200 : jobPagination.pageSize,
      offset: filterKeyword.value ? 0 : (jobPagination.page - 1) * jobPagination.pageSize,
    })
    // 关键字在客户端过滤（匹配用例名称）
    if (filterKeyword.value) {
      const kw = filterKeyword.value.toLowerCase()
      jobs.value = res.data.items.filter(j => {
        const caseName = (caseMap.value[j.case_id] || j.case_id).toLowerCase()
        return caseName.includes(kw)
      })
      jobTotal.value = jobs.value.length
    } else {
      jobs.value = res.data.items
      jobTotal.value = res.data.total
    }
    jobPagination.itemCount = jobTotal.value
  } finally {
    jobsLoading.value = false
  }
}

async function deleteJob(id: string) {
  await replayApi.delete(id)
  message.success('已删除')
  jobs.value = jobs.value.filter(j => j.id !== id)
  selectedIds.value = selectedIds.value.filter(i => i !== id)
}

async function deleteSelected() {
  dialog.warning({
    title: '确认批量删除',
    content: `将删除选中的 ${selectedIds.value.length} 条回放记录，确认吗？`,
    positiveText: '删除', negativeText: '取消',
    onPositiveClick: async () => {
      batchDeleting.value = true
      try {
        await replayApi.batchDelete(selectedIds.value)
        message.success(`已删除 ${selectedIds.value.length} 条`)
        jobs.value = jobs.value.filter(j => !selectedIds.value.includes(j.id))
        selectedIds.value = []
        jobTotal.value = jobs.value.length
        jobPagination.itemCount = jobTotal.value
      } finally {
        batchDeleting.value = false
      }
    },
  })
}

onMounted(async () => {
  await Promise.all([
    testCaseApi.list({ limit: 500 }).then(casesRes => {
      caseOptions.value = casesRes.data.items.map(c => ({ label: c.name, value: c.id }))
      caseMap.value = Object.fromEntries(casesRes.data.items.map(c => [c.id, c.name]))
    }).catch(() => {}),
    applicationApi.list().then(appsRes => {
      appOptions.value = appsRes.data.map(a => ({ label: a.name, value: a.id }))
      appMap.value = Object.fromEntries(appsRes.data.map(a => [a.id, a.name]))
    }).catch(() => {}),
    loadJobs(),
  ])
})
</script>
