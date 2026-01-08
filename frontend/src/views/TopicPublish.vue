<template>
  <div class="page topic-publish-page">
    <!-- 顶部 Banner -->
    <el-card class="banner-card" shadow="never">
      <div class="banner-inner">
        <div class="banner-left">
          <div class="weather-icon">☁️</div>
          <div>
            <div class="banner-title">张教授 您好！</div>
            <div class="banner-sub">请管理您已通过审批的课题发布状态</div>
          </div>
        </div>
      </div>
    </el-card>

    <el-card shadow="never" class="mb-16">
      <el-form inline>
        <el-form-item label="课题名称">
          <el-input v-model="keyword" placeholder="请输入课题名称" clearable @keyup.enter="fetchTopics"/>
        </el-form-item>
        <el-form-item label="课题类型">
          <el-select v-model="type" placeholder="全部" clearable>
            <el-option label="全部" value="" />
            <el-option label="科研课题" value="科研课题" />
            <el-option label="企业项目" value="企业项目" />
            <el-option label="教学题目" value="教学题目" />
          </el-select>
        </el-form-item>
        <el-form-item label="发布状态">
          <el-select v-model="publishStatusStr" placeholder="全部" clearable>
            <el-option label="全部" value="" />
            <!-- 修改：严格对应数据库字典 0:未发布 -->
            <el-option label="未发布" value="0" />
            <el-option label="已发布" value="1" />
            <el-option label="已下架" value="2" />
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="fetchTopics" :loading="loading">搜索</el-button>
          <el-button @click="resetSearch">清除筛选</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-row :gutter="20">
      <el-col :span="16">
        <el-card shadow="never">
          <template #header>
            <span>已通过审批的课题</span>
          </template>

          <el-table
            :data="tableData"
            highlight-current-row
            @current-change="onRowChange"
            v-loading="loading"
          >
            <el-table-column label="课题题目" min-width="260">
              <template #default="{ row }">
                <div class="topic-title">
                  <div style="font-weight: bold;">{{ row.title }}</div>
                  <div class="tag-list">
                    <el-tag size="small" effect="plain" type="info">
                      {{ row.type }}
                    </el-tag>
                    <el-tag size="small" effect="plain" type="info" style="margin-left: 5px;">
                      限选{{ row.maxStudents }}人
                    </el-tag>
                  </div>
                </div>
              </template>
            </el-table-column>
            
            <el-table-column prop="type" label="类型" width="100" />
            
            <el-table-column label="状态" width="100">
              <template #default="{ row }">
                <!-- 修改：状态文案修正 -->
                <el-tag v-if="row.publishStatus === 0" type="info" size="small">未发布</el-tag>
                <el-tag v-else-if="row.publishStatus === 1" type="success" size="small">已发布</el-tag>
                <el-tag v-else-if="row.publishStatus === 2" type="warning" size="small">已下架</el-tag>
              </template>
            </el-table-column>
            

            
            <el-table-column label="操作" width="140">
              <template #default="{ row }">
                <!-- 
                   逻辑：
                   已发布(1) -> 显示“下架”按钮 (变为2)
                   未发布(0) 或 已下架(2) -> 显示“发布”按钮 (变为1)
                -->
                <el-button 
                  v-if="row.publishStatus === 1"
                  type="warning" link 
                  @click.stop="togglePublishStatus(row, 2)"
                >
                  下架
                </el-button>
                <el-button 
                  v-else
                  type="success" link 
                  @click.stop="togglePublishStatus(row, 1)"
                >
                  发布
                </el-button>
                <el-button type="primary" link @click.stop="handleEdit(row)">编辑</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card shadow="never" class="detail-card">
          <template #header>
            <span>课题详情</span>
          </template>
          <div v-if="currentTopic">
            <h3 style="margin-top:0;">{{ currentTopic.title }}</h3>
            <p><strong>类型：</strong>{{ currentTopic.type }}</p>
            <p><strong>状态：</strong>
               <!-- 修改：详情页文案修正 -->
               <span v-if="currentTopic.publishStatus === 0">未发布</span>
               <span v-if="currentTopic.publishStatus === 1" style="color:green">已发布</span>
               <span v-if="currentTopic.publishStatus === 2" style="color:orange">已下架</span>
            </p>
            <el-divider content-position="left">详细信息</el-divider>
            <p><strong>面向专业：</strong>{{ currentTopic.majorLimit || '不限' }}</p>
            <p><strong>限选人数：</strong>{{ currentTopic.maxStudents }} 人</p>
            <p><strong>研究内容：</strong></p>
            <div class="content-box">{{ currentTopic.content || '暂无内容' }}</div>
            <p><strong>预期成果：</strong></p>
            <div class="content-box">{{ currentTopic.expectedResult || '暂无' }}</div>
            <br/>
            <p style="color:#909399; font-size:12px;">创建于：{{ formatDate(currentTopic.createdAt) }}</p>
          </div>
          <div v-else class="empty-tip">
            请点击左侧列表查看详细信息
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

