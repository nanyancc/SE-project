import { createRouter, createWebHistory } from 'vue-router'

import TopicApply from '../views/TopicApply.vue'
import TopicPublish from '../views/TopicPublish.vue'
import TopicSelect from '../views/TopicSelect.vue'
import OpeningManage from '../views/OpeningManage.vue'
import MidtermCheck from '../views/MidtermCheck.vue'
import PaperUpload from '../views/PaperUpload.vue'
import ScorePage from '../views/ScorePage.vue'
import NotificationManage from '../views/NotificationManage.vue'
import TopicReview from '../views/TopicReview.vue'

const routes = [
  { path: '/', redirect: '/topic-apply' },

  { path: '/topic-apply', component: TopicApply, meta: { title: '课题申报' } },
  { path: '/topic-publish', component: TopicPublish, meta: { title: '课题发布' } },
  { path: '/topic-select', component: TopicSelect, meta: { title: '选题管理' } },
  { path: '/opening-manage', component: OpeningManage, meta: { title: '开题管理' } },
  { path: '/midterm-check', component: MidtermCheck, meta: { title: '中期检查' } },
  { path: '/paper-upload', component: PaperUpload, meta: { title: '纸质资料及考核表' } },
  { path: '/score', component: ScorePage, meta: { title: '成绩录入与查询' } },
  { path: '/notification', component: NotificationManage, meta: { title: '通知管理' } },
  { path: '/topic-review', component: TopicReview, meta: { title: '课题审批' } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
