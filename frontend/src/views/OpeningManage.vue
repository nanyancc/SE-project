<template>
  <div class="page opening-page">
    <!-- 1. 顶部身份模拟 -->
    <el-card class="role-switch-card" shadow="never">
      <div class="role-switch-inner">
        <div class="switch-group">
          <span class="label">当前身份：</span>
          <el-radio-group v-model="currentRole" @change="handleRoleChange">
            <el-radio-button label="student">学生</el-radio-button>
            <el-radio-button label="teacher">导师</el-radio-button>
          </el-radio-group>
        </div>

        <div class="student-simulator">
          <span class="label">{{ currentRole === 'student' ? '我的学号' : '查询学生学号' }}：</span>
          <el-input-number 
            v-model="targetStudentId" 
            :min="1" 
            :max="99999" 
            size="small" 
            @change="handleIdChange"
          />
          <el-button 
            type="primary" 
            link 
            size="small" 
            style="margin-left: 10px" 
            @click="loadReport"
          >
            加载数据
          </el-button>
        </div>
      </div>
    </el-card>

    <!-- 2. Banner -->
    <el-card class="banner-card" shadow="never">
      <div class="banner-inner">
        <div class="banner-left">
          <div class="weather-icon">📝</div>
          <div>
            <div class="banner-title">
              {{ currentRole === 'student' ? '开题报告申报' : '开题报告审核' }}
            </div>
            <div class="banner-sub">
              {{ currentRole === 'student' ? '请完善您的开题信息并提交' : '请输入学生ID查询并审核报告' }}
            </div>
          </div>
        </div>
        <div class="banner-right">
          <el-tag size="large" :type="getStatusType(reportForm.reportStatus)">
            当前状态：{{ reportForm.reportStatus || '未创建' }}
          </el-tag>
        </div>
      </div>
    </el-card>

    <el-row :gutter="20">
      <!-- 3. 主表单区域 -->
      <el-col :span="16">
        <el-card shadow="never" v-loading="loading">
          <template #header>
            <div class="card-header">
              <span>报告内容</span>
              <span v-if="reportForm.id" style="font-size: 12px; color: #999;">
                报告ID: {{ reportForm.id }} | 最后更新: {{ formatTime(reportForm.submitTime) }}
              </span>
            </div>
          </template>

          <el-form 
            :model="reportForm" 
            label-width="120px" 
            label-position="top"
            :disabled="isFormDisabled"
          >
            <!-- ⬇️⬇️⬇️ 新增：课题ID输入框 ⬇️⬇️⬇️ -->
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="课题ID (Topic ID)">
                  <el-input-number 
                    v-model="reportForm.topicId" 
                    style="width: 100%" 
                    placeholder="请输入课题ID"
                    :disabled="!!reportForm.id || currentRole === 'teacher'"
                  />
                  <!-- 说明：如果报告已存在(id不为空)或角色是导师，则禁止修改课题ID -->
                </el-form-item>
              </el-col>
            </el-row>
            <!-- ⬆️⬆️⬆️ 新增结束 ⬆️⬆️⬆️ -->

            <!-- 学生填写区 -->
            <el-form-item label="研究背景 (Background)">
              <el-input 
                v-model="reportForm.background" 
                type="textarea" 
                :rows="3" 
                placeholder="请输入研究背景..." 
              />
            </el-form-item>
            <el-form-item label="研究目标 (Target)">
              <el-input 
                v-model="reportForm.target" 
                type="textarea" 
                :rows="2" 
                placeholder="请输入研究目标..." 
              />
            </el-form-item>
            <el-form-item label="研究方法 (Method)">
              <el-input 
                v-model="reportForm.method" 
                type="textarea" 
                :rows="3" 
                placeholder="请输入研究方法..." 
              />
            </el-form-item>
            <el-form-item label="时间计划 (Plan)">
              <el-input 
                v-model="reportForm.plan" 
                type="textarea" 
                :rows="3" 
                placeholder="请输入进度安排..." 
              />
            </el-form-item>

            <!-- 导师审核区 -->
            <div v-if="currentRole === 'teacher' || reportForm.teacherComment" class="audit-section">
              <el-divider content-position="left">导师审核</el-divider>
              <el-form-item label="导师评语 (Teacher Comment)">
                <el-input 
                  v-model="reportForm.teacherComment" 
                  type="textarea" 
                  :rows="2" 
                  placeholder="导师在此输入评语..." 
                  :disabled="currentRole === 'student'" 
                />
              </el-form-item>
            </div>

            <!-- 按钮操作区 -->
            <el-form-item style="margin-top: 30px;">
              <template v-if="currentRole === 'student'">
                <el-button 
                  type="primary" 
                  @click="handleStudentSubmit" 
                  :loading="submitting"
                  :disabled="reportForm.reportStatus === '已通过'"
                >
                  {{ reportForm.id ? '更新报告 (PUT)' : '创建报告 (POST)' }}
                </el-button>
                <span v-if="reportForm.reportStatus === '已通过'" class="tips">已通过审核，无法修改</span>
              </template>

              <template v-if="currentRole === 'teacher'">
                <el-button 
                  type="success" 
                  @click="handleTeacherAudit('已通过')" 
                  :loading="submitting"
                  :disabled="!reportForm.id"
                >
                  通过 (Pass)
                </el-button>
                <el-button 
                  type="warning" 
                  @click="handleTeacherAudit('需修改')" 
                  :loading="submitting"
                  :disabled="!reportForm.id"
                >
                  退回 (Reject)
                </el-button>
              </template>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <!-- 4. 右侧信息栏 -->
      <el-col :span="8">
        <el-card shadow="never">
          <template #header><span>数据状态</span></template>
          <el-descriptions :column="1" border size="small">
            <el-descriptions-item label="学生ID">{{ targetStudentId }}</el-descriptions-item>
            <el-descriptions-item label="课题ID">
              <span style="font-weight: bold; color: #409EFF">{{ reportForm.topicId || '未输入' }}</span>
            </el-descriptions-item>
            <el-descriptions-item label="审核状态">
              <el-tag size="small" :type="getStatusType(reportForm.reportStatus)">
                {{ reportForm.reportStatus || '空' }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="审核时间">
              {{ formatTime(reportForm.auditTime) }}
            </el-descriptions-item>
          </el-descriptions>
          
          <div class="api-tip">
            <p><strong>测试说明：</strong></p>
            <p>1. 输入学生ID点击加载。</p>
            <p>2. 如果是新报告，<strong>请输入课题ID</strong>。</p>
            <p>3. 填写内容并提交。</p>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

// --- 状态定义 ---
const currentRole = ref('student') // 当前角色
const targetStudentId = ref(1)     // 要操作的学生ID
const loading = ref(false)
const submitting = ref(false)

// 表单数据
const reportForm = ref({
  id: null,             
  studentId: null,
  topicId: 1,           // 默认给个 1，方便测试，用户可改
  background: '',
  target: '',
  method: '',
  plan: '',
  reportStatus: '',     
  teacherComment: '',
  submitTime: null,
  auditTime: null
})

// --- Axios 实例 ---
const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '/api',
  timeout: 5000
})

