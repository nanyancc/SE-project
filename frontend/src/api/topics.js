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

const buildQuery = params => {
  const search = new URLSearchParams()
  Object.entries(params || {}).forEach(([k, v]) => {
    if (v !== undefined && v !== null && v !== '') {
      search.set(k, v)
    }
  })
  return search.toString()
}

const toClient = topic => ({
  id: topic.id,
  name: topic.topic_name,
  type: topic.topic_type,
  maxStudents: topic.max_students,
  auditStatus: topic.audit_status,
  publishStatus: topic.publish_status,
  createdAt: topic.created_at?.slice(0, 10),
  content: topic.content,
  expectedResult: topic.expected_result,
  majorLimit: topic.major_limit,
  auditOpinion: topic.audit_opinion,
  teacherId: topic.teacher_id
})

const toServer = payload => ({
  topic_name: payload.name,
  topic_type: payload.type,
  teacher_id: payload.teacherId,
  content: payload.content,
  expected_result: payload.expectedResult,
  major_limit: payload.majorLimit,
  max_students: payload.maxStudents,
  audit_status: payload.auditStatus,
  audit_opinion: payload.auditOpinion,
  publish_status: payload.publishStatus
})

export const listTopics = async params => {
  const qs = buildQuery(params)
  const data = await fetchJson(`${API_BASE}/extra/topics?${qs}`)
  return {
    items: (data.items || []).map(toClient),
    total: data.total || 0
  }
}

export const createTopic = async payload => {
  const data = await fetchJson(`${API_BASE}/extra/topics`, {
    method: 'POST',
    body: JSON.stringify(toServer(payload))
  })
  return toClient(data)
}

export const updateTopic = async (id, payload) => {
  const data = await fetchJson(`${API_BASE}/extra/topics/${id}`, {
    method: 'PUT',
    body: JSON.stringify(toServer(payload))
  })
  return toClient(data)
}
