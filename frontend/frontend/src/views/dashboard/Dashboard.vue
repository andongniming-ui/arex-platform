<template>
  <n-space vertical :size="16">
    <!-- 汇总统计卡片 -->
    <n-card title="总览">
      <template #header-extra>
        <n-space>
          <n-select
            v-model:value="filterAppId"
            :options="appOptions"
            placeholder="全部应用"
            clearable
            style="width: 180px"
            @update:value="reload"
          />
          <n-select
            v-model:value="days"
            :options="dayOptions"
            style="width: 110px"
            @update:value="reload"
          />
        </n-space>
      </template>
      <n-space :size="24" v-if="summary">
        <n-statistic label="回放任务数" :value="summary.job_count" />
        <n-statistic label="总发送">
          <template #default><span>{{ summary.total_sent }}</span></template>
        </n-statistic>
        <n-statistic label="通过">
          <template #default><span style="color:#18a058">{{ summary.total_pass }}</span></template>
        </n-statistic>
        <n-statistic label="失败">
          <template #default><span style="color:#d03050">{{ summary.total_fail }}</span></template>
        </n-statistic>
        <n-statistic label="错误">
          <template #default><span style="color:#f0a020">{{ summary.total_error }}</span></template>
        </n-statistic>
        <n-statistic label="平均通过率">
          <template #default>
            <span :style="{ color: summary.avg_pass_rate >= 90 ? '#18a058' : '#d03050' }">
              {{ summary.avg_pass_rate.toFixed(1) }}%
            </span>
          </template>
        </n-statistic>
      </n-space>
      <n-skeleton v-else :repeat="6" height="60px" />
    </n-card>

    <!-- 趋势图 -->
    <n-card title="通过率趋势">
      <v-chart
        :option="chartOption"
        :loading="loading"
        style="height: 340px"
        autoresize
      />
    </n-card>

    <!-- 每日明细 -->
    <n-card title="每日明细">
      <n-space style="margin-bottom: 12px">
        <n-input
          v-model:value="trendSearchDate"
          placeholder="搜索日期，如 03-15"
          clearable
          style="width: 180px"
        />
        <n-select
          v-model:value="trendSearchStatus"
          :options="trendStatusOptions"
          placeholder="通过率筛选"
          clearable
          style="width: 150px"
        />
      </n-space>
      <span style="color:#999;font-size:13px;margin-bottom:10px;display:block">共 {{ filteredTrend.length }} 条</span>
      <n-data-table
        :columns="tableColumns"
        :data="filteredTrend"
        size="small"
        :pagination="tablePagination"
        :row-props="rowProps"
      />
    </n-card>
  </n-space>

  <!-- 当日任务详情抽屉 -->
  <n-drawer v-model:show="showDrawer" :width="620" placement="right">
    <n-drawer-content :title="`${drawerDate} 回放任务`" closable>
      <n-spin :show="drawerLoading">
        <n-empty v-if="!drawerLoading && drawerJobs.length === 0" description="当日无回放任务" />
        <template v-else>
          <span style="color:#999;font-size:13px;margin-bottom:10px;display:block">共 {{ drawerJobs.length }} 条</span>
          <n-data-table
            :columns="drawerColumns"
            :data="drawerJobs"
            size="small"
            :pagination="drawerPagination"
          />
        </template>
      </n-spin>
    </n-drawer-content>
  </n-drawer>
</template>

<script setup lang="ts">
import { ref, computed, reactive, onMounted, h, watch } from 'vue'
import { useRouter } from 'vue-router'
import {
  NCard, NSpace, NStatistic, NSelect, NSkeleton, NDataTable, NTag,
  NDrawer, NDrawerContent, NSpin, NEmpty, NButton, NInput,
} from 'naive-ui'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent, DataZoomComponent } from 'echarts/components'
import VChart from 'vue-echarts'
import { statsApi, type TrendPoint, type Summary, type DailyJob } from '@/api/stats'
import { applicationApi } from '@/api/applications'
import { fmtTime } from '@/utils/time'

use([CanvasRenderer, LineChart, BarChart, GridComponent, TooltipComponent, LegendComponent, DataZoomComponent])

const router = useRouter()
const filterAppId = ref<string | null>(null)
const days = ref(7)
const loading = ref(false)
const trend = ref<TrendPoint[]>([])
const summary = ref<Summary | null>(null)
const appOptions = ref<{ label: string; value: string }[]>([])
const appMap = ref<Record<string, string>>({})

// 抽屉状态
const showDrawer = ref(false)
const drawerDate = ref('')
const drawerLoading = ref(false)
const drawerJobs = ref<DailyJob[]>([])

