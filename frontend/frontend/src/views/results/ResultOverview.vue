<template>
  <n-space vertical :size="16">
    <n-card v-if="summary" :title="`回放结果 — ${fmtTime(job?.created_at)}`">
      <template #header-extra>
        <n-space>
          <n-button size="small" tag="a" :href="replayApi.reportUrl(jobId)" target="_blank">
            导出 HTML 报告
          </n-button>
          <n-button size="small" @click="router.push('/replay-history')">返回回放历史</n-button>
        </n-space>
      </template>
      <n-space :size="24">
        <n-statistic label="总计" :value="summary.total_count" />
        <n-statistic label="通过">
          <template #default>
            <span style="color: #18a058">{{ summary.success_count }}</span>
          </template>
        </n-statistic>
        <n-statistic label="失败">
          <template #default>
            <span style="color: #d03050">{{ summary.fail_count }}</span>
          </template>
        </n-statistic>
        <n-statistic label="错误" v-if="summary.error_count > 0">
          <template #default>
            <span style="color: #f0a020">{{ summary.error_count }}</span>
          </template>
        </n-statistic>
        <n-statistic label="通过率">
          <template #default>
            <span :style="{ color: summary.pass_rate >= 0.9 ? '#18a058' : '#d03050' }">
              {{ (summary.pass_rate * 100).toFixed(1) }}%
            </span>
          </template>
        </n-statistic>
      </n-space>

      <!-- 对比配置：忽略字段 / 智能规则 / 断言 -->
      <div v-if="job && (job.ignore_fields?.length || job.diff_rules?.length || job.assertions?.length)"
           style="margin-top:14px;padding-top:12px;border-top:1px solid #f0f0f0;display:flex;flex-wrap:wrap;gap:16px;align-items:flex-start">
        <div v-if="job.ignore_fields?.length">
          <span style="font-size:12px;color:#999;margin-right:6px">忽略字段：</span>
          <n-tag v-for="f in job.ignore_fields" :key="f" size="small" style="margin-right:4px;font-family:monospace">{{ f }}</n-tag>
        </div>
        <div v-if="job.diff_rules?.length">
          <span style="font-size:12px;color:#999;margin-right:6px">智能规则：</span>
          <n-tag v-for="r in job.diff_rules" :key="r.path" size="small" type="info" style="margin-right:4px;font-family:monospace">
            {{ r.type }}:{{ r.path }}
          </n-tag>
        </div>
        <div v-if="job.assertions?.length">
          <span style="font-size:12px;color:#999;margin-right:6px">断言：</span>
          <n-tag v-for="a in job.assertions" :key="a.path" size="small" type="warning" style="margin-right:4px;font-family:monospace">
            {{ a.path }}
          </n-tag>
        </div>
      </div>
    </n-card>

    <!-- 失败分析面板 -->
    <n-card v-if="analysis" title="失败原因分析">
      <n-grid :cols="5" :x-gap="16" :y-gap="8">
        <n-gi v-for="cat in categoryList" :key="cat.key">
          <n-card 
            size="small" 
            :class="['category-card', filterCategory === cat.key ? 'active' : '']"
            hoverable
            @click="toggleCategory(cat.key)"
            :style="{ cursor: cat.count > 0 ? 'pointer' : 'default', opacity: cat.count > 0 ? 1 : 0.5 }"
          >
            <n-statistic :label="cat.label" :value="cat.count">
              <template #default>
                <span :style="{ color: cat.color, fontWeight: 'bold' }">{{ cat.count }}</span>
              </template>
              <template #suffix>
                <span style="font-size:12px;color:#999">{{ cat.percentage }}%</span>
              </template>
            </n-statistic>
          </n-card>
        </n-gi>
      </n-grid>
      <n-space v-if="filterCategory" style="margin-top: 12px">
        <n-button size="small" @click="filterCategory = null; loadResults()">
          清除筛选: {{ categoryLabels[filterCategory] }}
        </n-button>
      </n-space>
    </n-card>

    <n-card title="逐条结果">
      <n-space style="margin-bottom: 12px">
        <n-select
          v-model:value="filterStatus"
          :options="statusOptions"
          placeholder="状态筛选"
          clearable
          style="width: 150px"
          @update:value="loadResults"
        />
        <n-button @click="loadResults">刷新</n-button>
        <!-- P2-2: 保存为用例 -->
        <n-button type="primary" size="small" @click="showSaveDialog = true" :disabled="!hasFailResults">
          保存失败接口为用例
        </n-button>
      </n-space>

      <n-empty v-if="!loading && results.length === 0" description="暂无结果数据" style="padding:32px 0" />
      <n-data-table v-else :columns="columns" :data="results" :loading="loading" :scroll-x="1100" />

      <n-space justify="end" align="center" style="margin-top:12px">
        <span style="font-size:13px;color:#666">共 {{ resultTotal }} 条</span>
        <n-pagination
          v-model:page="resultPagination.page"
          v-model:page-size="resultPagination.pageSize"
          :page-sizes="resultPagination.pageSizes"
          :item-count="resultTotal"
          show-size-picker
          :show-quick-jumper="true"
          :disabled="loading"
          @update:page="loadResultsPage"
          @update:page-size="(size) => { resultPagination.pageSize = size; resultPagination.page = 1; loadResultsPage() }"
        />
      </n-space>
    </n-card>

    <!-- P2-2: 保存为用例对话框 -->
    <n-modal v-model:show="showSaveDialog" preset="dialog" title="保存失败接口为测试用例" style="width:480px">
      <n-form :model="saveForm" label-placement="left" label-width="100px">
        <n-form-item label="用例名称" required>
          <n-input v-model:value="saveForm.case_name" placeholder="请输入测试用例名称" />
        </n-form-item>
        <n-form-item label="用例描述">
          <n-input v-model:value="saveForm.case_description" type="textarea" placeholder="可选描述" :rows="2" />
        </n-form-item>
        <n-form-item label="选择接口">
          <n-checkbox-group v-model:value="saveForm.recording_ids">
            <n-space vertical>
              <n-checkbox v-for="r in failedResults" :key="r.recording_id" :value="r.recording_id" :label="r.recording_path || r.recording_id.slice(0, 8)" />
            </n-space>
          </n-checkbox-group>
        </n-form-item>
      </n-form>
      <template #action>
        <n-button @click="showSaveDialog = false">取消</n-button>
        <n-button type="primary" :loading="saving" :disabled="!saveForm.case_name || saveForm.recording_ids.length === 0" @click="saveToTestCase">
          保存 ({{ saveForm.recording_ids.length }} 个)
        </n-button>
      </template>
    </n-modal>

    <!-- Diff modal -->
    <n-modal v-model:show="showDiff" preset="card" style="width: 860px" title="响应对比">
      <n-grid :cols="2" :x-gap="16">
        <n-gi>
          <n-card title="原始响应" size="small">
            <pre style="font-size: 12px; overflow: auto; max-height: 400px">{{ formatJson(selectedResult?.original_response) }}</pre>
          </n-card>
        </n-gi>
        <n-gi>
          <n-card title="回放响应" size="small">
            <pre style="font-size: 12px; overflow: auto; max-height: 400px">{{ formatJson(selectedResult?.replayed_response) }}</pre>
          </n-card>
        </n-gi>
      </n-grid>
      <!-- 忽略字段提示 -->
      <div v-if="job?.ignore_fields?.length" style="margin-top:10px;padding:6px 10px;background:#f9f9f9;border-radius:4px;font-size:12px;color:#666;display:flex;flex-wrap:wrap;align-items:center;gap:6px">
        <span style="color:#999">已忽略字段：</span>
        <n-tag v-for="f in job.ignore_fields" :key="f" size="small" style="font-family:monospace">{{ f }}</n-tag>
      </div>
      <n-card title="差异 (deepdiff)" size="small" style="margin-top: 12px" v-if="selectedResult?.diff_json">
        <pre style="font-size: 12px; overflow: auto; max-height: 300px; color: #d03050">{{ formatJson(selectedResult.diff_json) }}</pre>
      </n-card>
      <n-card title="断言结果" size="small" style="margin-top: 12px" v-if="selectedResult?.assertion_results?.length">
        <n-space vertical>
          <n-space
            v-for="(ar, i) in selectedResult.assertion_results"
            :key="i"
            align="center"
            size="small"
          >
            <n-tag :type="ar.passed ? 'success' : 'error'" size="small">
              {{ ar.passed ? '通过' : '失败' }}
            </n-tag>
            <span style="font-size:13px">{{ ar.message }}</span>
          </n-space>
        </n-space>
      </n-card>
    </n-modal>
  </n-space>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, h, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  NCard, NSpace, NStatistic, NDataTable, NSelect, NButton,
  NModal, NGrid, NGi, NTag, NPagination, NEmpty,
  NForm, NFormItem, NCheckbox, NCheckboxGroup, useMessage,
} from 'naive-ui'
import { replayApi, type ReplayJob, type ReplayResult, type ResultSummary, type FailureAnalysis } from '@/api/replays'
import { fmtTime } from '@/utils/time'

