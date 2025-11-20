<template>
  <div class="page opening-page">
    <el-card class="banner-card" shadow="never">
      <div class="banner-inner">
        <div class="banner-left">
          <div class="weather-icon">🌤</div>
          <div>
            <div class="banner-title">张三同学 您好！祝您开题顺利</div>
            <div class="banner-sub">登录时间：2025-05-20 AM 09:30:22</div>
          </div>
        </div>
      </div>
    </el-card>

    <el-row :gutter="20">
      <!-- 左侧开题信息 + 报告上传 -->
      <el-col :span="16">
        <el-card shadow="never" class="mb-16">
          <template #header>
            <span>选题名称：基于 WEB 的高校后勤车辆管理系统</span>
          </template>
          <p><strong>研究内容：</strong></p>
          <p>1）车辆管理：对校园内所有车辆的基本信息进行管理；</p>
          <p>2）预约管理：对预约车辆进行审批管理；</p>
          <p>3）系统管理：提供用户角色管理、日志查询等功能。</p>

          <div class="btn-group">
            <el-button type="primary">提交</el-button>
            <el-button>编辑</el-button>
            <el-button type="warning">申请审批</el-button>
          </div>
        </el-card>

        <el-card shadow="never">
          <template #header>
            <span>开题报告</span>
          </template>
          <el-upload
            drag
            action="#"
            :auto-upload="false"
            multiple
            class="upload-area"
          >
            <el-icon class="upload-icon"><UploadFilled /></el-icon>
            <div class="el-upload__text">
              将文件拖到此处，或 <em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">支持 dotx / pdf 文件，前端示例不真正上传</div>
            </template>
          </el-upload>
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
import { ref } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'

const history = ref([
  {
    time: '2025-04-16',
    title: '开题申请模板下载',
    remark: '教务处发布'
  },
  {
    time: '2025-04-20',
    title: '开题申请需要修改',
    remark: '指导老师：内容需补充系统架构设计'
  },
  {
    time: '2025-04-29',
    title: '开题申请审批通过',
    remark: '系主任审批通过'
  },
  {
    time: '2019-04-16',
    title: '置顶：开题截止时间为 xxxx.xx.xx 23:59',
    remark: '教务公告'
  }
])
</script>

<style scoped>
.mb-16 {
  margin-bottom: 16px;
}

.btn-group {
  margin-top: 16px;
}

.upload-area {
  width: 100%;
}

.upload-icon {
  font-size: 40px;
  margin-bottom: 10px;
}
</style>
