<template>
  <n-card :title="`录制详情 — ${recording?.entry_type || ''} ${recording?.host || ''} ${recording?.path || ''}`" v-if="recording">
    <template #header-extra>
      <n-space>
        <n-button size="small" :loading="recapturing" @click="recapture">重新捕获基线</n-button>
        <n-button size="small" @click="router.back()">返回</n-button>
      </n-space>
    </template>
    <n-descriptions bordered :column="2">
      <n-descriptions-item label="TraceId">{{ recording.trace_id || '-' }}</n-descriptions-item>
      <n-descriptions-item label="应用">{{ recording.entry_app || '-' }}</n-descriptions-item>
      <n-descriptions-item label="Host">{{ recording.host || '-' }}</n-descriptions-item>
      <n-descriptions-item label="耗时">{{ recording.duration_ms ? recording.duration_ms + 'ms' : '-' }}</n-descriptions-item>
      <n-descriptions-item label="时间">{{ fmtTime(recording.timestamp || recording.created_at) }}</n-descriptions-item>
      <n-descriptions-item label="状态">{{ { PASS: '通过', FAIL: '失败', ERROR: '错误', PARSED: '已解析', RAW: '原始', ADDED_TO_CASE: '已加入用例' }[recording.status] || recording.status }}</n-descriptions-item>
      <n-descriptions-item label="标签" :span="2">
        <n-space align="center">
          <n-dynamic-tags v-model:value="editableTags" @update:value="saveTags" />
          <n-tag v-if="tagSaving" size="small" type="info">保存中…</n-tag>
        </n-space>
      </n-descriptions-item>
    </n-descriptions>

    <n-divider>请求报文</n-divider>
    <n-code :code="prettyJson(recording.request_body)" language="json" show-line-numbers />

    <n-divider>响应报文</n-divider>
    <n-code :code="prettyJson(recording.response_body)" language="json" show-line-numbers />

    <n-divider v-if="recording.sub_invocations?.length">子调用 (Mock)</n-divider>
    <n-collapse v-if="recording.sub_invocations?.length">
      <n-collapse-item
        v-for="(sub, i) in recording.sub_invocations"
        :key="i"
        :title="`Sub #${i + 1} — ${sub.type || sub.invokeType || 'UNKNOWN'}`"
      >
        <n-code :code="JSON.stringify(sub, null, 2)" language="json" show-line-numbers />
      </n-collapse-item>
    </n-collapse>
  </n-card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  NCard, NButton, NSpace, NDescriptions, NDescriptionsItem, NDivider, NCode,
  NCollapse, NCollapseItem, NTag, NDynamicTags, useMessage,
} from 'naive-ui'
import { recordingApi, type Recording } from '@/api/recordings'
import { fmtTime } from '@/utils/time'

const route = useRoute()
const router = useRouter()
const message = useMessage()
const recording = ref<Recording | null>(null)
const recapturing = ref(false)
const tagSaving = ref(false)
const editableTags = ref<string[]>([])

async function saveTags(tags: string[]) {
  if (!recording.value) return
  tagSaving.value = true
  try {
    const res = await recordingApi.updateTags(recording.value.id, tags)
    recording.value = res.data
    message.success('标签已保存')
  } catch {
    message.error('保存失败')
  } finally {
    tagSaving.value = false
  }
}

async function recapture() {
  recapturing.value = true
  try {
    const res = await recordingApi.recapture(route.params.id as string)
    recording.value = res.data
    message.success('基线响应已更新')
  } catch (e: any) {
    message.error(e.response?.data?.detail || '捕获失败')
  } finally {
    recapturing.value = false
  }
}

function prettyJson(text?: string | null): string {
  if (!text) return ''
  try {
    return JSON.stringify(JSON.parse(text), null, 2)
  } catch {
    return text
  }
}

onMounted(async () => {
  const res = await recordingApi.get(route.params.id as string)
  recording.value = res.data
  editableTags.value = res.data.tags || []
})
</script>