const route = useRoute()
const router = useRouter()
const message = useMessage()
const jobId = route.params.jobId as string
const summary = ref<ResultSummary | null>(null)
const job = ref<ReplayJob | null>(null)
const results = ref<ReplayResult[]>([])
const loading = ref(false)
const filterStatus = ref<string | null>(null)
const filterCategory = ref<string | null>(null)
const showDiff = ref(false)
const selectedResult = ref<ReplayResult | null>(null)
const analysis = ref<FailureAnalysis | null>(null)

// P2-2: 保存为用例相关变量
const showSaveDialog = ref(false)
const saving = ref(false)
const saveForm = reactive({
  case_name: '',
  case_description: '',
  recording_ids: [] as string[],
})
const failedResults = computed(() => results.value.filter(r => r.status === 'FAIL' || r.status === 'ERROR'))
const hasFailResults = computed(() => failedResults.value.length > 0)

const categoryLabels: Record<string, string> = {
  ENVIRONMENT: '环境问题',
  DATA_ISSUE: '数据问题',
  BUG: '代码缺陷',
  PERFORMANCE: '性能问题',
  UNKNOWN: '未知',
}

const categoryColors: Record<string, string> = {
  ENVIRONMENT: '#f0a020',
  DATA_ISSUE: '#2080f0',
  BUG: '#d03050',
  PERFORMANCE: '#18a058',
  UNKNOWN: '#999',
}

