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
        <el-form-item label="学年学期">
          <el-select v-model="filter.term" style="width: 160px" clearable>
            <el-option label="2024-2025 学年 第二学期" value="2024-2" />
          </el-select>
        </el-form-item>
        <el-form-item label="学院">
          <el-select v-model="filter.college" clearable style="width: 140px">
            <el-option label="计算机学院" value="计算机学院" />
          </el-select>
        </el-form-item>
        <el-form-item label="专业">
          <el-select v-model="filter.major" clearable style="width: 140px">
            <el-option label="软件工程" value="软件工程" />
            <el-option label="计算机科学与技术" value="计算机科学与技术" />
          </el-select>
        </el-form-item>
        <el-form-item label="班级">
          <el-input
            v-model="filter.className"
            placeholder="例如：软工 2101"
            clearable
          />
        </el-form-item>
        <el-form-item label="指导教师">
          <el-input
            v-model="filter.teacher"
            placeholder="教师姓名"
            clearable
          />
        </el-form-item>
        <el-form-item label="学号/姓名">
          <el-input
            v-model="filter.keyword"
            placeholder="学号或姓名"
            clearable
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
        <el-form-item label="是否通过">
          <el-select v-model="filter.passed" clearable style="width: 120px">
            <el-option label="全部" value="" />
            <el-option label="通过" value="通过" />
            <el-option label="未通过" value="未通过" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="filter.status" clearable style="width: 120px">
            <el-option label="全部" value="" />
            <el-option label="暂存" value="暂存" />
            <el-option label="待审核" value="待审核" />
            <el-option label="已发布" value="已发布" />
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary">查询</el-button>
          <el-button @click="resetFilter">清空</el-button>
          <el-button>导出当前列表</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 成绩列表 + 操作 -->
    <el-card shadow="never" class="mt-16">
      <template #header>
        <div class="card-header">
          <span>成绩列表（前端模拟数据）</span>
          <div>
            <el-button size="small" @click="batchSetStatus('待审核')">
              批量提交审核
            </el-button>
            <el-button size="small" @click="batchSetStatus('已发布')">
              批量发布（教务办）
            </el-button>
          </div>
        </div>
      </template>

      <el-table
        :data="filteredScores"
        border
        size="small"
        @selection-change="onSelectionChange"
      >
        <el-table-column type="selection" width="40" />
        <el-table-column prop="studentId" label="学号" width="90" />
        <el-table-column prop="studentName" label="姓名" width="80" />
        <el-table-column prop="major" label="专业" width="120" />
        <el-table-column prop="className" label="班级" width="100" />
        <el-table-column prop="teacher" label="指导教师" width="100" />

        <el-table-column label="过程成绩" width="90" prop="processScore" />
        <el-table-column label="开题" width="70" prop="openingScore" />
        <el-table-column label="中期" width="70" prop="midScore" />
        <el-table-column label="论文" width="70" prop="thesisScore" />
        <el-table-column label="答辩" width="70" prop="defenseScore" />

        <el-table-column label="总评" width="70">
          <template #default="{ row }">
            {{ calcTotal(row).toFixed(1) }}
          </template>
        </el-table-column>
        <el-table-column label="等级" width="70">
          <template #default="{ row }">
            {{ calcLevel(calcTotal(row)) }}
          </template>
        </el-table-column>
        <el-table-column label="是否通过" width="80">
          <template #default="{ row }">
            <el-tag
              :type="calcTotal(row) >= 60 ? 'success' : 'danger'"
              size="small"
            >
              {{ calcTotal(row) >= 60 ? '通过' : '未通过' }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="status" label="状态" width="80">
          <template #default="{ row }">
            <el-tag v-if="row.status === '暂存'" size="small">暂存</el-tag>
            <el-tag
              v-else-if="row.status === '待审核'"
              type="warning"
              size="small"
            >
              待审核
            </el-tag>
            <el-tag
              v-else-if="row.status === '已发布'"
              type="success"
              size="small"
            >
              已发布
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="操作" fixed="right" width="180">
          <template #default="{ row }">
            <el-button type="primary" link @click="openEditDialog(row)">
              录入/修改
            </el-button>
            <el-button type="primary" link @click="viewDetail(row)">
              查看
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
        <el-form-item label="学生">
          <span>{{ current.studentId }} {{ current.studentName }}</span>
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
          <el-input-number v-model="current.midScore" :min="0" :max="100" />
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
        <el-form-item label="教师评语">
          <el-input
            v-model="current.comment"
            type="textarea"
            :rows="3"
            placeholder="教师综合评语"
          />
        </el-form-item>
        <el-form-item label="答辩意见">
          <el-input
            v-model="current.defenseComment"
            type="textarea"
            :rows="2"
            placeholder="答辩小组意见（前端示例）"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="editVisible = false">取消</el-button>
        <el-button type="primary" @click="saveCurrent('暂存')">
          保存暂存
        </el-button>
        <el-button type="success" @click="saveCurrent('待审核')">
          提交审核
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'

// 查询条件
const filter = reactive({
  term: '2024-2',
  college: '计算机学院',
  major: '',
  className: '',
  teacher: '',
  keyword: '',
  range: '',
  passed: '',
  status: ''
})

// 成绩数据（前端假数据）
const scores = ref([
  {
    id: 1,
    studentId: '20210001',
    studentName: '张三',
    major: '软件工程',
    className: '软工 2101',
    teacher: '李老师',
    processScore: 85,
    openingScore: 90,
    midScore: 88,
    thesisScore: 86,
    defenseScore: 87,
    status: '暂存',
    comment: '',
    defenseComment: ''
  },
  {
    id: 2,
    studentId: '20210002',
    studentName: '李四',
    major: '软件工程',
    className: '软工 2101',
    teacher: '李老师',
    processScore: 76,
    openingScore: 80,
    midScore: 78,
    thesisScore: 82,
    defenseScore: 79,
    status: '待审核',
    comment: '',
    defenseComment: ''
  },
  {
    id: 3,
    studentId: '20210003',
    studentName: '王五',
    major: '计算机科学与技术',
    className: '计科 2102',
    teacher: '王老师',
    processScore: 92,
    openingScore: 95,
    midScore: 93,
    thesisScore: 94,
    defenseScore: 96,
    status: '已发布',
    comment: '表现优秀',
    defenseComment: '答辩表现出色'
  }
])

// 计算总评（简单按权重：过程 20%、开题 10%、中期 10%、论文 30%、答辩 30%）
const calcTotal = row => {
  const p = row.processScore ?? 0
  const o = row.openingScore ?? 0
  const m = row.midScore ?? 0
  const t = row.thesisScore ?? 0
  const d = row.defenseScore ?? 0
  return p * 0.2 + o * 0.1 + m * 0.1 + t * 0.3 + d * 0.3
}

const calcLevel = total => {
  if (total >= 90) return '优'
  if (total >= 80) return '良'
  if (total >= 70) return '中'
  if (total >= 60) return '及格'
  return '不及格'
}

// 过滤后的列表
const filteredScores = computed(() => {
  return scores.value.filter(s => {
    const kw = filter.keyword.trim()
    const okKw =
      !kw ||
      s.studentId.includes(kw) ||
      s.studentName.includes(kw)

    const okMajor = !filter.major || s.major === filter.major
    const okClass =
      !filter.className || s.className.includes(filter.className)
    const okTeacher =
      !filter.teacher || s.teacher.includes(filter.teacher)

    // 成绩段
    let okRange = true
    if (filter.range) {
      const total = calcTotal(s)
      const [min, max] = filter.range.split('-').map(Number)
      okRange = total >= min && total <= max
    }

    // 是否通过
    let okPassed = true
    if (filter.passed === '通过') {
      okPassed = calcTotal(s) >= 60
    } else if (filter.passed === '未通过') {
      okPassed = calcTotal(s) < 60
    }

    let okStatus = true
    if (filter.status) {
      okStatus = s.status === filter.status
    }

    return okKw && okMajor && okClass && okTeacher && okRange && okPassed && okStatus
  })
})

// 统计信息
const stats = computed(() => {
  if (!filteredScores.value.length) {
    return {
      count: 0,
      avg: 0,
      max: 0,
      min: 0,
      passRate: 0,
      excellentRate: 0
    }
  }
  const totals = filteredScores.value.map(calcTotal)
  const sum = totals.reduce((a, b) => a + b, 0)
  const count = totals.length
  const avg = sum / count
  const max = Math.max(...totals)
  const min = Math.min(...totals)
  const passCount = totals.filter(t => t >= 60).length
  const excellentCount = totals.filter(t => t >= 90).length
  return {
    count,
    avg,
    max,
    min,
    passRate: passCount / count,
    excellentRate: excellentCount / count
  }
})

const resetFilter = () => {
  filter.major = ''
  filter.className = ''
  filter.teacher = ''
  filter.keyword = ''
  filter.range = ''
  filter.passed = ''
  filter.status = ''
}

// 多选
const selectedRows = ref([])
const onSelectionChange = rows => {
  selectedRows.value = rows
}

// 批量设置状态（模拟教务办审核/发布）
const batchSetStatus = status => {
  if (!selectedRows.value.length) {
    ElMessage.warning('请先勾选需要操作的记录')
    return
  }
  selectedRows.value.forEach(r => {
    r.status = status
  })
  ElMessage.success(`已批量设置为【${status}】`)
}

// 录入对话框
const editVisible = ref(false)
const current = ref(null)

const openEditDialog = row => {
  current.value = row
  editVisible.value = true
}

const saveCurrent = status => {
  if (!current.value) return
  current.value.status = status
  editVisible.value = false
  ElMessage.success(status === '暂存' ? '成绩已暂存' : '成绩已提交审核')
}

// 查看详情：这里只是简单提示
const viewDetail = row => {
  const total = calcTotal(row).toFixed(1)
  ElMessage.info(
    `【${row.studentName}】总评：${total}，等级：${calcLevel(total)}，状态：${row.status}`
  )
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
