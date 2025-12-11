<template>
  <div class="page notification-page">
    <!-- 顶部欢迎 / 提示 -->
    <el-card class="banner-card" shadow="never">
      <div class="banner-inner">
        <div class="banner-left">
          <div class="weather-icon">🔔</div>
          <div>
            <div class="banner-title">课题申报通知管理</div>
            <div class="banner-sub">
              教科办可发布“初次申报 / 二次补申报”通知，设置时间范围并自动开启教师申报权限。
            </div>
          </div>
        </div>
      </div>
    </el-card>

    <el-row :gutter="16" class="mt-16">
      <!-- 左侧：通知编辑表单 -->
      <el-col :span="10">
        <el-card shadow="never">
          <template #header>
            <div class="card-header">
              <span>{{ form.id ? '编辑课题申报通知' : '新建课题申报通知' }}</span>
              <el-tag v-if="form.status" size="small" :type="statusTagType(form.status)">
                {{ form.status }}
              </el-tag>
            </div>
          </template>

          <el-form
            ref="formRef"
            :model="form"
            :rules="rules"
            label-width="90px"
            size="small"
          >
            <el-form-item label="通知标题" prop="title">
              <el-input
                v-model="form.title"
                maxlength="50"
                show-word-limit
                placeholder="例如：2025 届毕业设计课题申报通知"
              />
            </el-form-item>

            <el-form-item label="通知类型" prop="type">
              <el-select v-model="form.type" placeholder="请选择">
                <el-option label="初次申报" value="初次申报" />
                <el-option label="二次补申报" value="二次补申报" />
              </el-select>
            </el-form-item>

            <el-form-item label="面向专业" prop="majors">
              <el-select
                v-model="form.majors"
                multiple
                filterable
                placeholder="请选择面向专业"
              >
                <el-option
                  v-for="m in majorOptions"
                  :key="m"
                  :label="m"
                  :value="m"
                />
              </el-select>
            </el-form-item>

            <el-form-item label="接收教师" prop="teacherScope">
              <el-input
                v-model="form.teacherScope"
                placeholder="例如：计算机学院全部指导教师 / 指定教师列表"
              />
            </el-form-item>

            <el-form-item label="申报时间" required>
              <el-date-picker
                v-model="timeRange"
                type="datetimerange"
                value-format="YYYY-MM-DD HH:mm"
                range-separator="至"
                start-placeholder="开始时间"
                end-placeholder="截止时间"
              />
            </el-form-item>

            <el-form-item label="申报要求" prop="requirement">
              <el-input
                v-model="form.requirement"
                type="textarea"
                :rows="4"
                placeholder="填写申报要求、材料说明等"
              />
            </el-form-item>

            <el-form-item label="通知模板">
              <el-select
                v-model="selectedTemplate"
                placeholder="选择模板快速填充"
                clearable
                @change="applyTemplate"
              >
                <el-option
                  v-for="tpl in templates"
                  :key="tpl.value"
                  :label="tpl.label"
                  :value="tpl.value"
                />
              </el-select>
            </el-form-item>

            <el-form-item label="自动提醒">
              <el-switch
                v-model="form.autoRemind"
                active-text="开启"
                inactive-text="关闭"
              />
            </el-form-item>

            <el-form-item>
              <el-button type="primary" :loading="saving" @click="handleSave('draft')">
                保存草稿
              </el-button>
              <el-button type="success" :loading="saving" @click="handleSave('publish')">
                发布通知
              </el-button>
              <el-button @click="handleReset">重置</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <!-- 右侧：历史通知列表 -->
      <el-col :span="14">
        <el-card shadow="never">
          <template #header>
            <div class="card-header">
              <span>历史通知列表</span>
              <div>
                <el-button size="small" @click="handleExport">
                  导出列表
                </el-button>
              </div>
            </div>
          </template>

          <el-form inline size="small" class="search-form">
            <el-form-item label="关键字">
              <el-input
                v-model="query.keyword"
                placeholder="标题 / 要求说明"
                clearable
              />
            </el-form-item>
            <el-form-item label="类型">
              <el-select
                v-model="query.type"
                placeholder="全部"
                clearable
                style="width: 120px"
              >
                <el-option label="初次申报" value="初次申报" />
                <el-option label="二次补申报" value="二次补申报" />
              </el-select>
            </el-form-item>
            <el-form-item label="状态">
              <el-select
                v-model="query.status"
                placeholder="全部"
                clearable
                style="width: 120px"
              >
                <el-option label="草稿" value="草稿" />
                <el-option label="已发布" value="已发布" />
                <el-option label="已撤回" value="已撤回" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="fetchNotifications">查询</el-button>
              <el-button @click="resetQuery">清空</el-button>
            </el-form-item>
          </el-form>

          <el-table
            :data="filteredNotifications"
            size="small"
            border
            style="margin-top: 8px"
            highlight-current-row
          >
            <el-table-column prop="title" label="通知标题" min-width="220" />
            <el-table-column prop="type" label="类型" width="90" />
            <el-table-column label="状态" width="90">
              <template #default="{ row }">
                <el-tag :type="statusTagType(row.status)" size="small">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="时间范围" min-width="200">
              <template #default="{ row }">
                <div>{{ row.startTime }} ~</div>
                <div>{{ row.endTime }}</div>
              </template>
            </el-table-column>
            <el-table-column prop="majors" label="面向专业" min-width="160">
              <template #default="{ row }">
                <el-tag
                  v-for="m in row.majors"
                  :key="m"
                  size="small"
                  effect="plain"
                  class="tag-item"
                >
                  {{ m }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="publisher" label="发布人" width="90" />
            <el-table-column prop="publishTime" label="发布时间" width="150" />
            <el-table-column prop="readRate" label="阅读率" width="90" />

            <el-table-column label="操作" width="230" fixed="right">
              <template #default="{ row }">
                <el-button
                  type="primary"
                  link
                  @click="editNotification(row)"
                >
                  编辑
                </el-button>
                <el-button type="primary" link @click="copyNotification(row)">
                  复制
                </el-button>
                <el-button
                  v-if="row.status === '草稿'"
                  type="success"
                  link
                  @click="publishNotificationRow(row)"
                >
                  发布
                </el-button>
                <el-button
                  v-else-if="row.status === '已发布'"
                  type="danger"
                  link
                  :disabled="isStarted(row)"
                  @click="revokeNotificationRow(row)"
                >
                  撤回
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  listNotices,
  publishNotice,
  revokeNotice,
  saveNotice
} from '../api/notices'