// --- 状态 ---
const keyword = ref('')
const type = ref('')
const publishStatusStr = ref('')
const loading = ref(false)
const tableData = ref([])
const currentTopic = ref(null)

// 假设当前教师 ID 为 1
const teacherId = 1

// --- API ---
const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '/api',
  timeout: 5000
})

// --- 方法 ---

// 1. 获取课题列表
const fetchTopics = async () => {
  loading.value = true
  try {
    const params = {
      keyword: keyword.value || undefined,
      type: type.value || undefined,
      teacherId: teacherId,
      status: '通过', // 强制只查审核通过的
      publishStatus: publishStatusStr.value !== '' ? parseInt(publishStatusStr.value) : undefined, 
      limit: 50
    }
    
    const res = await request.get('/extra/topics', { params })
    
    if (res.data && res.data.items) {
      tableData.value = res.data.items.map(item => ({
        id: item.id,
        title: item.topic_name,
        type: item.topic_type,
        maxStudents: item.max_students,
        majorLimit: item.major_limit,
        content: item.content,
        expectedResult: item.expected_result,
        publishStatus: item.publish_status, // 0:未发布, 1:已发布, 2:已下架
        createdAt: item.created_at
      }))
      
      // 同步更新详情页数据
      if (currentTopic.value) {
        const found = tableData.value.find(t => t.id === currentTopic.value.id)
        currentTopic.value = found || null
      }
    }
  } catch (error) {
    ElMessage.error('加载课题列表失败')
  } finally {
    loading.value = false
  }
}

// 2. 切换发布状态
const togglePublishStatus = async (row, newStatus) => {
  try {
    await request.put(`/extra/topics/${row.id}`, {
      publish_status: newStatus
    })
    
    // 提示文案处理
    let actionName = ''
    if (newStatus === 1) actionName = '发布'
    else if (newStatus === 2) actionName = '下架'
    else actionName = '取消发布' // 如果有变成0的操作

    ElMessage.success(`课题 "${row.title}" 已${actionName}`)
    
    // 前端更新状态
    row.publishStatus = newStatus
    if (currentTopic.value && currentTopic.value.id === row.id) {
      currentTopic.value.publishStatus = newStatus
    }
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

// 3. 点击行显示详情
const onRowChange = (row) => {
  currentTopic.value = row
}

// 4. 编辑
const handleEdit = (row) => {
  ElMessage.info(`跳转到编辑页面: ${row.title}`)
}

// 5. 重置搜索
const resetSearch = () => {
  keyword.value = ''
  type.value = ''
  publishStatusStr.value = ''
  fetchTopics()
}

// 辅助：日期格式化
const formatDate = (d) => {
  if (!d) return '-'
  return new Date(d).toLocaleDateString()
}

// 初始化
onMounted(() => {
  fetchTopics()
})
</script>

<style scoped>
.mb-16 { margin-bottom: 16px; }
.topic-title { display: flex; flex-direction: column; }
.tag-list { margin-top: 4px; }
.detail-card { min-height: 400px; }
.empty-tip { color: #909399; text-align: center; padding: 40px 0; }
.content-box {
  background: #f5f7fa;
  padding: 10px;
  border-radius: 4px;
  font-size: 13px;
  line-height: 1.5;
  color: #606266;
  white-space: pre-wrap;
}


</style>