const trendSearchDate = ref('')
const trendSearchStatus = ref<string | null>(null)

const trendStatusOptions = [
  { label: '有数据', value: 'hasData' },
  { label: '通过率 ≥ 90%', value: 'pass' },
  { label: '通过率 < 90%', value: 'fail' },
  { label: '无数据', value: 'noData' },
]

const filteredTrend = computed(() => {
  let list = [...trend.value].reverse()
  if (trendSearchDate.value) {
    const kw = trendSearchDate.value.toLowerCase()
    list = list.filter(p => p.date.toLowerCase().includes(kw))
  }
  if (trendSearchStatus.value === 'hasData') {
    list = list.filter(p => p.total > 0)
  } else if (trendSearchStatus.value === 'noData') {
    list = list.filter(p => p.total === 0)
  } else if (trendSearchStatus.value === 'pass') {
    list = list.filter(p => p.total > 0 && (p.pass_rate ?? 0) >= 90)
  } else if (trendSearchStatus.value === 'fail') {
    list = list.filter(p => p.total > 0 && (p.pass_rate ?? 0) < 90)
  }
  return list
})

// 搜索条件变化时重置到第一页
watch([trendSearchDate, trendSearchStatus], () => { tablePagination.page = 1 })

const tablePagination = reactive({
  page: 1,
  pageSize: 7,
  showSizePicker: true,
  pageSizes: [7, 14, 30],
  onChange: (page: number) => { tablePagination.page = page },
  onUpdatePageSize: (size: number) => { tablePagination.pageSize = size; tablePagination.page = 1 },
})

const drawerPagination = reactive({
  page: 1,
  pageSize: 10,
  showSizePicker: true,
  pageSizes: [10, 20, 50],
  onChange: (page: number) => { drawerPagination.page = page },
  onUpdatePageSize: (size: number) => { drawerPagination.pageSize = size; drawerPagination.page = 1 },
})

const dayOptions = [
  { label: '近 7 天', value: 7 },
  { label: '近 14 天', value: 14 },
  { label: '近 30 天', value: 30 },
  { label: '近 90 天', value: 90 },
]

const chartOption = computed(() => {
  const dates = trend.value.map(p => p.date)
  const passRates = trend.value.map(p => p.pass_rate)
  const passCounts = trend.value.map(p => p.pass)
  const failCounts = trend.value.map(p => p.fail)
  const errorCounts = trend.value.map(p => p.error)

  // 根据天数决定 x 轴标签间隔：≤14 天全显，≤30 天隔一个，>30 天隔两个
  const n = dates.length
  const labelInterval = n <= 14 ? 0 : n <= 30 ? 1 : 2

  return {
    tooltip: {
      trigger: 'axis',
      formatter: (params: any[]) => {
        // axisValue 是 MM-DD，从原始 dates 数组取完整日期
        const fullDate = dates[params[0].dataIndex] ?? params[0].axisValue
        const lines = params.map((p: any) => `${p.marker}${p.seriesName}: ${p.value ?? '-'}`).join('<br/>')
        return `${fullDate}<br/>${lines}`
      },
    },
    legend: { data: ['通过率(%)', '通过', '失败', '错误'] },
    grid: { left: 40, right: 40, top: 40, bottom: 70 },
    dataZoom: [{ type: 'slider', bottom: 4 }],
    xAxis: {
      type: 'category',
      // tooltip 显示完整日期，轴标签只显示 MM-DD
      data: dates.map(d => d.slice(5)),
      axisLabel: {
        rotate: 45,
        fontSize: 12,
        interval: labelInterval,
        color: '#666',
      },
      axisTick: { alignWithLabel: true },
    },
    yAxis: [
      { type: 'value', name: '通过率(%)', min: 0, max: 100, position: 'left' },
      { type: 'value', name: '条数', position: 'right', splitLine: { show: false } },
    ],
    series: [
      {
        name: '通过率(%)',
        type: 'line',
        yAxisIndex: 0,
        data: passRates,
        smooth: true,
        lineStyle: { width: 2 },
        itemStyle: { color: '#18a058' },
        areaStyle: { color: 'rgba(24,160,88,0.08)' },
        connectNulls: true,
      },
      {
        name: '通过', type: 'bar', yAxisIndex: 1, data: passCounts,
        itemStyle: { color: 'rgba(24,160,88,0.7)' }, stack: 'count',
      },
      {
        name: '失败', type: 'bar', yAxisIndex: 1, data: failCounts,
        itemStyle: { color: 'rgba(208,48,80,0.7)' }, stack: 'count',
      },
      {
        name: '错误', type: 'bar', yAxisIndex: 1, data: errorCounts,
        itemStyle: { color: 'rgba(240,160,32,0.7)' }, stack: 'count',
      },
    ],
  }
})

