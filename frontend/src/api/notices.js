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

const buildQuery = (params = {}) => {
  const search = new URLSearchParams()
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== null && v !== '') {
      search.set(k, v)
    }
  })
  return search.toString()
}

const toClient = data => ({
  id: data.id,
  title: data.title,
  type: data.type,
  majors: data.majors || [],
  teacherScope: data.teacher_scope || '',
  requirement: data.requirement || '',
  autoRemind: data.auto_remind ?? false,
  startTime: data.start_time || data.startTime,
  endTime: data.end_time || data.endTime,
  status: data.status,
  publisher: data.publisher,
  publishTime: data.publish_time || data.publishTime
})

const toServer = payload => ({
  title: payload.title,
  type: payload.type,
  majors: payload.majors || [],
  teacher_scope: payload.teacherScope || '',
  requirement: payload.requirement || '',
  auto_remind: payload.autoRemind ?? true,
  start_time: payload.startTime,
  end_time: payload.endTime,
  status: payload.status || '草稿',
  publisher: payload.publisher || '教科办'
})

export const listNotices = async params => {
  const qs = buildQuery(params)
  const data = await fetchJson(`${API_BASE}/extra/notices?${qs}`)
  return data.map(toClient)
}

export const saveNotice = async payload => {
  if (payload.id) {
    const data = await fetchJson(`${API_BASE}/extra/notices/${payload.id}`, {
      method: 'PUT',
      body: JSON.stringify(toServer(payload))
    })
    return toClient(data)
  }
  const data = await fetchJson(`${API_BASE}/extra/notices`, {
    method: 'POST',
    body: JSON.stringify(toServer(payload))
  })
  return toClient(data)
}

export const publishNotice = async id => {
  return fetchJson(`${API_BASE}/extra/notices/${id}/publish`, { method: 'POST' })
}

export const revokeNotice = async id => {
  return fetchJson(`${API_BASE}/extra/notices/${id}/revoke`, { method: 'POST' })
}
