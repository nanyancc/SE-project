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

    <!-- 查询条件 -->
    <el-card shadow="never" class="mt-16">
      <el-form :inline="true" :model="filter" size="small">
        <el-form-item label="学号">
          <el-input
            v-model="filter.studentId"
            placeholder="学生ID"
            clearable
            style="width: 160px"
          />
        </el-form-item>
        <el-form-item label="课题ID">
          <el-input
            v-model="filter.topicId"
            placeholder="课题ID"
            clearable
            style="width: 160px"
          />
        </el-form-item>
        <el-form-item label="成绩段">
          <el-select v-model="filter.range" clearable style="width: 120px">
            <el-option label="全部" value="" />
            <el-option label="90-100" value="90-100" />
            <el-option label="80-89" value="80-89" />
            <el-option label="60-79" value="60-79" />
            <el-option label="0-59" value="0-59" />
          </el-select>
        </el-form-item>
        <el-form-item label="等级">
          <el-select v-model="filter.level" clearable style="width: 120px">
            <el-option label="全部" value="" />
            <el-option label="A" value="A" />
            <el-option label="B" value="B" />
            <el-option label="C" value="C" />
            <el-option label="D" value="D" />
            <el-option label="F" value="F" />
          </el-select>
        </el-form-item>
        <el-form-item label="发布状态">
          <el-select v-model="filter.published" clearable style="width: 120px">
            <el-option label="全部" :value="''" />
            <el-option label="暂存" :value="0" />
            <el-option label="已发布" :value="1" />
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="fetchScoresData">查询</el-button>
          <el-button @click="resetFilter">清空</el-button>
          <el-button>导出当前列表</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 成绩列表 + 操作 -->
    <el-card shadow="never" class="mt-16">
      <template #header>
        <div class="card-header">
          <span>成绩列表</span>
          <div>
            <el-button size="small" @click="batchSetStatus(0)">
              批量暂存
            </el-button>
            <el-button size="small" @click="batchSetStatus(1)">
              批量发布（教务办）
            </el-button>
          </div>
        </div>
      </template>

      <el-table
        :data="filteredScores"
        border
        size="small"
        :loading="loading"
        @selection-change="onSelectionChange"
      >
        <el-table-column type="selection" width="40" />
        <el-table-column prop="studentId" label="学号" width="90" />
        <el-table-column prop="topicId" label="课题ID" width="90" />

        <el-table-column label="过程成绩" width="90" prop="processScore" />
        <el-table-column label="开题" width="70" prop="openingScore" />
        <el-table-column label="中期" width="70" prop="midtermScore" />
        <el-table-column label="论文" width="70" prop="thesisScore" />
        <el-table-column label="答辩" width="70" prop="defenseScore" />

        <el-table-column label="总评" width="70">
          <template #default="{ row }">
            {{ getTotal(row).toFixed(1) }}
          </template>
        </el-table-column>
        <el-table-column label="等级" width="70">
          <template #default="{ row }">
            {{ row.scoreLevel || calcLevel(getTotal(row)) }}
          </template>
        </el-table-column>
        <el-table-column prop="isPublished" label="发布状态" width="90">
          <template #default="{ row }">
            <el-tag :type="row.isPublished ? 'success' : 'info'" size="small">
              {{ row.isPublished ? '已发布' : '暂存' }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="操作" fixed="right" width="120">
          <template #default="{ row }">
            <el-button type="primary" link @click="openEditDialog(row)">
              录入/修改
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 统计信息 -->
    <el-row :gutter="16" class="mt-16">
      <el-col :span="6">
        <el-card shadow="never">
          <div>统计学生数</div>
          <h3>{{ stats.count }}</h3>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="never">
          <div>平均分</div>
          <h3>{{ stats.avg.toFixed(1) }}</h3>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="never">
          <div>最高 / 最低</div>
          <h3>{{ stats.max.toFixed(1) }} / {{ stats.min.toFixed(1) }}</h3>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="never">
          <div>及格率 / 优秀率</div>
          <h3>
            {{ (stats.passRate * 100).toFixed(1) }}% /
            {{ (stats.excellentRate * 100).toFixed(1) }}%
          </h3>
        </el-card>
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

// 服务端已过滤，这里保持表格绑定
const filteredScores = computed(() => scores.value)

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
</style>
