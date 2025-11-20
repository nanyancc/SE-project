<template>
  <div class="page topic-apply-page">
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

    <el-alert
      type="warning"
      show-icon
      class="mb-16"
      title="课题申报截止时间：2025-06-15 23:59:59，请在此日期前完成课题申报。"
    />

    <el-card shadow="never" class="mb-16">
      <el-descriptions :column="4" size="small" border>
        <el-descriptions-item label="教师姓名">{{ teacher.name }}</el-descriptions-item>
        <el-descriptions-item label="所属学院">{{ teacher.college }}</el-descriptions-item>
        <el-descriptions-item label="职称">{{ teacher.title }}</el-descriptions-item>
        <el-descriptions-item label="联系方式">{{ teacher.email }}</el-descriptions-item>
        <el-descriptions-item label="申报学年">
          {{ teacher.year }}
        </el-descriptions-item>
        <el-descriptions-item label="课题总数">
          {{ teacher.total }}/10
        </el-descriptions-item>
        <el-descriptions-item label="已审核">
          {{ teacher.approved }} 个课题
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag type="warning" size="small">待提交</el-tag>
        </el-descriptions-item>
      </el-descriptions>
    </el-card>

    <el-card shadow="never" class="mb-16">
      <template #header>
        <div class="table-header">
          <span>课题管理</span>
          <el-button type="primary" size="small">新建课题</el-button>
        </div>
      </template>

      <el-form inline class="mb-16">
        <el-form-item label="课题名称关键词">
          <el-input v-model="keyword" placeholder="请输入关键词查询" />
        </el-form-item>
        <el-form-item label="课题类型">
          <el-select v-model="type" placeholder="all">
            <el-option label="全部" value="" />
            <el-option label="研究型" value="研究型" />
            <el-option label="应用型" value="应用型" />
            <el-option label="设计型" value="设计型" />
          </el-select>
        </el-form-item>
        <el-form-item label="审核状态">
          <el-select v-model="status" placeholder="all">
            <el-option label="全部" value="" />
            <el-option label="已通过" value="已通过" />
            <el-option label="待审核" value="待审核" />
            <el-option label="未通过" value="未通过" />
          </el-select>
        </el-form-item>
      </el-form>

      <el-table :data="filteredList" border>
        <el-table-column prop="name" label="课题名称" min-width="240" />
        <el-table-column prop="type" label="课题类型" width="100" />
        <el-table-column prop="studentNum" label="学生人数" width="100" />
        <el-table-column label="审核状态" width="120">
          <template #default="{ row }">
            <el-tag
              v-if="row.status === '已通过'"
              type="success"
              size="small"
            >
              已通过
            </el-tag>
            <el-tag
              v-else-if="row.status === '待审核'"
              type="warning"
              size="small"
            >
              待审核
            </el-tag>
            <el-tag
              v-else
              type="danger"
              size="small"
            >
              未通过
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createdAt" label="创建日期" width="120" />
        <el-table-column label="操作" width="160">
          <template #default>
            <el-button type="primary" link>查看</el-button>
            <el-button type="primary" link>编辑</el-button>
            <el-button type="danger" link>删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const teacher = {
  name: '张教授',
  college: '计算机学院',
  title: '教授',
  email: 'zhang@university.edu.cn',
  year: '2024-2025 学年第 二学期',
  total: 5,
  approved: 2
}

const keyword = ref('')
const type = ref('')
const status = ref('')

const topics = ref([
  {
    id: 1,
    name: '基于深度学习的图像识别算法研究',
    type: '研究型',
    studentNum: '1人',
    status: '已通过',
    createdAt: '2025-05-01'
  },
  {
    id: 2,
    name: '智能校园导航系统设计与实现',
    type: '应用型',
    studentNum: '2人',
    status: '已通过',
    createdAt: '2025-05-03'
  },
  {
    id: 3,
    name: '在线教育平台前端界面设计',
    type: '设计型',
    studentNum: '2人',
    status: '待审核',
    createdAt: '2025-05-05'
  },
  {
    id: 4,
    name: '基于大数据的学生成绩分析系统',
    type: '研究型',
    studentNum: '3人',
    status: '待审核',
    createdAt: '2025-05-10'
  },
  {
    id: 5,
    name: '智能考勤整体 APP 开发',
    type: '应用型',
    studentNum: '2人',
    status: '未通过',
    createdAt: '2025-05-15'
  }
])

const filteredList = computed(() =>
  topics.value.filter(t => {
    const k = keyword.value.trim()
    return (
      (!k || t.name.includes(k)) &&
      (!type.value || t.type === type.value) &&
      (!status.value || t.status === status.value)
    )
  })
)
</script>

<style scoped>
.mb-16 {
  margin-bottom: 16px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
