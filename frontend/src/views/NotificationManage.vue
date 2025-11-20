<template>
  <div class="page notification-page">
    <el-card class="banner-card" shadow="never">
      <div class="banner-inner">
        <div class="banner-left">
          <div class="weather-icon">🔔</div>
          <div>
            <div class="banner-title">通知管理</div>
            <div class="banner-sub">创建、编辑毕业设计相关通知</div>
          </div>
        </div>
      </div>
    </el-card>

    <el-row :gutter="20">
      <el-col :span="16">
        <el-card shadow="never" class="mb-16">
          <el-form inline>
            <el-form-item label="通知标题">
              <el-input v-model="keyword" placeholder="请输入通知标题" />
            </el-form-item>
            <el-form-item label="通知状态">
              <el-select v-model="status" placeholder="全部">
                <el-option label="全部" value="" />
                <el-option label="草稿" value="草稿" />
                <el-option label="已发布" value="已发布" />
                <el-option label="已结束" value="已结束" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary">搜索</el-button>
              <el-button>导出报表</el-button>
              <el-button type="primary">创建通知</el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <el-card shadow="never">
          <template #header>
            <span>通知列表</span>
          </template>

          <el-table
            :data="filteredList"
            highlight-current-row
            @current-change="onRowChange"
          >
            <el-table-column prop="title" label="标题" min-width="220" />
            <el-table-column prop="range" label="通知对象" width="120" />
            <el-table-column label="状态" width="90">
              <template #default="{ row }">
                <el-tag
                  v-if="row.status === '已发布'"
                  type="success"
                  size="small"
                >
                  已发布
                </el-tag>
                <el-tag
                  v-else-if="row.status === '草稿'"
                  type="info"
                  size="small"
                >
                  草稿
                </el-tag>
                <el-tag
                  v-else
                  type="warning"
                  size="small"
                >
                  已结束
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="start" label="开始时间" width="120" />
            <el-table-column prop="end" label="结束时间" width="120" />
            <el-table-column label="完成率" width="120">
              <template #default="{ row }">
                <el-progress :percentage="row.progress" :stroke-width="8" />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="140">
              <template #default>
                <el-button type="primary" link>查看</el-button>
                <el-button type="primary" link>编辑</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card shadow="never" class="detail-card">
          <template #header>
            <span>通知详情 / 审批进度</span>
          </template>

          <div v-if="current">
            <p><strong>标题：</strong>{{ current.title }}</p>
            <p><strong>发布范围：</strong>{{ current.range }}</p>
            <p><strong>时间：</strong>{{ current.start }} ~ {{ current.end }}</p>
            <p class="mt-16"><strong>内容摘要：</strong></p>
            <p class="text-muted">
              {{ current.content }}
            </p>

            <p class="mt-16"><strong>完成情况：</strong></p>
            <el-progress :percentage="current.progress" />

            <p class="mt-16"><strong>时间线：</strong></p>
            <el-timeline>
              <el-timeline-item
                v-for="item in current.timeline"
                :key="item.time"
                :timestamp="item.time"
              >
                {{ item.text }}
              </el-timeline-item>
            </el-timeline>
          </div>
          <div v-else class="empty-tip">
            请选择左侧一条通知查看详细信息
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const keyword = ref('')
const status = ref('')

const notices = ref([
  {
    id: 1,
    title: '2025 届毕业设计选题通知',
    range: '全部学生',
    status: '已发布',
    start: '2025-03-15',
    end: '2025-04-15',
    progress: 95,
    content: '关于 2025 届毕业设计选题的安排，请各位同学在规定时间内完成选题并提交志愿。',
    timeline: [
      { time: '2025-03-15', text: '通知已发布' },
      { time: '2025-03-20', text: '超过 50% 学生完成选题' },
      { time: '2025-04-10', text: '超过 90% 学生完成选题' }
    ]
  },
  {
    id: 2,
    title: '中期检查安排',
    range: '指导教师',
    status: '已发布',
    start: '2025-05-01',
    end: '2025-05-15',
    progress: 68,
    content: '请各位指导教师在规定时间内完成所带学生的中期检查，并上传相关表格。',
    timeline: [{ time: '2025-05-01', text: '通知已发布' }]
  },
  {
    id: 3,
    title: '毕业论文提交截止提醒',
    range: '全部学生',
    status: '草稿',
    start: '2025-06-01',
    end: '2025-06-15',
    progress: 0,
    content: '草稿通知示例，尚未发布。',
    timeline: []
  }
])

const current = ref(null)

const filteredList = computed(() =>
  notices.value.filter(n => {
    const k = keyword.value.trim()
    return (
      (!k || n.title.includes(k)) &&
      (!status.value || n.status === status.value)
    )
  })
)

const onRowChange = row => {
  current.value = row
}
</script>

<style scoped>
.mb-16 {
  margin-bottom: 16px;
}

.detail-card {
  min-height: 260px;
}

.empty-tip {
  text-align: center;
  color: #909399;
  padding: 40px 0;
}
</style>
