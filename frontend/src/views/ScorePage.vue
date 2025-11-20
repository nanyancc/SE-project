<template>
  <div class="page score-page">
    <!-- 蓝色问候卡片 -->
    <el-card class="banner-card" shadow="never">
      <div class="banner-inner">
        <div class="banner-left">
          <div class="weather-icon">☁️</div>
          <div>
            <div class="banner-title">张三同学 您好！祝您开心每一天</div>
            <div class="banner-sub">登录时间：2025-05-19 AM 01:59:13</div>
          </div>
        </div>
      </div>
    </el-card>

    <el-row :gutter="20">
      <!-- 左侧课题列表 -->
      <el-col :span="16">
        <el-card shadow="never">
          <template #header>
            <span>成绩查询与录入</span>
          </template>
          <el-scrollbar style="max-height: 520px">
            <div
              v-for="topic in topics"
              :key="topic.id"
              class="topic-row"
              :class="{ active: topic.id === selectedTopic.id }"
              @click="handleSelect(topic)"
            >
              <span class="index">{{ topic.id }}.</span>
              <span class="name">{{ topic.name }}</span>
              <span class="score-label">
                {{
                  topic.score1 == null && topic.score2 == null
                    ? '暂无成绩'
                    : `阶段一：${topic.score1 ?? '-'}，阶段二：${topic.score2 ?? '-'}`
                }}
              </span>
            </div>
          </el-scrollbar>
        </el-card>
      </el-col>

      <!-- 右侧录入表单 -->
      <el-col :span="8">
        <el-card shadow="never">
          <div class="info-line">
            <span class="label">课题名称：</span>
            <span>{{ selectedTopic.name }}</span>
          </div>
          <div class="info-line">
            <span class="label">课题状态：</span>
            <el-tag size="small" type="success">进行中</el-tag>
          </div>
          <div class="info-line">
            <span class="label">课题简介：</span>
            <span>xxxx</span>
          </div>

          <el-divider />

          <el-form label-width="80px">
            <el-form-item label="阶段一成绩">
              <el-input-number v-model="stage1" :min="0" :max="100" />
              <el-button type="primary" class="ml-8" @click="saveStage1">提交</el-button>
            </el-form-item>

            <el-form-item label="阶段二成绩">
              <el-input-number v-model="stage2" :min="0" :max="100" />
              <el-button type="primary" class="ml-8" @click="saveStage2">提交</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const topics = ref([
  { id: 1, name: '课题1 - 暂无成绩', score1: null, score2: null },
  { id: 2, name: '课题2 - 暂无成绩', score1: null, score2: null },
  { id: 3, name: '课题3 - 暂无成绩', score1: null, score2: null },
  { id: 4, name: '课题4 - 暂无成绩', score1: null, score2: null },
  { id: 5, name: '课题5 - 暂无成绩', score1: null, score2: null },
  { id: 6, name: '课题6 - 暂无成绩', score1: null, score2: null },
  { id: 7, name: '课题7 - 暂无成绩', score1: null, score2: null },
  { id: 8, name: '课题8 - 暂无成绩', score1: null, score2: null }
])

const selectedTopic = ref(topics.value[0])

const stage1 = ref(null)
const stage2 = ref(null)

const handleSelect = topic => {
  selectedTopic.value = topic
  stage1.value = topic.score1
  stage2.value = topic.score2
}

const saveStage1 = () => {
  selectedTopic.value.score1 = stage1.value
  ElMessage.success('阶段一成绩已保存（仅前端示例）')
}

const saveStage2 = () => {
  selectedTopic.value.score2 = stage2.value
  ElMessage.success('阶段二成绩已保存（仅前端示例）')
}
</script>

<style scoped>
.topic-row {
  display: flex;
  align-items: center;
  padding: 10px 12px;
  border-bottom: 1px solid #f2f2f2;
  cursor: pointer;
}

.topic-row:last-child {
  border-bottom: none;
}

.topic-row:hover {
  background: #f5f7fa;
}

.topic-row.active {
  background: #ecf5ff;
}

.index {
  width: 32px;
  color: #909399;
}

.name {
  flex: 1;
}

.score-label {
  color: #909399;
  font-size: 12px;
}

.info-line {
  margin-bottom: 10px;
  font-size: 14px;
}

.label {
  display: inline-block;
  width: 80px;
  color: #909399;
}

.ml-8 {
  margin-left: 8px;
}
</style>
