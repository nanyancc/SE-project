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
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { listTopics } from '../api/topics'

const loading = ref(false)
const groups = ref([])

// 从后端获取课题数据并按专业方向分组统计
const fetchGroups = async () => {
  loading.value = true
  try {
    // 获取全部课题
    const { items } = await listTopics({ limit: 200 })
    
    // 按专业方向分组统计
    const groupMap = {}
    items.forEach(topic => {
      const major = topic.majorLimit || '未指定专业'
      if (!groupMap[major]) {
        groupMap[major] = {
          id: Object.keys(groupMap).length + 1,
          name: `${major}审批组`,
          major,
          leader: '待分配',
          memberCount: 1,
          total: 0,
          pending: 0,
          approved: 0
        }
      }
      groupMap[major].total++
      if (topic.auditStatus === '待审核') {
        groupMap[major].pending++
      } else if (topic.auditStatus === '审核通过') {
        groupMap[major].approved++
      }
    })
    
    // 转换为数组并计算进度
    groups.value = Object.values(groupMap).map(g => ({
      ...g,
      pendingTopics: g.pending,
      // 完成度 = 已处理数量 / 总数量
      progress: g.total > 0 ? Math.round(((g.total - g.pending) / g.total) * 100) : 0,
      status: g.pending > 0 ? '活跃' : '已完成'
    }))
  } catch (err) {
    console.error(err)
    ElMessage.error('获取数据失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchGroups()
})
</script>

<style scoped>
.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