const categoryList = computed(() => {
  if (!analysis.value) return []
  const cats = analysis.value.categories
  return [
    { key: 'ENVIRONMENT', label: '🌐 环境问题', count: cats.ENVIRONMENT.count, percentage: cats.ENVIRONMENT.percentage, color: categoryColors.ENVIRONMENT },
    { key: 'DATA_ISSUE', label: '📝 数据问题', count: cats.DATA_ISSUE.count, percentage: cats.DATA_ISSUE.percentage, color: categoryColors.DATA_ISSUE },
    { key: 'BUG', label: '🐛 代码缺陷', count: cats.BUG.count, percentage: cats.BUG.percentage, color: categoryColors.BUG },
    { key: 'PERFORMANCE', label: '⚡ 性能问题', count: cats.PERFORMANCE.count, percentage: cats.PERFORMANCE.percentage, color: categoryColors.PERFORMANCE },
    { key: 'UNKNOWN', label: '❓ 未知', count: cats.UNKNOWN.count, percentage: cats.UNKNOWN.percentage, color: categoryColors.UNKNOWN },
  ]
})

function toggleCategory(cat: string) {
  if (filterCategory.value === cat) {
    filterCategory.value = null
  } else {
    filterCategory.value = cat
  }
  loadResults()
}

const resultTotal = ref(0)
const resultPagination = reactive({
  page: 1,
  pageSize: 20,
  showSizePicker: true,
  pageSizes: [20, 50, 100],
})

const statusOptions = [
  { label: '通过', value: 'PASS' },
  { label: '失败', value: 'FAIL' },
  { label: '错误', value: 'ERROR' },
]

const statusColor: Record<string, any> = { PASS: 'success', FAIL: 'error', ERROR: 'warning' }
const statusLabel: Record<string, string> = { PASS: '通过', FAIL: '失败', ERROR: '错误' }

const failureCategoryColor: Record<string, string> = {
  ENVIRONMENT: '#f0a020',
  DATA_ISSUE: '#2080f0',
  BUG: '#d03050',
  PERFORMANCE: '#18a058',
  UNKNOWN: '#999',
}