const formRef = ref()
const loading = ref(false)
const saving = ref(false)

// 下拉选项
const majorOptions = [
  '计算机科学与技术',
  '软件工程',
  '信息安全',
  '人工智能',
  '数据科学与大数据技术'
]

const templates = [
  {
    value: 'first',
    label: '初次申报模板',
    title: '2025 届毕业设计课题初次申报通知',
    requirement:
      '请各位指导教师根据教学计划和学生人数，合理申报毕业设计课题，确保课题难度适中、工作量合理。'
  },
  {
    value: 'second',
    label: '二次补申报模板',
    title: '2025 届毕业设计课题二次补申报通知',
    requirement:
      '为满足学生选题需求，现开启毕业设计课题二次补申报，请有新增课题的教师按要求补充申报。'
  }
]

// 表单默认值
const emptyForm = () => ({
  id: null,
  title: '',
  type: '初次申报',
  majors: [],
  teacherScope: '本学院全部指导教师',
  startTime: '',
  endTime: '',
  requirement: '',
  autoRemind: true,
  status: '草稿',
  publisher: '教科办'
})

const form = reactive(emptyForm())
const timeRange = ref([]) // [start, end]
const selectedTemplate = ref('')

// 校验规则
const rules = {
  title: [{ required: true, message: '请输入通知标题', trigger: 'blur' }],
  type: [{ required: true, message: '请选择通知类型', trigger: 'change' }],
  majors: [
    { required: true, message: '请选择面向专业', trigger: 'change' }
  ],
  teacherScope: [
    { required: true, message: '请输入接收教师范围', trigger: 'blur' }
  ],
  requirement: [
    { required: true, message: '请输入申报要求说明', trigger: 'blur' }
  ]
}

const notifications = ref([])

// 查询条件
const query = reactive({
  keyword: '',
  type: '',
  status: ''
})

const filteredNotifications = computed(() => {
  return notifications.value.filter(n => {
    const kw = query.keyword.trim()
    const okKw =
      !kw ||
      n.title.includes(kw) ||
      (n.requirement && n.requirement.includes(kw))
    const okType = !query.type || n.type === query.type
    const okStatus = !query.status || n.status === query.status
    return okKw && okType && okStatus
  })
})

// 状态对应 tag 颜色
const statusTagType = status => {
  if (status === '已发布') return 'success'
  if (status === '已撤回') return 'info'
  return 'warning' // 草稿
}

