<template>
  <div class="page topic-apply-page">
    <!-- 1. 顶部 Banner -->
    <el-card class="banner-card" shadow="never">
      <div class="banner-inner">
        <div class="banner-left">
          <div class="weather-icon">📢</div>
          <div>
            <div class="banner-title">课题申报</div>
            <div class="banner-sub">管理和提交毕业设计课题申报表</div>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 2. 教师信息 -->
    <el-card shadow="never" class="mb-16">
      <el-descriptions :column="4" size="small" border>
        <el-descriptions-item label="教师姓名">{{ teacherInfo.name }}</el-descriptions-item>
        <el-descriptions-item label="所属学院">{{ teacherInfo.college }}</el-descriptions-item>
        <el-descriptions-item label="职称">{{ teacherInfo.title }}</el-descriptions-item>
        <el-descriptions-item label="课题总数">{{ teacherInfo.total }}</el-descriptions-item>
        <el-descriptions-item label="已审核">{{ teacherInfo.approved }} 个课题</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- 3. 课题列表区域 -->
    <el-card shadow="never" class="mb-16">
      <template #header>
        <div class="table-header">
          <span>课题管理</span>
          <!-- 点击触发新建弹窗 -->
          <el-button type="primary" size="small" @click="handleOpenCreate">新建课题</el-button>
        </div>
      </template>

      <!-- 搜索栏 -->
      <el-form inline class="mb-16">
        <el-form-item label="课题名称">
          <el-input v-model="keyword" placeholder="关键词" clearable @keyup.enter="fetchTopics"/>
        </el-form-item>
        <el-form-item label="审核状态">
          <el-select v-model="status" placeholder="全部" clearable>
            <el-option label="全部" value="" />
            <el-option label="待审核" value="待审核" />
            <el-option label="通过" value="通过" />
            <el-option label="拒绝" value="拒绝" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchTopics" :loading="loading">搜索</el-button>
        </el-form-item>
      </el-form>

      <!-- 表格 -->
      <el-table :data="tableData" border v-loading="loading">
        <el-table-column prop="id" label="ID" width="60" align="center" />
        <el-table-column prop="name" label="课题名称" min-width="200" show-overflow-tooltip />
        <el-table-column prop="type" label="类型" width="100" align="center" />
        <el-table-column prop="studentNum" label="限选" width="80" align="center" />
        <el-table-column label="审核状态" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="getStatusColor(row.status)" size="small">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="操作" width="180" fixed="right" align="center">
          <template #default="{ row }">
            <el-button 
              v-if="row.status === '通过'"
              type="warning" link size="small" 
              @click="handleChangeStatus(row, '拒绝')"
            >
              拒绝
            </el-button>
            <el-button 
              v-else
              type="success" link size="small" 
              @click="handleChangeStatus(row, '通过')"
            >
              通过
            </el-button>
            <el-button type="danger" link size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 4. 新建课题弹窗 (新增部分) -->
    <el-dialog
      v-model="createVisible"
      title="新建课题申报"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form ref="createFormRef" :model="createForm" :rules="rules" label-width="100px">
        <el-form-item label="课题名称" prop="topic_name">
          <el-input v-model="createForm.topic_name" placeholder="请输入课题完整名称" />
        </el-form-item>
        
        <el-row>
          <el-col :span="12">
            <el-form-item label="课题类型" prop="topic_type">
              <el-select v-model="createForm.topic_type" placeholder="请选择" style="width: 100%">
                <el-option label="科研课题" value="科研课题" />
                <el-option label="企业项目" value="企业项目" />
                <el-option label="教学题目" value="教学题目" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="限选人数" prop="max_students">
              <el-input-number v-model="createForm.max_students" :min="1" :max="10" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="面向专业" prop="major_limit">
          <el-input v-model="createForm.major_limit" placeholder="例如：软件工程、计算机科学与技术" />
        </el-form-item>

        <el-form-item label="研究内容" prop="content">
          <el-input 
            v-model="createForm.content" 
            type="textarea" 
            rows="4" 
            placeholder="简述课题的主要研究内容..." 
          />
        </el-form-item>

        <el-form-item label="预期成果" prop="expected_result">
          <el-input 
            v-model="createForm.expected_result" 
            type="textarea" 
            rows="3" 
            placeholder="例如：毕业论文一篇，原型系统一套..." 
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="createVisible = false">取消</el-button>
          <el-button type="primary" @click="submitCreate" :loading="submitting">
            提交申报
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

