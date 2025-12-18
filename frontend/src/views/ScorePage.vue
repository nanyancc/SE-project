<template>
  <div class="page score-page">
    <!-- 顶部卡片 -->
    <el-card class="banner-card" shadow="never">
      <div class="banner-inner">
        <div class="banner-left">
          <div class="weather-icon">📊</div>
          <div>
            <div class="banner-title">毕业设计成绩录入与查询</div>
            <div class="banner-sub">
              指导教师在规定时间内录入成绩，教务办审核后统一发布，学生可按权限查询。
            </div>
          </div>
        </div>
      </div>
    </el-card>

    <el-row :gutter="16" class="mt-16 content-layout">
      <el-col :span="18" class="content-main">
        <!-- 查询条件 -->
        <el-card shadow="never" class="filter-card">
          <template #header>
            <div class="card-header">
              <div>
                <div class="card-title">查询条件</div>
                <div class="card-subtitle">支持多条件组合筛选</div>
              </div>
            </div>
          </template>
          <el-form
            :model="filter"
            label-position="top"
            size="small"
            class="filter-form"
          >
            <el-row :gutter="16">
              <el-col :xs="24" :sm="12" :lg="8">
                <el-form-item label="学号">
                  <el-input
                    v-model="filter.studentId"
                    placeholder="学生ID"
                    clearable
                  />
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12" :lg="8">
                <el-form-item label="课题ID">
                  <el-input
                    v-model="filter.topicId"
                    placeholder="课题ID"
                    clearable
                  />
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12" :lg="8">
                <el-form-item label="成绩段">
                  <el-select
                    v-model="filter.range"
                    clearable
                    placeholder="请选择范围"
                  >
                    <el-option label="全部" value="" />
                    <el-option label="90-100" value="90-100" />
                    <el-option label="80-89" value="80-89" />
                    <el-option label="60-79" value="60-79" />
                    <el-option label="0-59" value="0-59" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12" :lg="8">
                <el-form-item label="等级">
                  <el-select v-model="filter.level" clearable placeholder="全部">
                    <el-option label="全部" value="" />
                    <el-option label="A" value="A" />
                    <el-option label="B" value="B" />
                    <el-option label="C" value="C" />
                    <el-option label="D" value="D" />
                    <el-option label="F" value="F" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :xs="24" :sm="12" :lg="8">
                <el-form-item label="发布状态">
                  <el-select v-model="filter.published" clearable placeholder="全部">
                    <el-option label="全部" :value="''" />
                    <el-option label="暂存" :value="0" />
                    <el-option label="已发布" :value="1" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="24">
                <div class="filter-actions">
                  <el-button @click="resetFilter">清空</el-button>
                  <el-button @click="exportCurrentList">导出当前列表</el-button>
                  <el-button type="primary" @click="fetchScoresData">
                    查询
                  </el-button>
                </div>
              </el-col>
            </el-row>
          </el-form>
        </el-card>

        <!-- 成绩列表 + 操作 -->
        <el-card shadow="never" class="mt-16 score-table-card">
          <template #header>
            <div class="card-header table-header">
              <div>
                <div class="card-title">成绩列表</div>
                <div class="card-subtitle">
                  共 {{ filteredScores.length }} 条记录
                </div>
              </div>
              <div class="table-actions">
                <el-button size="small" @click="batchSetStatus(0)">
                  批量暂存
                </el-button>
                <el-button
                  size="small"
                  type="success"
                  @click="batchSetStatus(1)"
                >
                  批量发布（教务办）
                </el-button>
              </div>
            </div>
          </template>

          <el-table
            :data="filteredScores"
            border
            stripe
            highlight-current-row
            size="small"
            :loading="loading"
            class="score-table"
            @selection-change="onSelectionChange"
          >
            <el-table-column type="selection" width="40" />
            <el-table-column prop="studentId" label="学号" width="80" />
            <el-table-column prop="topicId" label="课题ID" width="80" />

            <el-table-column label="过程成绩" width="70" prop="processScore" />
            <el-table-column label="开题" width="60" prop="openingScore" />
            <el-table-column label="中期" width="60" prop="midtermScore" />
            <el-table-column label="论文" width="60" prop="thesisScore" />
            <el-table-column label="答辩" width="60" prop="defenseScore" />

            <el-table-column label="总评" width="60">
              <template #default="{ row }">
                {{ getTotal(row).toFixed(1) }}
              </template>
            </el-table-column>
            <el-table-column label="等级" width="60">
              <template #default="{ row }">
                {{ row.scoreLevel || calcLevel(getTotal(row)) }}
              </template>
            </el-table-column>
            <el-table-column prop="isPublished" label="发布状态" width="80">
              <template #default="{ row }">
                <el-tag :type="row.isPublished ? 'success' : 'info'" size="small">
                  {{ row.isPublished ? '已发布' : '暂存' }}
                </el-tag>
              </template>
            </el-table-column>

            <el-table-column label="操作" fixed="right" width="80">
              <template #default="{ row }">
                <el-button type="primary" link @click="openEditDialog(row)">
                  修改
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="6" class="stats-col">
        <div class="stats-panel">
          <el-card
            v-for="item in statItems"
            :key="item.label"
            shadow="never"
            class="stats-card"
          >
            <div class="stats-label">{{ item.label }}</div>
            <div class="stats-value">{{ item.value }}</div>
            <div class="stats-desc">{{ item.desc }}</div>
          </el-card>
        </div>
      </el-col>
    </el-row>

    <!-- 录入对话框 -->
    <el-dialog
      v-model="editVisible"
      title="成绩录入 / 修改"
      width="540px"
      destroy-on-close
    >
      <el-form
        v-if="current"
        :model="current"
        label-width="120px"
        size="small"
      >
        <el-form-item label="学生ID">
          <el-input v-model="current.studentId" disabled />
        </el-form-item>
        <el-form-item label="课题ID">
          <el-input v-model="current.topicId" disabled />
        </el-form-item>
        <el-form-item label="过程成绩">
          <el-input-number
            v-model="current.processScore"
            :min="0"
            :max="100"
          />
        </el-form-item>
        <el-form-item label="开题成绩">
          <el-input-number
            v-model="current.openingScore"
            :min="0"
            :max="100"
          />
        </el-form-item>
        <el-form-item label="中期检查成绩">
          <el-input-number v-model="current.midtermScore" :min="0" :max="100" />
        </el-form-item>
        <el-form-item label="论文成绩">
          <el-input-number
            v-model="current.thesisScore"
            :min="0"
            :max="100"
          />
        </el-form-item>
        <el-form-item label="答辩成绩">
          <el-input-number
            v-model="current.defenseScore"
            :min="0"
            :max="100"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="editVisible = false">取消</el-button>
        <el-button type="primary" @click="saveCurrent(0)">保存暂存</el-button>
        <el-button type="success" @click="saveCurrent(1)">发布</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import {
  batchUpdateStatus,
  getScoreStats,
  getScores,
  updateScore
} from '../api/scores'

