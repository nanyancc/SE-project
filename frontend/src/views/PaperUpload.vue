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
          <el-input v-model="keyword" placeholder="输入课题名称关键词" />
        </el-form-item>
        <el-form-item label="指导教师">
          <el-input v-model="teacher" placeholder="输入教师姓名" />
        </el-form-item>
        <el-form-item label="课题类型">
          <el-select v-model="type" placeholder="全部">
            <el-option label="全部" value="" />
            <el-option label="研究型" value="研究型" />
            <el-option label="应用型" value="应用型" />
            <el-option label="设计类" value="设计类" />
          </el-select>
        </el-form-item>
        <el-form-item label="课题状态">
          <el-select v-model="status" placeholder="全部">
            <el-option label="全部" value="" />
            <el-option label="可选题" value="可选题" />
            <el-option label="已选满" value="已选满" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary">搜索</el-button>
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

      <el-table :data="filteredList" border style="margin-top: 10px">
        <el-table-column prop="name" label="课题名称" min-width="220" />
        <el-table-column prop="teacher" label="指导教师" width="140" />
        <el-table-column prop="type" label="课题类型" width="100" />
        <el-table-column prop="planCount" label="计划人数" width="90" />
        <el-table-column prop="selectedCount" label="已选人数" width="90" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
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
              名额已满
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
import { computed, ref } from 'vue'

const keyword = ref('')
const teacher = ref('')
const type = ref('')
const status = ref('')
const activeTab = ref('student')

const topics = ref([
  {
    id: 1,
    name: '基于深度学习的图像识别算法研究',
    teacher: '张教授',
    type: '研究型',
    planCount: 3,
    selectedCount: 2,
    status: '可选题'
  },
  {
    id: 2,
    name: '智能图像检索系统的设计与实现',
    teacher: '李教授',
    type: '应用型',
    planCount: 2,
    selectedCount: 2,
    status: '已选满'
  },
  {
    id: 3,
    name: '电子商务平台安全机制研究',
    teacher: '王老师',
    type: '应用型',
    planCount: 2,
    selectedCount: 1,
    status: '可选题'
  },
  {
    id: 4,
    name: '移动端 UI 交互设计研究',
    teacher: '刘老师',
    type: '设计类',
    planCount: 5,
    selectedCount: 3,
    status: '可选题'
  },
  {
    id: 5,
    name: '大数据分析平台搭建与应用',
    teacher: '赵老师',
    type: '应用型',
    planCount: 4,
    selectedCount: 4,
    status: '已选满'
  }
])

const filteredList = computed(() =>
  topics.value.filter(t => {
    const k = keyword.value.trim()
    const tea = teacher.value.trim()
    return (
      (!k || t.name.includes(k)) &&
      (!tea || t.teacher.includes(tea)) &&
      (!type.value || t.type === type.value) &&
      (!status.value || t.status === status.value)
    )
  })
)
</script>

<style scoped>
.mb-16 {
  margin-bottom: 16px;
}
</style>
