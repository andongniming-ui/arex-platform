<template>
  <n-layout has-sider style="height: 100vh">
    <n-layout-sider
      bordered
      collapse-mode="width"
      :collapsed-width="64"
      :width="220"
      :collapsed="collapsed"
      @collapse="collapsed = true"
      @expand="collapsed = false"
    >
      <div class="logo" @click="collapsed = !collapsed">
        <span v-if="!collapsed">🔄 录制回放平台</span>
        <span v-else>🔄</span>
      </div>
      <n-menu
        :collapsed="collapsed"
        :collapsed-width="64"
        :collapsed-icon-size="22"
        :options="menuOptions"
        :value="activeKey"
        @update:value="handleNav"
      />
    </n-layout-sider>

    <n-layout>
      <n-layout-content content-style="padding: 24px; min-height: 100vh; background: #f5f5f5">
        <slot />
      </n-layout-content>
    </n-layout>
  </n-layout>
</template>

<script setup lang="ts">
import { ref, computed, h } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  NLayout, NLayoutSider, NLayoutContent, NMenu,
} from 'naive-ui'
import type { MenuOption } from 'naive-ui'

const collapsed = ref(false)
const router = useRouter()
const route = useRoute()

const activeKey = computed(() => {
  const p = route.path
  if (p.startsWith('/dashboard')) return 'dashboard'
  if (p.startsWith('/applications')) return 'applications'
  if (p.startsWith('/recording')) return 'recording'
  if (p.startsWith('/test-cases')) return 'test-cases'
  if (p === '/replay') return 'replay'
  if (p.startsWith('/replay-history')) return 'replay-history'
  if (p.startsWith('/results')) return 'results'
  if (p.startsWith('/schedules')) return 'schedules'
  if (p.startsWith('/suites')) return 'suites'
  if (p.startsWith('/compare')) return 'compare'
  return 'applications'
})

const menuOptions: MenuOption[] = [
  { label: '数据总览', key: 'dashboard', icon: () => '📊' },
  { label: '应用管理', key: 'applications', icon: () => '🖥' },
  { label: '录制中心', key: 'recording', icon: () => '⏺' },
  { label: '测试用例库', key: 'test-cases', icon: () => '📋' },
  { label: '回放中心', key: 'replay', icon: () => '▶️' },
  { label: '回放历史', key: 'replay-history', icon: () => '📜' },
  { label: '定时回放', key: 'schedules', icon: () => '⏰' },
  { label: '回放套件', key: 'suites', icon: () => '📦' },
  { label: '双环境对比', key: 'compare', icon: () => '🔀' },
]

function handleNav(key: string) {
  router.push('/' + key)
}
</script>

<style scoped>
.logo {
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  padding: 0 16px;
  border-bottom: 1px solid #efeff5;
  white-space: nowrap;
  overflow: hidden;
}
</style>
