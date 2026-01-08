<template>
  <div class="page midterm-page">
    <el-card class="banner-card" shadow="never">
      <div class="banner-inner">
        <div class="banner-left">
          <div class="weather-icon">🕒</div>
          <div>
            <div class="banner-title">中期检查</div>
            <div class="banner-sub">选择学生并填写中期检查信息</div>
          </div>
        </div>
      </div>
    </el-card>

    <el-row :gutter="20">
      <el-col :span="16">
        <el-card shadow="never" class="mb-16">
          <template #header>
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span>选择学生</span>
              <el-input
                v-model="searchKeyword"
                placeholder="搜索学生姓名/学号"
                style="width: 200px"
                clearable
                @keyup.enter="loadStudents"
                @clear="loadStudents"
              >
                <template #suffix>
                  <el-icon style="cursor: pointer" @click="loadStudents"><Search /></el-icon>
                </template>
              </el-input>
            </div>
          </template>

          <el-table :data="students" border v-loading="loadingStudents">
            <el-table-column type="index" label="序号" width="60" />
            <el-table-column prop="name" label="姓名" width="100" />
            <el-table-column prop="userCode" label="学号" width="120" />
            <el-table-column prop="topicName" label="课题名称">
              <template #default="{ row }">
                {{ row.topicName || '未选题' }}
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="100">
              <template #default="{ row }">
                <el-button type="primary" link @click="selectStudent(row)">
                  选择
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <div class="text-muted" style="margin-top: 8px">
            共 {{ students.length }} 条记录
          </div>
        </el-card>

        <el-card shadow="never">
          <template #header>
            <span>填写中期检查</span>
          </template>

          <p class="mb-16">
            当前选择学生：
            <strong>{{ currentStudent ? currentStudent.name : '未选择' }}</strong>
          </p>

          <el-form :model="form" label-width="120px" label-position="left">
            <el-form-item label="已完成内容">
              <el-input
                v-model="form.completedContent"
                type="textarea"
                :rows="3"
                placeholder="填写当前已完成工作"
              />
            </el-form-item>
            <el-form-item label="遇到的问题">
              <el-input
                v-model="form.problems"
                type="textarea"
                :rows="2"
                placeholder="列出主要问题"
              />
            </el-form-item>
            <el-form-item label="下一步计划">
              <el-input
                v-model="form.nextPlan"
                type="textarea"
                :rows="2"
                placeholder="后续计划安排"
              />
            </el-form-item>
            <el-form-item label="进度评估">
              <el-select v-model="form.progressStatus" style="width: 200px">
                <el-option label="正常" value="正常" />
                <el-option label="滞后" value="滞后" />
                <el-option label="严重滞后" value="严重滞后" />
              </el-select>
            </el-form-item>
            <el-form-item label="导师反馈">
              <el-input
                v-model="form.teacherFeedback"
                type="textarea"
                :rows="2"
                placeholder="教师建议"
              />
            </el-form-item>
            <el-form-item label="检查结果">
              <el-select v-model="form.checkResult" style="width: 200px">
                <el-option label="通过" value="通过" />
                <el-option label="整改" value="整改" />
              </el-select>
            </el-form-item> 
            <el-form-item>
              <el-button type="primary" :loading="saving" @click="saveMidterm">
                保存
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card shadow="never">
          <template #header>
            <span>帮助说明</span>
          </template>
          <p>1. 先在上方列表中选择学生。</p>
          <p>2. 然后在下方上传对应的中期检查表扫描件。</p>
          <p>3. 提交后等待系统审核结果。</p>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { getMidterm, upsertMidterm, getStudents } from '../api/midterm'

const students = ref([])
const loadingStudents = ref(false)
const searchKeyword = ref('')

const currentStudent = ref(null)
const saving = ref(false)
const form = reactive({
  id: null,
  completedContent: '',
  problems: '',
  nextPlan: '',
  progressStatus: '正常',
  teacherFeedback: '',
  checkResult: ''
})

const resetForm = () => {
  form.id = null
  form.completedContent = ''
  form.problems = ''
  form.nextPlan = ''
  form.progressStatus = '正常'
  form.teacherFeedback = ''
  form.checkResult = ''
}

const selectStudent = async row => {
  currentStudent.value = row
  resetForm()
  try {
    const res = await getMidterm(Number(row.id))
    if (res) {
      form.id = res.id
      form.completedContent = res.completedContent || ''
      form.problems = res.problems || ''
      form.nextPlan = res.nextPlan || ''
      form.progressStatus = res.progressStatus || '正常'
      form.teacherFeedback = res.teacherFeedback || ''
      form.checkResult = res.checkResult || ''
    }
  } catch (err) {
    console.warn('未找到记录，创建新表单')
  }
}

const saveMidterm = async () => {
  if (!currentStudent.value) {
    ElMessage.warning('请先选择学生')
    return
  }
  saving.value = true
  try {
    const payload = {
      studentId: Number(currentStudent.value.id),
      completedContent: form.completedContent,
      problems: form.problems,
      nextPlan: form.nextPlan,
      progressStatus: form.progressStatus,
      teacherFeedback: form.teacherFeedback,
      checkResult: form.checkResult
    }
    const res = await upsertMidterm(payload)
    form.id = res.id
    ElMessage.success('保存成功')
    // 保存成功后刷新学生列表，更新状态
    await loadStudents()
  } catch (err) {
    console.error(err)
    ElMessage.error('保存失败，请重试')
  } finally {
    saving.value = false
  }
}

// 获取状态对应的标签类型
const getStatusType = (status) => {
  switch (status) {
    case '通过':
      return 'success'
    case '整改':
      return 'warning'
    case '已提交':
      return 'info'
    case '未提交':
    default:
      return 'danger'
  }
}

// 加载学生列表
const loadStudents = async () => {
  loadingStudents.value = true
  try {
    students.value = await getStudents(searchKeyword.value)
  } catch (err) {
    console.error(err)
    ElMessage.error('加载学生列表失败')
  } finally {
    loadingStudents.value = false
  }
}

// 组件挂载时加载数据
onMounted(() => {
  loadStudents()
})
</script>

<style scoped>
.mb-16 {
  margin-bottom: 16px;
}

.upload-area {
  width: 100%;
}

.upload-icon {
  font-size: 36px;
  margin-bottom: 8px;
}
</style>
