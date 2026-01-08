<template>
  <div class="page topic-select-page">
    <el-card class="banner-card" shadow="never">
      <div class="banner-inner">
        <div class="banner-left">
          <div class="weather-icon">📚</div>
          <div>
            <div class="banner-title">选题管理</div>
            <div class="banner-sub">管理学生选题、志愿和历史记录</div>
          </div>
        </div>
      </div>
    </el-card>

    <el-card shadow="never" class="mb-16">
      <el-form inline>
        <el-form-item label="课题名称">
          <el-input v-model="keyword" placeholder="输入课题名称关键词" clearable @keyup.enter="fetchData" />
        </el-form-item>
        <el-form-item label="指导教师">
          <el-input v-model="teacher" placeholder="输入教师ID" clearable />
        </el-form-item>
        <el-form-item label="课题类型">
          <el-select v-model="type" placeholder="全部" clearable>
            <el-option label="全部" value="" />
            <el-option label="研究型" value="研究" />
            <el-option label="应用型" value="应用" />
            <el-option label="设计类" value="设计" />
          </el-select>
        </el-form-item>
        <el-form-item label="课题状态">
          <el-select v-model="statusFilter" placeholder="全部">
            <el-option label="全部" value="" />
            <el-option label="可选题" value="可选题" />
            <el-option label="已选满" value="已选满" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData" :loading="loading">搜索</el-button>
          <el-button>选题统计</el-button>
          <el-button>导出报表</el-button>
          <el-button type="primary">发送通知</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card shadow="never">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="学生选题" name="student" />
        <el-tab-pane label="题目总览" name="topic" />
        <el-tab-pane label="志愿调整" name="wish" />
        <el-tab-pane label="申报表管理" name="apply" />
        <el-tab-pane label="历史记录" name="history" />
      </el-tabs>

      <el-table :data="tableData" border style="margin-top: 10px" v-loading="loading">
        <el-table-column prop="name" label="课题名称" min-width="220" />
        <el-table-column prop="teacher" label="指导教师" width="140" />
        <el-table-column prop="type" label="课题类型" width="100" />
        <el-table-column prop="planCount" label="计划人数" width="90" />
        <el-table-column prop="selectedCount" label="已选人数" width="90" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <!-- 状态标签显示逻辑 -->
            <el-tag
              v-if="row.status === '可选题'"
              type="success"
              size="small"
            >
              可选题
            </el-tag>
            <el-tag
              v-else
              type="warning"
              size="small"
            >
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default>
            <el-button type="primary" link>选题明细</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const keyword = ref('')
const teacher = ref('')
const type = ref('')
const statusFilter = ref('') // 前端筛选“可选题/已选满”用
const activeTab = ref('student')
const loading = ref(false)
const tableData = ref([])

const fetchData = async () => {
  loading.value = true
  try {
    // 1. 构造请求参数
    const params = {
      keyword: keyword.value || undefined,
      teacherId: teacher.value || undefined,
      type: type.value || undefined,
      publishStatus: '1', // 【核心修改】强制只向后端请求“审核通过”的数据
      limit: 100
    }

    // 2. 发起请求
    const apiBase = import.meta.env.VITE_API_BASE || '/api'
    const res = await axios.get(`${apiBase}/extra/topics`, { params })

    if (res.data && res.data.items) {
      // 3. 数据处理与状态模拟
      const rawItems = res.data.items.map(item => {
        // 【随机模拟】因为后端还没做选课人数统计，这里随机生成一个“已选人数”
        // 逻辑：生成一个 0 到 max_students 之间的随机数
        const max = item.max_students
        // 让“可选题”出现的概率大一点 (70%概率未满)
        const isFull = Math.random() > 0.7 
        const fakeSelected = isFull ? max : Math.floor(Math.random() * max)
        
        // 决定前端显示的状态文字
        const displayStatus = (fakeSelected >= max) ? '已选满' : '可选题'

        return {
          id: item.id,
          name: item.topic_name,
          teacher: `教师ID: ${item.teacher_id}`,
          type: item.topic_type,
          planCount: max,
          selectedCount: fakeSelected, // 使用模拟数据
          status: displayStatus        // 映射后的状态
        }
      })

      // 4. 前端二次过滤（处理页面上那个“课题状态”下拉框）
      // 因为后端我们强制查了“审核通过”，页面上的下拉框现在用来筛选“可选题”还是“已选满”
      if (statusFilter.value) {
        tableData.value = rawItems.filter(item => item.status === statusFilter.value)
      } else {
        tableData.value = rawItems
      }
    }
  } catch (error) {
    console.error('API Error:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.mb-16 {
  margin-bottom: 16px;
}
/* 保持原有样式 */
</style>