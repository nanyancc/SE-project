<template>
  <div class="page topic-publish-page">
    <el-card class="banner-card" shadow="never">
      <div class="banner-inner">
        <div class="banner-left">
          <div class="weather-icon">☁️</div>
          <div>
            <div class="banner-title">张教授 您好！今天是 2025 年 11 月 12 日</div>
            <div class="banner-sub">登录时间：2025-11-12 AM 09:30:22</div>
          </div>
        </div>
      </div>
    </el-card>

    <el-card shadow="never" class="mb-16">
      <el-form inline>
        <el-form-item label="课题名称">
          <el-input v-model="keyword" placeholder="请输入课题名称" />
        </el-form-item>
        <el-form-item label="课题类型">
          <el-select v-model="type" placeholder="全部">
            <el-option label="全部" value="" />
            <el-option label="技术开发" value="技术开发" />
            <el-option label="应用研究" value="应用研究" />
            <el-option label="设计类" value="设计类" />
          </el-select>
        </el-form-item>
        <el-form-item label="发布状态">
          <el-select v-model="status" placeholder="全部">
            <el-option label="全部" value="" />
            <el-option label="草稿" value="草稿" />
            <el-option label="已发布" value="已发布" />
            <el-option label="已下架" value="已下架" />
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary">搜索</el-button>
          <el-button>高级搜索</el-button>
          <el-button>清除筛选</el-button>
        </el-form-item>

        <el-form-item style="float: right; margin-left: auto">
          <el-button>导入模板</el-button>
          <el-button>导出列表</el-button>
          <el-button type="primary">创建课题</el-button>
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
            :data="filteredTopics"
            highlight-current-row
            @current-change="onRowChange"
          >
            <el-table-column label="课题题目" min-width="260">
              <template #default="{ row }">
                <div class="topic-title">
                  <div>{{ row.title }}</div>
                  <div class="tag-list">
                    <el-tag
                      v-for="tag in row.tags"
                      :key="tag"
                      size="small"
                      effect="plain"
                    >
                      {{ tag }}
                    </el-tag>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="type" label="类型" width="100" />
            <el-table-column label="状态" width="100">
              <template #default="{ row }">
                <el-tag
                  v-if="row.status === '草稿'"
                  type="info"
                  size="small"
                >
                  草稿
                </el-tag>
                <el-tag
                  v-else-if="row.status === '已发布'"
                  type="success"
                  size="small"
                >
                  已发布
                </el-tag>
                <el-tag
                  v-else
                  type="warning"
                  size="small"
                >
                  已下架
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="createdAt" label="创建时间" width="120" />
            <el-table-column label="操作" width="140">
              <template #default="{ row }">
                <el-button type="primary" link>
                  {{ row.status === '已发布' ? '下架' : '发布' }}
                </el-button>
                <el-button type="primary" link>编辑</el-button>
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
            <p><strong>题目：</strong>{{ currentTopic.title }}</p>
            <p><strong>类型：</strong>{{ currentTopic.type }}</p>
            <p><strong>标签：</strong></p>
            <p>
              <el-tag
                v-for="tag in currentTopic.tags"
                :key="tag"
                class="mr-4"
                size="small"
                effect="plain"
              >
                {{ tag }}
              </el-tag>
            </p>
            <p><strong>简介：</strong>这里是课题简介示例，用于展示右侧详情区域。</p>
            <p><strong>创建时间：</strong>{{ currentTopic.createdAt }}</p>
          </div>
          <div v-else class="empty-tip">
            请选择一个课题查看详细信息
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const keyword = ref('')
const type = ref('')
const status = ref('')

const topics = ref([
  {
    id: 1,
    title: '基于深度学习的图像识别算法研究与实现',
    type: '技术开发',
    status: '草稿',
    tags: ['人工智能', '计算机视觉'],
    createdAt: '2023-11-10'
  },
  {
    id: 2,
    title: '智能教学系统的设计与实现',
    type: '技术开发',
    status: '已发布',
    tags: ['Web开发', '数据分析'],
    createdAt: '2023-11-05'
  },
  {
    id: 3,
    title: '大数据分析在用户行为研究中的应用',
    type: '应用研究',
    status: '已发布',
    tags: ['大数据', '可视化'],
    createdAt: '2023-11-01'
  },
  {
    id: 4,
    title: '移动应用界面设计与用户体验研究',
    type: '设计类',
    status: '已下架',
    tags: ['UI/UX', '交互设计'],
    createdAt: '2023-10-28'
  },
  {
    id: 5,
    title: '区块链技术在供应链管理中的应用研究',
    type: '应用研究',
    status: '草稿',
    tags: ['区块链', '管理信息系统'],
    createdAt: '2023-10-25'
  }
])

const currentTopic = ref(null)

const filteredTopics = computed(() =>
  topics.value.filter(t => {
    const k = keyword.value.trim()
    return (
      (!k || t.title.includes(k)) &&
      (!type.value || t.type === type.value) &&
      (!status.value || t.status === status.value)
    )
  })
)

const onRowChange = row => {
  currentTopic.value = row
}
</script>

<style scoped>
.mb-16 {
  margin-bottom: 16px;
}

.topic-title {
  display: flex;
  flex-direction: column;
}

.tag-list {
  margin-top: 4px;
}

.mr-4 {
  margin-right: 4px;
}

.detail-card {
  min-height: 260px;
}

.empty-tip {
  color: #909399;
  text-align: center;
  padding: 40px 0;
}
</style>
