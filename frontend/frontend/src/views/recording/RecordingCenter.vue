<template>
  <n-card title="录制中心">
    <template #header-extra>
      <n-button v-if="fromAppId" size="small" @click="router.push(`/applications/${fromAppId}`)">← 返回应用详情</n-button>
    </template>
    <n-space vertical :size="12">
      <n-space align="center" wrap>
        <n-select
          v-model:value="filterAppId"
          :options="appOptions"
          placeholder="选择应用"
          clearable
          style="width: 180px"
          @update:value="onAppChange"
        />
        <n-select
          v-model:value="filterSessionId"
          :options="sessionOptions"
          placeholder="选择会话"
          clearable
          style="width: 220px"
          @update:value="load"
        />
        <n-select
          v-model:value="filterType"
          :options="typeOptions"
          placeholder="入口类型"
          clearable
          style="width: 130px"
          @update:value="load"
        />
        <n-date-picker
          v-model:value="filterDateRange"
          type="datetimerange"
          clearable
          :shortcuts="dateShortcuts"
          style="width: 340px"
          start-placeholder="开始时间"
          end-placeholder="结束时间"
          @update:value="load"
          @clear="load"
        />
        <n-select
          v-model:value="filterQuality"
          :options="qualityOptions"
          placeholder="响应质量"
          clearable
          style="width: 130px"
          @update:value="applyQualityFilter"
        />
        <n-button @click="load">搜索</n-button>
        <n-button @click="showHarModal = true">导入 HAR</n-button>
        <n-button
          size="small"
          :type="failedSelected ? 'warning' : 'default'"
          :secondary="!failedSelected"
          @click="toggleFailedRows"
          :disabled="filteredRecordings.length === 0"
        >{{ failedSelected ? '撤销选中' : '选中失败项' }}</n-button>
      </n-space>

      <n-data-table
        :columns="columns"
        :data="filteredRecordings"
        :loading="loading"
        :row-key="(r: any) => r.id"
        :checked-row-keys="selectedIds"
        :scroll-x="1050"
        @update:checked-row-keys="selectedIds = $event as string[]"
      />

      <n-space justify="end" style="margin-top:12px">
        <n-pagination
          v-model:page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :page-sizes="pagination.pageSizes"
          :item-count="pagination.itemCount"
          show-size-picker
          :show-quick-jumper="true"
          :disabled="loading"
          @update:page="loadPage"
          @update:page-size="(size) => { pagination.pageSize = size; pagination.page = 1; loadPage() }"
        >
          <template #prefix>
            <span style="font-size:13px;color:#666">共 {{ pagination.itemCount }} 条</span>
          </template>
        </n-pagination>
      </n-space>

      <n-space v-if="selectedIds.length > 0" align="center">
        <span>已选 {{ selectedIds.length }} 条</span>
        <n-button size="small" type="primary" @click="showAddToCase = true">加入测试用例</n-button>
        <n-button size="small" @click="showTagModal = true">批量打标签</n-button>
        <n-button size="small" type="error" :loading="batchDeleting" @click="deleteSelected">批量删除</n-button>
      </n-space>
    </n-space>
  </n-card>

  <!-- HAR 导入弹窗 -->
  <n-modal v-model:show="showHarModal" preset="dialog" title="导入 HAR 文件">
    <n-space vertical>
      <span style="color:#666;font-size:13px">选择应用和 .har 文件，将自动创建录制会话并导入 HTTP 请求条目</span>
      <n-select
        v-model:value="harAppId"
        :options="appOptions"
        placeholder="选择目标应用（必选）"
        style="width:100%"
      />
      <n-upload
        :key="harUploadKey"
        :max="1"
        accept=".har"
        :default-upload="false"
        @change="onHarFileChange"
      >
        <n-button>选择 .har 文件</n-button>
      </n-upload>
      <span v-if="harFileName" style="color:#18a058;font-size:13px">已选: {{ harFileName }}</span>
    </n-space>
    <template #action>
      <n-button @click="showHarModal = false">取消</n-button>
      <n-button type="primary" :loading="harImporting" :disabled="!harAppId || !harFile" @click="importHar">导入</n-button>
    </template>
  </n-modal>

  <!-- 加入测试用例弹窗 -->
  <n-modal v-model:show="showAddToCase" preset="dialog" title="加入测试用例">
    <n-select
      v-model:value="targetCaseId"
      :options="caseOptions"
      placeholder="选择测试用例"
      filterable
    />
    <template #action>
      <n-button @click="showAddToCase = false">取消</n-button>
      <n-button type="primary" @click="addToCase">确认</n-button>
    </template>
  </n-modal>

  <!-- 批量打标签弹窗 -->
  <n-modal v-model:show="showTagModal" preset="dialog" title="批量设置标签">
    <n-space vertical>
      <span style="color:#666;font-size:13px">将以下标签设置给选中的 {{ selectedIds.length }} 条录制（会覆盖已有标签）</span>
      <n-dynamic-tags v-model:value="batchTags" />
    </n-space>
    <template #action>
      <n-button @click="showTagModal = false">取消</n-button>
      <n-button type="primary" :loading="tagging" @click="applyBatchTags">确认</n-button>
    </template>
  </n-modal>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch, onMounted, onActivated, h } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  NCard, NSpace, NSelect, NButton, NDataTable, NTag, NModal,
  NIcon, NDynamicTags, NUpload, NPagination, NDatePicker, useMessage, useDialog,
} from 'naive-ui'
import { recordingApi, sessionApi, type Recording, type Session } from '@/api/recordings'
import { fmtTime } from '@/utils/time'
import { applicationApi } from '@/api/applications'
import { testCaseApi } from '@/api/testCases'