const statusColor: Record<string, any> = {
  DONE: 'success', FAILED: 'error', RUNNING: 'info', PENDING: 'default',
}

const statusLabel: Record<string, string> = {
  DONE: '已完成', FAILED: '失败', RUNNING: '运行中', PENDING: '待处理',
}

const tableColumns = [
  {
    title: '日期', key: 'date', width: 120,
    render: (r: TrendPoint) =>
      h('span', { style: 'color:#1677ff;cursor:pointer' }, r.date),
  },
  { title: '通过率', key: 'pass_rate', width: 90,
    render: (r: TrendPoint) => {
      if (r.total === 0) return h('span', { style: 'color:#999' }, '-')
      const color = (r.pass_rate ?? 0) >= 90 ? '#18a058' : '#d03050'
      return h('span', { style: `color:${color};font-weight:bold` }, `${r.pass_rate}%`)
    },
  },
  { title: '总计', key: 'total', width: 70 },
  { title: '通过', key: 'pass', width: 70,
    render: (r: TrendPoint) => r.pass > 0 ? h(NTag, { size: 'small', type: 'success' }, () => r.pass) : '-',
  },
  { title: '失败', key: 'fail', width: 70,
    render: (r: TrendPoint) => r.fail > 0 ? h(NTag, { size: 'small', type: 'error' }, () => r.fail) : '-',
  },
  { title: '错误', key: 'error', width: 70,
    render: (r: TrendPoint) => r.error > 0 ? h(NTag, { size: 'small', type: 'warning' }, () => r.error) : '-',
  },
]

// 抽屉内任务列表列定义
const drawerColumns = [
  {
    title: '任务 ID', key: 'id', width: 90,
    render: (r: DailyJob) => h('code', { style: 'font-size:12px' }, r.id.slice(0, 8)),
  },
  {
    title: '目标应用', key: 'target_app_id',
    render: (r: DailyJob) => appMap.value[r.target_app_id] || r.target_app_id.slice(0, 8),
  },
  {
    title: '状态', key: 'status', width: 75,
    render: (r: DailyJob) =>
      h(NTag, { size: 'small', type: statusColor[r.status] || 'default' }, () => statusLabel[r.status] || r.status),
  },
  {
    title: '通过/总计', key: 'progress', width: 90,
    render: (r: DailyJob) => {
      const pct = r.sent_count ? Math.round(r.success_count / r.sent_count * 100) : 0
      const color = pct >= 90 ? '#18a058' : '#d03050'
      return h('span', { style: `color:${color};font-weight:bold` },
        `${r.success_count}/${r.sent_count} (${pct}%)`)
    },
  },
  {
    title: '完成时间', key: 'finished_at', width: 155,
    render: (r: DailyJob) => fmtTime(r.finished_at),
  },
  {
    title: '操作', key: 'actions', width: 80,
    render: (r: DailyJob) =>
      h(NButton, {
        size: 'small',
        onClick: () => router.push(`/results/${r.id}`),
      }, () => '查看结果'),
  },
]

// 行点击：仅当该日有数据时才打开抽屉
function rowProps(row: TrendPoint) {
  return {
    style: row.total > 0 ? 'cursor:pointer;' : '',
    onClick: () => {
      if (row.total === 0) return
      openDrawer(row.date)
    },
  }
}

async function openDrawer(date: string) {
  drawerDate.value = date
  showDrawer.value = true
  drawerLoading.value = true
  drawerJobs.value = []
  drawerPagination.page = 1
  try {
    const res = await statsApi.dailyJobs(date, filterAppId.value)
    drawerJobs.value = res.data
  } finally {
    drawerLoading.value = false
  }
}

async function reload() {
  loading.value = true
  try {
    const params = { app_id: filterAppId.value || undefined, days: days.value }
    const [trendRes, sumRes] = await Promise.all([
      statsApi.trend(params),
      statsApi.summary({ app_id: filterAppId.value || undefined }),
    ])
    trend.value = trendRes.data
    summary.value = sumRes.data
    tablePagination.page = 1
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  const res = await applicationApi.list()
  appOptions.value = res.data.map(a => ({ label: a.name, value: a.id }))
  appMap.value = Object.fromEntries(res.data.map(a => [a.id, a.name]))
  await reload()
})
</script>