// 查询条件
const filter = reactive({
  studentId: '',
  topicId: '',
  range: '',
  level: '',
  published: ''
})

const scores = ref([])
const loading = ref(false)
const stats = ref({
  count: 0,
  avg: 0,
  max: 0,
  min: 0,
  passRate: 0,
  excellentRate: 0
})

// 计算总评（简单按权重：过程 20%、开题 10%、中期 10%、论文 30%、答辩 30%）
const calcTotal = row => {
  const p = row.processScore ?? 0
  const o = row.openingScore ?? 0
  const m = row.midtermScore ?? 0
  const t = row.thesisScore ?? 0
  const d = row.defenseScore ?? 0
  return p * 0.2 + o * 0.1 + m * 0.1 + t * 0.3 + d * 0.3
}

const getTotal = row => Number(row.totalScore ?? row.total ?? calcTotal(row))

const calcLevel = totalScore => {
  if (totalScore >= 90) return 'A'
  if (totalScore >= 80) return 'B'
  if (totalScore >= 70) return 'C'
  if (totalScore >= 60) return 'D'
  return 'F'
}

const csvColumns = [
  { label: '学号', getter: row => row.studentId ?? '' },
  { label: '课题ID', getter: row => row.topicId ?? '' },
  { label: '过程成绩', getter: row => row.processScore ?? '' },
  { label: '开题', getter: row => row.openingScore ?? '' },
  { label: '中期', getter: row => row.midtermScore ?? '' },
  { label: '论文', getter: row => row.thesisScore ?? '' },
  { label: '答辩', getter: row => row.defenseScore ?? '' },
  { label: '总评', getter: row => getTotal(row).toFixed(1) },
  {
    label: '等级',
    getter: row => row.scoreLevel || calcLevel(getTotal(row))
  },
  { label: '发布状态', getter: row => (row.isPublished ? '已发布' : '暂存') }
]

// 服务端已过滤，这里保持表格绑定
const filteredScores = computed(() => scores.value)

