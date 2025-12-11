<template>
  <div class="page archive-page">
    <el-card class="banner-card" shadow="never">
      <div class="banner-inner">
        <div class="banner-left">
          <div class="weather-icon">🗂</div>
          <div>
            <div class="banner-title">资料归档</div>
            <div class="banner-sub">提交论文/总结/考核表等归档资料</div>
          </div>
        </div>
      </div>
    </el-card>

    <el-card shadow="never" class="mb-16">
      <template #header>
        <span>归档记录</span>
      </template>
      <el-table :data="docs" border>
        <el-table-column prop="fileName" label="文件名称" min-width="220" />
        <el-table-column prop="fileType" label="类型" width="100" />
        <el-table-column prop="version" label="版本" width="80" />
        <el-table-column prop="uploadTime" label="上传时间" width="160" />
        <el-table-column label="审核状态" width="100">
          <template #default="{ row }">
            <el-tag
              :type="row.auditStatus === '已通过' ? 'success' : row.auditStatus === '退回' ? 'danger' : 'warning'"
              size="small"
            >
              {{ row.auditStatus }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button type="primary" link @click="editDoc(row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-card shadow="never">
      <template #header>
        <span>{{ form.id ? '编辑归档' : '新增归档' }}</span>
      </template>
      <el-form :model="form" label-width="100px" size="small" class="form-block">
        <el-form-item label="文件名称" required>
          <el-input v-model="form.fileName" placeholder="例如：毕业论文最终版.pdf" />
        </el-form-item>
        <el-form-item label="文件类型" required>
          <el-select v-model="form.fileType" placeholder="选择类型">
            <el-option label="论文" value="论文" />
            <el-option label="总结" value="总结" />
            <el-option label="考核表" value="考核表" />
          </el-select>
        </el-form-item>
        <el-form-item label="存储路径" required>
          <el-input
            v-model="form.filePath"
            placeholder="/uploads/student1000/thesis.pdf"
          />
        </el-form-item>
        <el-form-item label="版本号">
          <el-input v-model="form.version" />
        </el-form-item>
        <el-form-item label="审核状态">
          <el-select v-model="form.auditStatus">
            <el-option label="待审核" value="待审核" />
            <el-option label="已通过" value="已通过" />
            <el-option label="退回" value="退回" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="saving" @click="saveDoc">
            {{ form.id ? '更新' : '保存' }}
          </el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import {
  createArchiveDoc,
  listArchiveDocs,
  updateArchiveDoc
} from '../api/archive'

const studentId = 1
const docs = ref([])
const saving = ref(false)

const form = reactive({
  id: null,
  fileName: '',
  fileType: '论文',
  filePath: '',
  version: 'v1.0',
  auditStatus: '待审核'
})

const fetchDocs = async () => {
  try {
    docs.value = await listArchiveDocs(studentId)
  } catch (err) {
    console.error(err)
    ElMessage.error('获取归档记录失败')
  }
}

const resetForm = () => {
  form.id = null
  form.fileName = ''
  form.fileType = '论文'
  form.filePath = ''
  form.version = 'v1.0'
  form.auditStatus = '待审核'
}

const editDoc = row => {
  form.id = row.id
  form.fileName = row.fileName
  form.fileType = row.fileType
  form.filePath = row.filePath
  form.version = row.version
  form.auditStatus = row.auditStatus
}

const saveDoc = async () => {
  if (!form.fileName || !form.fileType || !form.filePath) {
    ElMessage.warning('请填写完整信息')
    return
  }
  saving.value = true
  try {
    const payload = {
      studentId,
      fileName: form.fileName,
      fileType: form.fileType,
      filePath: form.filePath,
      version: form.version,
      auditStatus: form.auditStatus
    }
    if (form.id) {
      await updateArchiveDoc(form.id, payload)
    } else {
      await createArchiveDoc(payload)
    }
    await fetchDocs()
    resetForm()
    ElMessage.success('保存成功')
  } catch (err) {
    console.error(err)
    ElMessage.error('保存失败，请重试')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  fetchDocs()
})
</script>

<style scoped>
.mb-16 {
  margin-bottom: 16px;
}

.form-block {
  max-width: 640px;
}
</style>
