const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api'

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

const toClient = data => ({
  id: data.id,
  studentId: data.student_id ?? data.studentId,
  topicId: data.topic_id ?? data.topicId,
  background: data.background,
  target: data.target,
  method: data.method,
  plan: data.plan,
  reportStatus: data.report_status ?? data.reportStatus,
  teacherComment: data.teacher_comment ?? data.teacherComment,
  submitTime: data.submit_time ?? data.submitTime,
  auditTime: data.audit_time ?? data.auditTime
})

const toServer = payload => ({
  student_id: payload.studentId,
  topic_id: payload.topicId,
  background: payload.background,
  target: payload.target,
  method: payload.method,
  plan: payload.plan,
  report_status: payload.reportStatus,
  teacher_comment: payload.teacherComment
})

export const getOpeningReport = async studentId => {
  const data = await fetchJson(
    `${API_BASE}/extra/opening-reports?studentId=${studentId}`
  )
  return data ? toClient(data) : null
}

export const createOpeningReport = async payload => {
  const data = await fetchJson(`${API_BASE}/extra/opening-reports`, {
    method: 'POST',
    body: JSON.stringify(toServer(payload))
  })
  return toClient(data)
}

export const updateOpeningReport = async (id, payload) => {
  const data = await fetchJson(`${API_BASE}/extra/opening-reports/${id}`, {
    method: 'PUT',
    body: JSON.stringify(toServer(payload))
  })
  return toClient(data)
}
