<template>
  <div class="page opening-page">
    <el-card class="banner-card" shadow="never">
      <div class="banner-inner">
        <div class="banner-left">
          <div class="weather-icon">🌤</div>
          <div>
            <div class="banner-title">
              {{ studentInfo.name }}，祝你开题顺利！
            </div>
            <div class="banner-sub">学号：{{ studentInfo.id }} | 课题ID：{{ studentInfo.topicId }}</div>
          </div>
        </div>
      </div>
    </el-card>

    <el-row :gutter="20">
      <!-- 左侧开题信息 + 报告上传 -->
      <el-col :span="16">
        <el-card shadow="never">
          <template #header>
            <span>开题报告</span>
          </template>
          <el-form :model="report" label-width="100px" label-position="left">
            <el-form-item label="研究背景">
              <el-input
                v-model="report.background"
                type="textarea"
                :rows="3"
                placeholder="填写研究背景/动机"
              />
            </el-form-item>
            <el-form-item label="研究目标">
              <el-input
                v-model="report.target"
                type="textarea"
                :rows="2"
                placeholder="目标与预期成果"
              />
            </el-form-item>
            <el-form-item label="研究方法">
              <el-input
                v-model="report.method"
                type="textarea"
                :rows="3"
                placeholder="拟采用的方法、工具、技术路线"
              />
            </el-form-item>
            <el-form-item label="时间计划">
              <el-input
                v-model="report.plan"
                type="textarea"
                :rows="3"
                placeholder="阶段计划与里程碑"
              />
            </el-form-item>
            <el-form-item label="导师意见">
              <el-input
                v-model="report.teacherComment"
                type="textarea"
                :rows="2"
                placeholder="审批/意见"
              />
            </el-form-item>
            <el-form-item label="报告状态">
              <el-tag :type="statusTag(report.reportStatus)" size="small">
                {{ report.reportStatus }}
              </el-tag>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="saving" @click="saveReport('待审核')">
                保存
              </el-button>
              <el-button type="success" :loading="saving" @click="saveReport('已通过')">
                标记通过
              </el-button>
              <el-button type="warning" :loading="saving" @click="saveReport('需修改')">
                退回修改
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <!-- 右侧通知及审批历史 -->
      <el-col :span="8">
        <el-card shadow="never">
          <template #header>
            <span>通知及审批历史</span>
          </template>
          <el-timeline>
            <el-timeline-item
              v-for="item in history"
              :key="item.time"
              :timestamp="item.time"
            >
              <p>{{ item.title }}</p>
              <p class="text-muted">{{ item.remark }}</p>
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import {
  createOpeningReport,
  getOpeningReport,
  updateOpeningReport
} from '../api/opening'

const studentInfo = {
  id: 1,
  name: '测试学生',
  topicId: 2001
}

const report = ref({
  id: null,
  studentId: studentInfo.id,
  topicId: studentInfo.topicId,
  background: '',
  target: '',
  method: '',
  plan: '',
  reportStatus: '待审核',
  teacherComment: ''
})

const history = ref([])
const saving = ref(false)

const statusTag = status => {
  if (status === '已通过') return 'success'
  if (status === '需修改') return 'warning'
  return 'info'
}

const buildHistory = data => {
  const items = []
  if (data.submitTime) {
    items.push({
      time: data.submitTime?.slice(0, 10),
      title: '提交开题报告',
      remark: '学生提交'
    })
  }
  if (data.auditTime) {
    items.push({
      time: data.auditTime?.slice(0, 10),
      title: '导师审核',
      remark: data.teacherComment || '导师反馈'
    })
  }
  history.value = items
}

const fetchReport = async () => {
  try {
    const data = await getOpeningReport(studentInfo.id)
    if (data) {
      report.value = {
        ...report.value,
        ...data,
        studentId: data.studentId,
        topicId: data.topicId
      }
      buildHistory(data)
    }
  } catch (err) {
    console.error(err)
  }
}

const saveReport = async status => {
  saving.value = true
  try {
    const payload = { ...report.value, reportStatus: status }
    let saved
    if (report.value.id) {
      saved = await updateOpeningReport(report.value.id, payload)
    } else {
      saved = await createOpeningReport(payload)
    }
    report.value = { ...report.value, ...saved }
    buildHistory(saved)
    ElMessage.success('保存成功')
  } catch (err) {
    console.error(err)
    ElMessage.error('保存失败，请重试')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  fetchReport()
})
</script>

<style scoped>
.mb-16 {
  margin-bottom: 16px;
}
</style>