const route = useRoute()
const router = useRouter()
const message = useMessage()
const dialog = useDialog()

const recordings = ref<Recording[]>([])
const loading = ref(false)
const batchDeleting = ref(false)
const tagging = ref(false)
const selectedIds = ref<string[]>([])

// 从应用详情跳入时携带 app_id，用于显示返回按钮
const fromAppId = ref<string | null>(route.query.app_id as string || null)
const filterAppId = ref<string | null>(route.query.app_id as string || null)
const filterSessionId = ref<string | null>(route.query.session_id as string || null)
const filterType = ref<string | null>(null)
const filterDateRange = ref<[number, number] | null>(null)
const filterQuality = ref<string | null>(null)

const now = Date.now()
const dateShortcuts = {
  '今天': () => [new Date().setHours(0, 0, 0, 0), now] as [number, number],
  '最近3天': () => [now - 3 * 86400000, now] as [number, number],
  '最近7天': () => [now - 7 * 86400000, now] as [number, number],
  '最近30天': () => [now - 30 * 86400000, now] as [number, number],
}

const appOptions = ref<{ label: string; value: string }[]>([])
const allSessions = ref<Session[]>([])
const sessionOptions = ref<{ label: string; value: string }[]>([])
const caseOptions = ref<{ label: string; value: string }[]>([])
const showAddToCase = ref(false)
const showTagModal = ref(false)
const batchTags = ref<string[]>([])
const targetCaseId = ref<string | null>(null)

// HAR import state
const showHarModal = ref(false)
const harAppId = ref<string | null>(null)
const harFile = ref<File | null>(null)
const harFileName = ref('')
const harImporting = ref(false)
const harUploadKey = ref(0)

watch(showHarModal, (val) => {
  if (val) {
    harAppId.value = null
    harFile.value = null
    harFileName.value = ''
    harUploadKey.value++  // 强制 NUpload 重新挂载，清空内部文件列表
  }
})

function onHarFileChange({ file }: any) {
  harFile.value = file.file ?? null
  harFileName.value = file.name
}

async function importHar() {
  if (!harAppId.value || !harFile.value) return
  harImporting.value = true
  try {
    const fd = new FormData()
    fd.append('app_id', harAppId.value)
    fd.append('file', harFile.value)
    const res = await recordingApi.importHar(fd)
    message.success(`已导入 ${res.data.imported} 条录制`)
    showHarModal.value = false
    harFile.value = null
    harFileName.value = ''
    harAppId.value = null
    await load()
  } catch (e: any) {
    message.error(e.response?.data?.detail || '导入失败')
  } finally {
    harImporting.value = false
  }
}

const pagination = reactive({
  page: 1,
  pageSize: 20,
  showSizePicker: true,
  pageSizes: [20, 50, 100],
  itemCount: 0,
  onChange: (page: number) => { pagination.page = page; loadPage() },
  onUpdatePageSize: (pageSize: number) => { pagination.pageSize = pageSize; pagination.page = 1; loadPage() },
})

function onAppChange(appId: string | null) {
  filterSessionId.value = null
  if (appId) {
    sessionOptions.value = allSessions.value
      .filter(s => s.app_id === appId)
      .map(s => ({ label: `${s.name || s.id.slice(0, 8)} (${s.status})`, value: s.id }))
  } else {
    sessionOptions.value = allSessions.value.map(s => ({
      label: `${s.name || s.id.slice(0, 8)} (${s.status})`,
      value: s.id,
    }))
  }
  load()
}

watch(showAddToCase, async (val) => {
  if (val) {
    const res = await testCaseApi.list({ app_id: filterAppId.value || undefined, limit: 500 })
    caseOptions.value = res.data.items.map(c => ({ label: c.name, value: c.id }))
    targetCaseId.value = null
  }
})