const columns = [
  {
    title: '接口',
    key: 'recording_path',
    width: 280,
    resizable: true,
    ellipsis: { tooltip: true },
    render: (r: ReplayResult) => {
      const tag = r.recording_entry_type || 'HTTP'
      const path = r.recording_path || r.recording_id.slice(0, 8)
      const children: any[] = [
        h('span', {
          style: 'display:inline-block;padding:0 5px;border-radius:3px;font-size:11px;font-weight:bold;margin-right:6px;background:#e8f4ff;color:#1677ff',
        }, tag),
        h('span', { style: 'font-family:monospace;font-size:13px' }, path),
      ]
      if (r.recording_service_id) {
        children.push(h('div', {
          style: 'font-size:11px;color:#888;margin-top:2px;font-family:monospace;letter-spacing:0.5px',
        }, r.recording_service_id))
      }
      return h('div', children)
    },
  },
  {
    title: '状态',
    key: 'status',
    render: (r: ReplayResult) =>
      h(NTag, { size: 'small', type: statusColor[r.status || ''] || 'default' }, () => statusLabel[r.status || ''] || r.status || '-'),
  },
  {
    title: '失败分类',
    key: 'failure_category',
    render: (r: ReplayResult) => {
      if (!r.failure_category || r.status === 'PASS') return h('span', { style: 'color:#999' }, '-')
      const color = failureCategoryColor[r.failure_category] || '#999'
      const label = categoryLabels[r.failure_category] || r.failure_category
      return h('span', { style: `color:${color};font-weight:500;font-size:12px` }, label)
    },
  },
  {
    title: 'Diff Score',
    key: 'diff_score',
    render: (r: ReplayResult) =>
      r.diff_score !== null && r.diff_score !== undefined
        ? r.diff_score.toFixed(3)
        : '-',
  },
  {
    title: '断言',
    key: 'assertion_results',
    render: (r: ReplayResult) => {
      if (!r.assertion_results?.length) return h('span', { style: 'color:#999' }, '-')
      const passed = r.assertion_results.filter(a => a.passed).length
      const total = r.assertion_results.length
      const color = passed === total ? '#18a058' : '#d03050'
      return h('span', { style: `color:${color};font-weight:bold` }, `${passed}/${total}`)
    },
  },
  { title: '状态码', key: 'replayed_status_code', render: (r: ReplayResult) => r.replayed_status_code ?? '-' },
  { title: '耗时(ms)', key: 'duration_ms' },
  { title: '时间', key: 'replayed_at', render: (r: ReplayResult) => fmtTime(r.replayed_at) },
  {
    title: '对比',
    key: 'diff',
    render: (r: ReplayResult) =>
      h(NButton, {
        size: 'small',
        onClick: () => { selectedResult.value = r; showDiff.value = true },
      }, () => '查看 Diff'),
  },
]

function formatJson(text?: string | null): string {
  if (!text) return ''
  try {
    return JSON.stringify(JSON.parse(text), null, 2)
  } catch {
    return text
  }
}

// P2-2: 保存为测试用例
async function saveToTestCase() {
  if (!saveForm.case_name || saveForm.recording_ids.length === 0) {
    message.warning('请填写用例名称并选择至少一个接口')
    return
  }
  saving.value = true
  try {
    const res = await replayApi.saveToTestCase(jobId, {
      case_name: saveForm.case_name,
      case_description: saveForm.case_description,
      recording_ids: saveForm.recording_ids,
    })
    message.success(`已创建测试用例 "${res.data.test_case_name}"，包含 ${res.data.added_count} 个接口`)
    showSaveDialog.value = false
    // 重置表单
    saveForm.case_name = ''
    saveForm.case_description = ''
    saveForm.recording_ids = []
  } catch (e: any) {
    message.error(e.response?.data?.detail || '保存失败')
  } finally {
    saving.value = false
  }
}

async function loadResults() {
  resultPagination.page = 1
  await loadResultsPage()
}

async function loadResultsPage() {
  loading.value = true
  try {
    // 如果有筛选分类，先从分析结果中获取对应分类的结果ID
    if (filterCategory.value && analysis.value) {
      const catResults = analysis.value.categories[filterCategory.value as keyof typeof analysis.value.categories]?.results || []
      // 分页处理
      const start = (resultPagination.page - 1) * resultPagination.pageSize
      const pagedIds = catResults.slice(start, start + resultPagination.pageSize).map(r => r.id)
      
      if (pagedIds.length === 0) {
        results.value = []
        resultTotal.value = catResults.length
        return
      }
      
      // 获取完整结果详情
      const allRes = await replayApi.results(jobId, {
        status: undefined,
        limit: 1000,
        offset: 0,
      })
      const filteredResults = allRes.data.items.filter(r => pagedIds.includes(r.id))
      results.value = filteredResults
      resultTotal.value = catResults.length
    } else {
      const res = await replayApi.results(jobId, {
        status: filterStatus.value || undefined,
        limit: resultPagination.pageSize,
        offset: (resultPagination.page - 1) * resultPagination.pageSize,
      })
      results.value = res.data.items
      resultTotal.value = res.data.total
    }
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  const [sumRes, jobRes, analysisRes] = await Promise.all([
    replayApi.summary(jobId),
    replayApi.get(jobId),
    replayApi.analysis(jobId).catch(() => ({ data: null })),
    loadResults(),
  ])
  summary.value = sumRes.data
  job.value = jobRes.data
  if (analysisRes.data) {
    analysis.value = analysisRes.data
  }
})
</script>
