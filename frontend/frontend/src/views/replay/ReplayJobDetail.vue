<template>
  <n-card :title="job ? `回放任务 — ${fmtTime(job.created_at)}` : '回放任务'" v-if="job">
    <n-descriptions bordered :column="4">
      <n-descriptions-item label="状态">
        <n-tag :type="statusColor[job.status] || 'default'">{{ statusLabel[job.status] || job.status }}</n-tag>
      </n-descriptions-item>
      <n-descriptions-item label="总数">{{ job.total_count }}</n-descriptions-item>
      <n-descriptions-item label="通过">
        <n-tag type="success">{{ job.success_count }}</n-tag>
      </n-descriptions-item>
      <n-descriptions-item label="失败">
        <n-tag type="error">{{ job.fail_count }}</n-tag>
      </n-descriptions-item>
    </n-descriptions>
    <n-button style="margin-top: 12px" @click="router.push(`/results/${jobId}`)">
      查看对比详情
    </n-button>
  </n-card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { NCard, NDescriptions, NDescriptionsItem, NTag, NButton } from 'naive-ui'
import { replayApi, type ReplayJob } from '@/api/replays'
import { fmtTime } from '@/utils/time'

const route = useRoute()
const router = useRouter()
const jobId = route.params.jobId as string
const job = ref<ReplayJob | null>(null)

const statusColor: Record<string, any> = {
  DONE: 'success', RUNNING: 'info', FAILED: 'error', CANCELLED: 'warning',
}

const statusLabel: Record<string, string> = {
  DONE: '已完成', RUNNING: '运行中', FAILED: '失败', CANCELLED: '已取消',
}

onMounted(async () => {
  const res = await replayApi.get(jobId)
  job.value = res.data
})
</script>
