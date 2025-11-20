<template>
  <el-container class="app-layout">
    <!-- 左侧菜单 -->
    <el-aside width="220px" class="aside">
      <div class="logo">毕业设计辅助管理系统</div>
      <el-menu
        router
        :default-active="activeMenu"
        background-color="#1f55d0"
        text-color="#fff"
        active-text-color="#ffd04b"
        class="side-menu"
      >
        <el-menu-item index="/topic-apply">课题申报</el-menu-item>
        <el-menu-item index="/topic-publish">课题发布</el-menu-item>
        <el-menu-item index="/topic-select">选题管理</el-menu-item>
        <el-menu-item index="/opening-manage">开题管理</el-menu-item>
        <el-menu-item index="/midterm-check">中期检查</el-menu-item>
        <el-menu-item index="/paper-upload">纸质资料及考核表</el-menu-item>
        <el-menu-item index="/score">成绩录入 / 查询</el-menu-item>
        <el-menu-item index="/notification">通知管理</el-menu-item>
        <el-menu-item index="/topic-review">课题审批</el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 右侧内容 -->
    <el-container>
      <el-header class="header">
        <div class="header-left">
          <el-icon><Menu /></el-icon>
          <span class="page-title">{{ currentTitle }}</span>
        </div>
        <div class="header-right">
          <el-input
            v-model="search"
            placeholder="快速检索"
            size="small"
            class="header-search"
            :prefix-icon="Search"
          />
          <el-dropdown>
            <span class="el-dropdown-link user-info">
              <el-avatar size="small">张</el-avatar>
              <span class="user-name">张教授</span>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>个人中心</el-dropdown-item>
                <el-dropdown-item>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import { Menu, Search } from '@element-plus/icons-vue'

const route = useRoute()
const search = ref('')

const activeMenu = computed(() => route.path)
const currentTitle = computed(() => route.meta.title || '毕业设计辅助管理系统')
</script>

<style scoped>
.app-layout {
  height: 100vh;
}

.aside {
  background: #1f55d0;
  color: #fff;
  display: flex;
  flex-direction: column;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 600;
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
}

.side-menu {
  border-right: none;
  flex: 1;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}

.header-left {
  display: flex;
  align-items: center;
}

.page-title {
  margin-left: 12px;
  font-size: 18px;
  font-weight: 500;
}

.header-right {
  display: flex;
  align-items: center;
}

.header-search {
  width: 240px;
  margin-right: 16px;
}

.user-info {
  display: inline-flex;
  align-items: center;
  cursor: pointer;
}

.user-name {
  margin-left: 6px;
}

.main {
  background: #f5f7fa;
  padding: 16px;
}
</style>