// --- 核心业务逻辑 ---

// 1. GET 查询报告
const loadReport = async () => {
  if (!targetStudentId.value) return
  loading.value = true
  try {
    const res = await request.get('/extra/opening-reports', {
      params: { studentId: targetStudentId.value }
    })

    if (res.data) {
      // 查到了：映射数据
      const data = res.data
      reportForm.value = {
        id: data.id,
        studentId: data.student_id,
        topicId: data.topic_id, // 从后端读取真实的 Topic ID
        background: data.background,
        target: data.target,
        method: data.method,
        plan: data.plan,
        reportStatus: data.report_status,
        teacherComment: data.teacher_comment,
        submitTime: data.submit_time,
        auditTime: data.audit_time
      }
      ElMessage.success('数据加载成功')
    } else {
      // 没查到：重置表单
      resetForm()
      ElMessage.info('该学生暂无开题报告，请输入课题ID并新建')
    }
  } catch (error) {
    console.error(error)
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

// 2. 学生提交 (POST 或 PUT)
const handleStudentSubmit = async () => {
  if (!reportForm.value.background || !reportForm.value.plan) {
    ElMessage.warning('请填写完整的开题内容')
    return
  }
  if (!reportForm.value.topicId) {
    ElMessage.warning('请填写课题ID')
    return
  }

  submitting.value = true
  try {
    let res
    const commonPayload = {
      background: reportForm.value.background,
      target: reportForm.value.target,
      method: reportForm.value.method,
      plan: reportForm.value.plan,
      report_status: '待审核'
    }

    if (reportForm.value.id) {
      // PUT: 更新
      res = await request.put(`/extra/opening-reports/${reportForm.value.id}`, commonPayload)
      ElMessage.success('更新成功 (PUT)')
    } else {
      // POST: 创建 (需要传 IDs)
      const createPayload = {
        ...commonPayload,
        student_id: targetStudentId.value,
        topic_id: reportForm.value.topicId // 使用用户输入的 topicId
      }
      res = await request.post('/extra/opening-reports', createPayload)
      ElMessage.success('创建成功 (POST)')
    }

    if (res.data) {
      const data = res.data
      reportForm.value.id = data.id
      reportForm.value.reportStatus = data.report_status
      reportForm.value.submitTime = data.submit_time
    }
    
  } catch (error) {
    // 捕获 400 错误 (如 topic_id 不存在)
    const msg = error.response?.data?.detail || '提交失败，请检查课题ID是否存在'
    ElMessage.error(msg)
  } finally {
    submitting.value = false
  }
}

// 3. 导师审核 (PUT)
const handleTeacherAudit = async (newStatus) => {
  if (!reportForm.value.id) {
    ElMessage.warning('当前无报告可审核')
    return
  }

  submitting.value = true
  try {
    const payload = {
      report_status: newStatus,
      teacher_comment: reportForm.value.teacherComment
    }
    const res = await request.put(`/extra/opening-reports/${reportForm.value.id}`, payload)
    
    if (res.data) {
      reportForm.value.reportStatus = res.data.report_status
      reportForm.value.auditTime = res.data.audit_time
    }
    ElMessage.success(`审核完成：${newStatus}`)
  } catch (error) {
    ElMessage.error('审核操作失败')
  } finally {
    submitting.value = false
  }
}

// --- 辅助逻辑 ---

const resetForm = () => {
  reportForm.value = {
    id: null,
    studentId: targetStudentId.value,
    topicId: 1, // 默认重置为 1
    background: '', target: '', method: '', plan: '',
    reportStatus: '未创建', teacherComment: '',
    submitTime: null, auditTime: null
  }
}

// 控制表单禁用状态
const isFormDisabled = computed(() => {
  if (currentRole.value === 'teacher') return false // 导师模式下，表单整体不禁用，但输入框可能单独控制
  if (reportForm.value.reportStatus === '已通过') return true 
  return false
})

const handleRoleChange = () => {
  loadReport()
}

const handleIdChange = () => {
  loadReport()
}

const getStatusType = (status) => {
  const map = { '已通过': 'success', '需修改': 'warning', '待审核': 'primary', '未创建': 'info' }
  return map[status] || 'info'
}

const formatTime = (t) => {
  if (!t) return '-'
  return new Date(t).toLocaleString()
}

onMounted(() => {
  loadReport()
})
</script>

<style scoped>
.page { padding: 20px; }
.mb-16 { margin-bottom: 16px; }

/* 角色切换区 */
.role-switch-card { margin-bottom: 20px; background-color: #f8f9fa; }
.role-switch-inner { display: flex; align-items: center; gap: 30px; }
.switch-group, .student-simulator { display: flex; align-items: center; }
.label { font-weight: bold; margin-right: 10px; font-size: 14px; }

/* Banner */

/* 审核区 */
.audit-section {
  background-color: #fdf6ec;
  padding: 10px 15px;
  border-radius: 4px;
  margin-top: 20px;
  border: 1px solid #faecd8;
}
.api-tip {
  margin-top: 20px;
  padding: 10px;
  background: #f4f4f5;
  border-radius: 4px;
  font-size: 12px;
  color: #909399;
  line-height: 1.8;
}
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>