<template>
  <el-dialog v-model="aboutDialogVisible" class="about-dialog border-r-4">
    <template #header="{ titleId, titleClass }">
      <div class="logo flex-center" :id="titleId" :class="titleClass">
        <img src="@/assets/MaxKB-logo.svg" height="59" />
      </div>
    </template>
    <div class="about-ui">
      <el-card
        shadow="hover"
        class="mb-16"
        @click="toUrl('https://maxkb.cn/docs/')"
      >
        <div class="flex align-center cursor">
          <AppIcon iconName="app-reading" class="mr-16 ml-8" style="font-size: 24px"></AppIcon>
          <span>{{ $t('layout.topbar.wiki') }}</span>
        </div>
      </el-card>
      <el-card shadow="hover" class="mb-16" @click="toUrl('https://github.com/1Panel-dev/MaxKB')">
        <div class="flex align-center cursor">
          <AppIcon iconName="app-github" class="mr-16 ml-8" style="font-size: 24px"></AppIcon>
          <span>{{ $t('layout.topbar.github') }}</span>
        </div>
      </el-card>
      <el-card shadow="hover" class="mb-16" @click="toUrl('https://bbs.fit2cloud.com/c/mk/11')">
        <div class="flex align-center cursor">
          <AppIcon iconName="app-help" class="mr-16 ml-8" style="font-size: 24px"></AppIcon>
          <span>{{ $t('layout.topbar.forum') }}</span>
        </div>
      </el-card>
    </div>
    <div class="text-center">{{ $t('layout.topbar.avatar.version') }}:{{ user.version }}</div>
  </el-dialog>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import useStore from '@/stores'
const defaultTitle = import.meta.env.VITE_APP_TITLE

const { user } = useStore()

const aboutDialogVisible = ref(false)

const open = () => {
  aboutDialogVisible.value = true
}

function toUrl(url: string) {
  window.open(url, '_blank')
}

defineExpose({ open })
</script>
<style lang="scss" scope>
.about-dialog {
  padding: 0 0 24px 0;
  width: 600px;
  font-weight: 400;
  .el-dialog__header {
    background: var(--app-header-bg-color);
    margin-right: 0;
    height: 140px;
    box-sizing: border-box;
    border-radius: 4px 4px 0 0;
  }
  .el-dialog__title {
    height: 140px;
    box-sizing: border-box;
  }
  .about-ui {
    width: 360px;
    margin: 0 auto;
    font-weight: 400;
    font-size: 16px;
    margin-top: 24px;
    .label {
      width: 180px;
      text-align: left;
      color: var(--app-text-color-secondary);
    }
  }
}
</style>
