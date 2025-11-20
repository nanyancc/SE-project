<template>
  <div class="page midterm-page">
    <el-card class="banner-card" shadow="never">
      <div class="banner-inner">
        <div class="banner-left">
          <div class="weather-icon">🕒</div>
          <div>
            <div class="banner-title">中期检查</div>
            <div class="banner-sub">选择学生并上传中期检查表</div>
          </div>
        </div>
      </div>
    </el-card>

    <el-row :gutter="20">
      <el-col :span="16">
        <el-card shadow="never" class="mb-16">
          <template #header>
            <span>选择学生</span>
          </template>

          <el-table :data="students" border>
            <el-table-column type="index" label="序号" width="60" />
            <el-table-column prop="name" label="姓名" width="100" />
            <el-table-column prop="id" label="学号" width="120" />
            <el-table-column prop="topicName" label="课题名称" />
            <el-table-column prop="status" label="状态" width="100" />
            <el-table-column label="操作" width="100">
              <template #default="{ row }">
                <el-button type="primary" link @click="selectStudent(row)">
                  选择
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <div class="text-muted" style="margin-top: 8px">
            当前第 1 页，共 3 页（静态示例）
          </div>
        </el-card>

        <el-card shadow="never">
          <template #header>
            <span>上传中期检查表</span>
          </template>

          <p class="mb-16">
            当前选择学生：
            <strong>{{ currentStudent ? currentStudent.name : '未选择' }}</strong>
          </p>

          <el-upload
            drag
            action="#"
            :auto-upload="false"
            class="upload-area"
          >
            <el-icon class="upload-icon"><UploadFilled /></el-icon>
            <div class="el-upload__text">
              只能上传 jpg / png 文件，且不超过 500kb（示例）
            </div>
          </el-upload>

          <div class="mt-16">
            <el-button type="primary">提交</el-button>
            <el-button>保存</el-button>
          </div>
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
import { ref } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'

const students = ref([
  { id: '1000', name: '张三', topicName: '课题 1', status: '已提交' },
  { id: '1001', name: '李四', topicName: '课题 2', status: '已保存' },
  { id: '1002', name: '王五', topicName: '课题 3', status: '未提交' },
  { id: '1003', name: '赵六', topicName: '课题 4', status: '未提交' }
])

const currentStudent = ref(null)

const selectStudent = row => {
  currentStudent.value = row
}
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