const fmt = val => {
  if (!val) return ''
  const d = new Date(val)
  if (Number.isNaN(d.getTime())) return val
  const pad = n => n.toString().padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(
    d.getHours()
  )}:${pad(d.getMinutes())}`
}

// 是否已经到开始时间（已开始则不能撤回）
const isStarted = row => {
  if (!row.startTime) return false
  const now = new Date()
  return now >= new Date(row.startTime.replace(/-/g, '/'))
}

// 应用模板
const applyTemplate = val => {
  const tpl = templates.find(t => t.value === val)
  if (!tpl) return
  form.title = tpl.title
  form.requirement = tpl.requirement
}

const syncFormTime = () => {
  if (timeRange.value?.length === 2) {
    form.startTime = timeRange.value[0]
    form.endTime = timeRange.value[1]
  }
}

const fetchNotifications = async () => {
  loading.value = true
  try {
    const list = await listNotices({
      keyword: query.keyword,
      type: query.type,
      status: query.status
    })
    notifications.value = list.map(item => ({
      ...item,
      startTime: fmt(item.startTime),
      endTime: fmt(item.endTime),
      publishTime: fmt(item.publishTime),
      readRate: item.status === '已发布' ? item.readRate || '0%' : '--'
    }))
  } catch (err) {
    console.error(err)
    ElMessage.error('获取通知列表失败')
  } finally {
    loading.value = false
  }
}

// 保存或发布（mode: draft/publish）
const handleSave = async mode => {
  await formRef.value.validate().catch(() => {
    ElMessage.error('请先填写完整的通知信息')
    return Promise.reject()
  })

  if (!timeRange.value || timeRange.value.length !== 2) {
    ElMessage.error('请选择申报开始时间和截止时间')
    return
  }

  syncFormTime()

  if (new Date(form.endTime) <= new Date(form.startTime)) {
    ElMessage.error('申报截止时间必须晚于开始时间')
    return
  }

  // 如果是发布，需要检查同一时间段不能存在多个已发布的同类型通知
  if (mode === 'publish') {
    const overlap = notifications.value.some(n => {
      if (n.id === form.id) return false
      if (n.type !== form.type) return false
      if (n.status !== '已发布') return false
      const startA = new Date(n.startTime.replace(/-/g, '/'))
      const endA = new Date(n.endTime.replace(/-/g, '/'))
      const startB = new Date(form.startTime.replace(/-/g, '/'))
      const endB = new Date(form.endTime.replace(/-/g, '/'))
      return startA <= endB && startB <= endA
    })
    if (overlap) {
      ElMessage.error('同一时间段内不能存在多个有效的同类型通知')
      return
    }
  }

  saving.value = true
  try {
    const status = mode === 'publish' ? '已发布' : '草稿'
    const saved = await saveNotice({ ...form, status })
    Object.assign(form, saved)
    await fetchNotifications()
    ElMessage.success(mode === 'publish' ? '通知已成功发布' : '草稿已保存')
  } catch (err) {
    console.error(err)
    ElMessage.error('保存失败，请重试')
  } finally {
    saving.value = false
  }
}

// 重置为新建
const handleReset = () => {
  Object.assign(form, emptyForm())
  timeRange.value = []
  selectedTemplate.value = ''
}

// 编辑
const editNotification = row => {
  Object.assign(form, row)
  timeRange.value = [row.startTime, row.endTime]
}

// 复制
const copyNotification = row => {
  handleReset()
  Object.assign(form, {
    ...row,
    id: null,
    title: row.title + '（复制）',
    status: '草稿'
  })
  timeRange.value = [row.startTime, row.endTime]
}

// 单行发布
const publishNotificationRow = row => {
  ElMessageBox.confirm('确定要发布该通知吗？', '提示', {
    type: 'warning'
  })
    .then(async () => {
      await publishNotice(row.id)
      await fetchNotifications()
      ElMessage.success('通知已成功发布')
    })
    .catch(() => {})
}

// 撤回
const revokeNotificationRow = row => {
  if (isStarted(row)) {
    ElMessage.error('申报已开始，不能撤回该通知')
    return
  }
  ElMessageBox.confirm('确定要撤回该通知吗？', '提示', { type: 'warning' })
    .then(async () => {
      await revokeNotice(row.id)
      await fetchNotifications()
      ElMessage.success('通知已撤回')
    })
    .catch(() => {})
}

// 导出（前端示例）
const handleExport = () => {
  ElMessage.info('前端示例：这里可以对接导出 Excel/PDF 接口')
}

// 查询区
const resetQuery = () => {
  query.keyword = ''
  query.type = ''
  query.status = ''
  fetchNotifications()
}

onMounted(() => {
  fetchNotifications()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-form {
  margin-bottom: 4px;
}

.tag-item {
  margin-right: 4px;
  margin-bottom: 2px;
}
</style>
