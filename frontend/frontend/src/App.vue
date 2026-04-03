<template>
  <n-config-provider :theme="null" :locale="zhCN" :date-locale="dateZhCN">
    <n-message-provider>
      <n-dialog-provider>
        <AppLayout>
          <router-view />
        </AppLayout>
      </n-dialog-provider>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
import { NConfigProvider, NMessageProvider, NDialogProvider, zhCN, dateZhCN } from 'naive-ui'
import AppLayout from './components/layout/AppLayout.vue'
</script>