const typeOptions = [
  { label: 'HTTP', value: 'HTTP' },
  { label: 'DUBBO', value: 'DUBBO' },
  { label: 'MYBATIS', value: 'MYBATIS' },
  { label: 'JAVA', value: 'JAVA' },
]

const qualityOptions = [
  { label: '✅ 成功 (2xx)', value: '2xx' },
  { label: '❌ 失败 (4xx)', value: '4xx' },
  { label: '❌ 服务错误 (5xx)', value: '5xx' },
  { label: '⚠️ 空响应', value: 'empty' },
  { label: '❓ 未知', value: 'unknown' },
]

/**
 * Detect response quality from response_body.
 * Checks for: JSON {"status": NNN, ...} or XML <code>NNN</code> / <status>NNN</status>
 */
function getResponseQuality(r: Recording): '2xx' | '4xx' | '5xx' | 'empty' | 'unknown' {
  const body = r.response_body
  if (!body || !body.trim()) return 'empty'

  // Try JSON
  try {
    const obj = JSON.parse(body)
    const code = obj.status ?? obj.code ?? obj.statusCode ?? obj.httpStatus
    if (typeof code === 'number') {
      if (code >= 200 && code < 300) return '2xx'
      if (code >= 400 && code < 500) return '4xx'
      if (code >= 500) return '5xx'
    }
    if (typeof code === 'string') {
      const n = parseInt(code)
      if (!isNaN(n)) {
        if (n >= 200 && n < 300) return '2xx'
        if (n >= 400 && n < 500) return '4xx'
        if (n >= 500) return '5xx'
      }
    }
    // Has JSON content but no recognizable status code → treat as 2xx (success body)
    return '2xx'
  } catch {}

  // Try XML: look for <code>NNN</code> or <status>NNN</status> or <httpStatus>NNN</httpStatus>
  const xmlMatch = body.match(/<(?:code|status|httpStatus|errorCode)>(\d{3})<\//)
  if (xmlMatch) {
    const n = parseInt(xmlMatch[1])
    if (n >= 200 && n < 300) return '2xx'
    if (n >= 400 && n < 500) return '4xx'
    if (n >= 500) return '5xx'
  }

  // Has XML/text content but no recognizable status → treat as 2xx
  if (body.trim().startsWith('<') || body.trim().length > 10) return '2xx'
  return 'unknown'
}

const qualityColorMap: Record<string, 'success' | 'error' | 'warning' | 'default'> = {
  '2xx': 'success',
  '4xx': 'error',
  '5xx': 'error',
  'empty': 'warning',
  'unknown': 'default',
}

const qualityLabelMap: Record<string, string> = {
  '2xx': '成功',
  '4xx': '失败4xx',
  '5xx': '服务错误',
  'empty': '空响应',
  'unknown': '未知',
}

const filteredRecordings = computed(() => {
  if (!filterQuality.value) return recordings.value
  return recordings.value.filter(r => getResponseQuality(r) === filterQuality.value)
})

function applyQualityFilter() {
  selectedIds.value = []
}

const failedIds = computed(() =>
  filteredRecordings.value
    .filter(r => { const q = getResponseQuality(r); return q === '4xx' || q === '5xx' || q === 'empty' })
    .map(r => r.id)
)

const failedSelected = computed(() =>
  failedIds.value.length > 0 &&
  failedIds.value.every(id => selectedIds.value.includes(id))
)

function toggleFailedRows() {
  if (failedIds.value.length === 0) {
    message.info('当前页没有失败的录制')
    return
  }
  if (failedSelected.value) {
    // 撤销：移除所有失败项的选中
    selectedIds.value = selectedIds.value.filter(id => !failedIds.value.includes(id))
  } else {
    // 选中：合并已选 + 失败项（去重）
    const merged = new Set([...selectedIds.value, ...failedIds.value])
    selectedIds.value = [...merged]
    message.info(`已选中 ${failedIds.value.length} 条失败/空响应的录制`)
  }
}

const statusColor: Record<string, any> = {
  PASS: 'success', FAIL: 'error', ERROR: 'error', PARSED: 'info', RAW: 'default', ADDED_TO_CASE: 'success',
}

const statusLabel: Record<string, string> = {
  PASS: '通过', FAIL: '失败', ERROR: '错误', PARSED: '已解析', RAW: '原始', ADDED_TO_CASE: '已加入用例',
}

const columns = [
  { type: 'selection' as const, width: 40 },
  {
    title: '入口类型', key: 'entry_type', width: 85,
    render: (r: Recording) => h(NTag, { size: 'small', type: 'info' }, () => r.entry_type || '-'),
  },
  { title: 'Host', key: 'host', width: 150, ellipsis: { tooltip: true } },
  { title: '路径', key: 'path', width: 200, ellipsis: { tooltip: true } },
  {
    title: '响应质量', key: 'resp_quality', width: 90,
    render: (r: Recording) => {
      const q = getResponseQuality(r)
      return h(NTag, { size: 'small', type: qualityColorMap[q] }, () => qualityLabelMap[q])
    },
  },
  {
    title: '标签', key: 'tags', width: 130,
    render: (r: Recording) =>
      r.tags?.length
        ? h(NSpace, { size: 4 }, () => r.tags!.map(t => h(NTag, { size: 'small', type: 'warning' }, () => t)))
        : '-',
  },
  { title: '耗时(ms)', key: 'duration_ms', width: 80 },
  {
    title: '状态', key: 'status', width: 90,
    render: (r: Recording) =>
      h(NTag, { size: 'small', type: statusColor[r.status] || 'default' }, () => statusLabel[r.status] || r.status),
  },
  {
    title: '时间', key: 'created_at', width: 155,
    render: (r: Recording) => fmtTime(r.created_at),
  },
  {
    title: '操作', key: 'actions', width: 110,
    render: (r: Recording) =>
      h(NSpace, { size: 'small' }, () => [
        h(NButton, { size: 'small', onClick: () => router.push(`/recordings/${r.id}`) }, () => '查看'),
        h(NButton, { size: 'small', type: 'error', onClick: () => deleteSingle(r.id) }, () => '删除'),
      ]),
  },
]

// 筛选条件变化时重置到第 1 页
async function load() {
  pagination.page = 1
  selectedIds.value = []
  await loadPage()
}

// 翻页/改页大小时调用，不重置页码
async function loadPage() {
  loading.value = true
  selectedIds.value = []
  try {
    const res = await recordingApi.list({
      app_id: filterAppId.value || undefined,
      session_id: filterSessionId.value || undefined,
      entry_type: filterType.value || undefined,
      created_after: filterDateRange.value ? new Date(filterDateRange.value[0]).toISOString() : undefined,
      created_before: filterDateRange.value ? new Date(filterDateRange.value[1]).toISOString() : undefined,
      limit: pagination.pageSize,
      offset: (pagination.page - 1) * pagination.pageSize,
    })
    recordings.value = res.data.items
    pagination.itemCount = res.data.total
  } finally {
    loading.value = false
  }
}

async function deleteSingle(id: string) {
  dialog.warning({
    title: '确认删除', content: '删除后不可恢复，确认吗？',
    positiveText: '删除', negativeText: '取消',
    onPositiveClick: async () => {
      await recordingApi.delete(id)
      message.success('已删除')
      selectedIds.value = selectedIds.value.filter(i => i !== id)
      await loadPage()
    },
  })
}

async function deleteSelected() {
  dialog.warning({
    title: '确认批量删除',
    content: `将删除选中的 ${selectedIds.value.length} 条录制，确认吗？`,
    positiveText: '删除', negativeText: '取消',
    onPositiveClick: async () => {
      batchDeleting.value = true
      try {
        const count = selectedIds.value.length
        await recordingApi.batchDelete(selectedIds.value)
        message.success(`已删除 ${count} 条`)
        selectedIds.value = []
        await loadPage()
      } finally {
        batchDeleting.value = false
      }
    },
  })
}

async function applyBatchTags() {
  tagging.value = true
  try {
    for (const id of selectedIds.value) {
      await recordingApi.updateTags(id, batchTags.value)
    }
    message.success(`已为 ${selectedIds.value.length} 条录制设置标签`)
    showTagModal.value = false
    await load()
  } finally {
    tagging.value = false
  }
}

async function addToCase() {
  if (!targetCaseId.value) { message.warning('请选择测试用例'); return }
  const res = await testCaseApi.addRecordings(targetCaseId.value, selectedIds.value)
  message.success(`已添加 ${res.data.added} 条录制到用例`)
  showAddToCase.value = false
  selectedIds.value = []
}

async function init() {
  const [appsRes, sessionsRes] = await Promise.all([
    applicationApi.list(),
    sessionApi.list(),
  ])
  appOptions.value = appsRes.data.map(a => ({ label: a.name, value: a.id }))
  allSessions.value = sessionsRes.data.items

  if (filterSessionId.value) {
    const s = sessionsRes.data.items.find(s => s.id === filterSessionId.value)
    if (s) filterAppId.value = s.app_id
  }

  sessionOptions.value = (filterAppId.value
    ? sessionsRes.data.items.filter(s => s.app_id === filterAppId.value)
    : sessionsRes.data.items
  ).map(s => ({ label: `${s.name || s.id.slice(0, 8)} (${s.status})`, value: s.id }))

  await load()
}

onMounted(init)
onActivated(init)
</script>
