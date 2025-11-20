<template>
  <div class="page topic-review-page">
    <el-card class="banner-card" shadow="never">
      <div class="banner-inner">
        <div class="banner-left">
          <div class="weather-icon">📝</div>
          <div>
            <div class="banner-title">课题审批</div>
            <div class="banner-sub">管理审批组和课题审批进度</div>
          </div>
        </div>
      </div>
    </el-card>

    <el-card shadow="never">
      <template #header>
        <div class="table-header">
          <span>审批批次管理</span>
          <el-button type="primary" size="small">创建审批组</el-button>
        </div>
      </template>

      <el-table :data="groups" border>
        <el-table-column prop="name" label="审批组名称" min-width="160" />
        <el-table-column prop="major" label="专业方向" width="120" />
        <el-table-column prop="leader" label="组长" width="120" />
        <el-table-column prop="memberCount" label="成员数量" width="100" />
        <el-table-column prop="pendingTopics" label="待审核课题" width="110" />
        <el-table-column label="审批完成度" width="180">
          <template #default="{ row }">
            <el-progress :percentage="row.progress" :stroke-width="8" />
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag
              v-if="row.status === '活跃'"
              type="success"
              size="small"
            >
              活跃
            </el-tag>
            <el-tag
              v-else
              type="info"
              size="small"
            >
              已完成
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="140">
          <template #default>
            <el-button type="primary" link>查看</el-button>
            <el-button type="primary" link>编辑</el-button>
            <el-button type="danger" link>删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
const groups = [
  {
    id: 1,
    name: '计算机科学审批一组',
    major: '计算机科学',
    leader: '李教授',
    memberCount: 5,
    pendingTopics: 12,
    progress: 75,
    status: '活跃'
  },
  {
    id: 2,
    name: '人工智能审批组',
    major: '人工智能',
    leader: '王教授',
    memberCount: 4,
    pendingTopics: 8,
    progress: 60,
    status: '活跃'
  },
  {
    id: 3,
    name: '数据科学审批组',
    major: '数据科学',
    leader: '张教授',
    memberCount: 6,
    pendingTopics: 5,
    progress: 85,
    status: '活跃'
  },
  {
    id: 4,
    name: '网络安全审批组',
    major: '网络安全',
    leader: '刘明',
    memberCount: 3,
    pendingTopics: 0,
    progress: 100,
    status: '已完成'
  }
]
</script>

<style scoped>
.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