// --- 基础状态 ---
const teacherInfo = ref({
  id: 1, // 当前登录教师ID，提交课题时需要用到
  name: '张教授',
  college: '计算机学院',
  title: '教授',
  total: 0,
  approved: 0
})
const keyword = ref('')
const status = ref('')
const loading = ref(false)
const tableData = ref([])

// --- 新建课题相关状态 ---
const createVisible = ref(false)
const submitting = ref(false)
const createFormRef = ref(null)

// 表单数据绑定
const createForm = reactive({
  topic_name: '',
  topic_type: '',
  max_students: 1,
  major_limit: '',
  content: '',
  expected_result: ''
})

// 表单验证规则
const rules = {
  topic_name: [{ required: true, message: '请输入课题名称', trigger: 'blur' }],
  topic_type: [{ required: true, message: '请选择课题类型', trigger: 'change' }],
  content: [{ required: true, message: '请填写研究内容', trigger: 'blur' }]
}

// --- API 配置 ---
const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '/api',
  timeout: 5000
})

// --- 核心业务逻辑 ---

// 1. 获取列表
const fetchTopics = async () => {
  loading.value = true
  try {
    const res = await request.get('/extra/topics', {
      params: {
        keyword: keyword.value || undefined,
        teacherId: teacherInfo.value.id,
        status: status.value || undefined,
        limit: 100
      }
    })
    if (res.data && res.data.items) {
      tableData.value = res.data.items.map(item => ({
        id: item.id,
        name: item.topic_name,
        type: item.topic_type,
        studentNum: item.max_students,
        status: item.audit_status || '待审核',
        createdAt: item.created_at
      }))
      teacherInfo.value.total = res.data.total
      teacherInfo.value.approved = tableData.value.filter(t => t.status === '通过').length
    }
  } catch (error) {
    ElMessage.error('加载列表失败')
  } finally {
    loading.value = false
  }
}

// 2. 打开新建弹窗
const handleOpenCreate = () => {
  // 重置表单
  createForm.topic_name = ''
  createForm.topic_type = ''
  createForm.max_students = 1
  createForm.major_limit = ''
  createForm.content = ''
  createForm.expected_result = ''
  createVisible.value = true
}

// 3. 提交新建课题
const submitCreate = async () => {
  if (!createFormRef.value) return
  
  // 校验表单
  await createFormRef.value.validate(async (valid) => {
    if (valid) {
      submitting.value = true
      try {
        // 构造提交数据 (Snake Case 对应后端 Schema)
        const payload = {
          topic_name: createForm.topic_name,
          topic_type: createForm.topic_type,
          max_students: createForm.max_students,
          major_limit: createForm.major_limit,
          content: createForm.content,
          expected_result: createForm.expected_result,
          teacher_id: teacherInfo.value.id // 必填：关联当前教师
          // audit_status 默认为 '待审核'，无需前端传
        }

        await request.post('/extra/topics', payload)
        
        ElMessage.success('课题申报提交成功')
        createVisible.value = false
        fetchTopics() // 刷新列表
      } catch (error) {
        console.error(error)
        ElMessage.error('提交失败：' + (error.response?.data?.detail || '未知错误'))
      } finally {
        submitting.value = false
      }
    }
  })
}

// 4. 修改状态 (通过/拒绝)
const handleChangeStatus = async (row, targetStatus) => {
  try {
    await request.put(`/extra/topics/${row.id}`, { audit_status: targetStatus })
    row.status = targetStatus
    ElMessage.success(`状态已更新为：${targetStatus}`)
    teacherInfo.value.approved = tableData.value.filter(t => t.status === '通过').length
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

// 5. 删除课题
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确定删除课题 "${row.name}" 吗？`, '警告', {
      type: 'warning',
      confirmButtonText: '确定删除',
      cancelButtonText: '取消'
    })
    await request.delete(`/extra/topics/${row.id}`)
    ElMessage.success('删除成功')
    fetchTopics()
  } catch (err) {
    if (err !== 'cancel') ElMessage.error('删除失败')
  }
}

// 辅助方法
const getStatusColor = (status) => {
  const map = { '通过': 'success', '待审核': 'warning', '拒绝': 'danger' }
  return map[status] || 'info'
}
const formatDate = (d) => d ? new Date(d).toLocaleDateString() : '-'

onMounted(() => fetchTopics())
</script>

<style scoped>
.mb-16 { margin-bottom: 16px; }

.table-header { display: flex; justify-content: space-between; align-items: center; }
</style>