const formatCsvValue = value => {
  const str = value === null || value === undefined ? '' : String(value)
  const escaped = str.replace(/"/g, '""')
  return `"${escaped}"`
}

const statItems = computed(() => [
  { label: '统计学生数', value: stats.value.count, desc: '已录入学生数' },
  {
    label: '平均分',
    value: stats.value.avg.toFixed(1),
    desc: '当前平均成绩'
  },
  {
    label: '最高 / 最低',
    value: `${stats.value.max.toFixed(1)} / ${stats.value.min.toFixed(1)}`,
    desc: '最高 / 最低分'
  },
  {
    label: '及格率 / 优秀率',
    value: `${(stats.value.passRate * 100).toFixed(1)}% / ${(stats.value.excellentRate * 100).toFixed(1)}%`,
    desc: '达标 / 优秀比例'
  }
])

const fetchStats = async () => {
  try {
    stats.value = await getScoreStats(filter)
  } catch (err) {
    console.error(err)
    ElMessage.error('获取统计信息失败')
  }
}

const fetchScoresData = async () => {
  loading.value = true
  try {
    const { items } = await getScores(filter)
    scores.value = items
  } catch (err) {
    console.error(err)
    ElMessage.error('获取成绩列表失败')
  } finally {
    loading.value = false
  }
  await fetchStats()
}

const resetFilter = () => {
  filter.studentId = ''
  filter.topicId = ''
  filter.range = ''
  filter.level = ''
  filter.published = ''
  fetchScoresData()
}

const exportCurrentList = () => {
  const data = filteredScores.value
  if (!data.length) {
    ElMessage.warning('当前没有数据可导出')
    return
  }
  if (typeof window === 'undefined' || typeof document === 'undefined') {
    ElMessage.error('当前环境不支持导出')
    return
  }

  const header = csvColumns.map(col => formatCsvValue(col.label)).join(',')
  const rows = data.map(row =>
    csvColumns.map(col => formatCsvValue(col.getter(row))).join(',')
  )
  const csvContent = [header, ...rows].join('\n')
  const blob = new Blob(['\ufeff' + csvContent], {
    type: 'text/csv;charset=utf-8;'
  })
  const url = window.URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `scores_${new Date().toISOString().slice(0, 10)}.csv`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  window.URL.revokeObjectURL(url)
  ElMessage.success('导出成功')
}

// 多选
const selectedRows = ref([])
const onSelectionChange = rows => {
  selectedRows.value = rows
}

// 批量设置状态（对接后端）
const batchSetStatus = async isPublished => {
  if (!selectedRows.value.length) {
    ElMessage.warning('请先勾选需要操作的记录')
    return
  }
  try {
    const ids = selectedRows.value.map(r => r.id)
    await batchUpdateStatus(ids, isPublished)
    await fetchScoresData()
    ElMessage.success(isPublished ? '已批量发布' : '已批量暂存')
  } catch (err) {
    console.error(err)
    ElMessage.error('批量更新状态失败')
  }
}

// 录入对话框
const editVisible = ref(false)
const current = ref(null)

const openEditDialog = row => {
  current.value = { ...row }
  editVisible.value = true
}

const saveCurrent = async isPublished => {
  if (!current.value) return
  try {
    const updated = await updateScore(current.value.id, {
      ...current.value,
      isPublished
    })
    const idx = scores.value.findIndex(s => s.id === updated.id)
    if (idx !== -1) {
      scores.value[idx] = updated
    }
    editVisible.value = false
    ElMessage.success(isPublished ? '成绩已发布' : '成绩已暂存')
    await fetchStats()
  } catch (err) {
    console.error(err)
    ElMessage.error('保存失败，请重试')
  }
}

onMounted(() => {
  fetchScoresData()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.card-subtitle {
  margin-top: 4px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.content-layout {
  align-items: stretch;
}

.content-main {
  display: flex;
  flex-direction: column;
}

.filter-card,
.score-table-card,
.stats-card {
  border-radius: 4px;
}

.filter-form .el-form-item {
  margin-bottom: 12px;
}

.filter-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  flex-wrap: wrap;
  padding-top: 8px;
}

.table-header {
  align-items: flex-start;
}

.table-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.score-table {
  font-size: 13px;
}

.stats-col {
  min-height: 100%;
}

.stats-panel {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.stats-card {
  border: 1px solid var(--el-border-color-lighter);
}

.stats-label {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.stats-value {
  margin: 6px 0;
  font-size: 24px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.stats-desc {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

@media (max-width: 992px) {
  .content-layout {
    flex-direction: column;
  }

  .stats-col {
    margin-top: 16px;
  }

  .table-actions {
    width: 100%;
    justify-content: flex-start;
  }
}
</style>
