const API_BASE = import.meta.env.VITE_API_BASE || '/api'

const fetchJson = async (url, options) => {
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...options
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || '请求失败')
  }
  return res.json()
}

// 获取学生列表（用于中期检查）
export const getStudents = async (keyword = '') => {
  const params = keyword ? `?keyword=${encodeURIComponent(keyword)}` : ''
  const data = await fetchJson(`${API_BASE}/extra/students${params}`)
  return data.map(item => ({
    id: item.id,
    name: item.name,
    userCode: item.user_code,
    topicId: item.topic_id,
    topicName: item.topic_name,
    status: item.status
  }))
}

const toClient = data => ({
  id: data.id,
  studentId: data.student_id ?? data.studentId,
  completedContent: data.completed_content ?? data.completedContent,
  problems: data.problems,
  nextPlan: data.next_plan ?? data.nextPlan,
  progressStatus: data.progress_status ?? data.progressStatus,
  teacherFeedback: data.teacher_feedback ?? data.teacherFeedback,
  checkResult: data.check_result ?? data.checkResult,
  submitTime: data.submit_time ?? data.submitTime
})

const toServer = payload => ({
  student_id: payload.studentId,
  completed_content: payload.completedContent,
  problems: payload.problems,
  next_plan: payload.nextPlan,
  progress_status: payload.progressStatus,
  teacher_feedback: payload.teacherFeedback,
  check_result: payload.checkResult
})

export const getMidterm = async studentId => {
  const data = await fetchJson(`${API_BASE}/extra/midterm-checks/${studentId}`)
  return toClient(data)
}

export const upsertMidterm = async payload => {
  const data = await fetchJson(`${API_BASE}/extra/midterm-checks`, {
    method: 'POST',
    body: JSON.stringify(toServer(payload))
  })
  return toClient(data)
}

export const updateMidterm = async (id, payload) => {
  const data = await fetchJson(`${API_BASE}/extra/midterm-checks/${id}`, {
    method: 'PUT',
    body: JSON.stringify(toServer(payload))
  })
  return toClient(data)
}
