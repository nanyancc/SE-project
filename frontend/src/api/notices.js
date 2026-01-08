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

// 补全时间格式：YYYY-MM-DD HH:mm -> YYYY-MM-DD HH:mm:ss
const normalizeTime = t => {
  if (!t) return t
  // 如果已经有秒数则不处理
  if (/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}/.test(t)) return t
  // YYYY-MM-DD HH:mm 补上 :00
  if (/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$/.test(t)) return t + ':00'
  return t
}

const toServer = payload => ({
  title: payload.title,
  type: payload.type,
  majors: payload.majors || [],
  teacher_scope: payload.teacherScope || '',
  requirement: payload.requirement || '',
  auto_remind: payload.autoRemind ?? true,
  start_time: normalizeTime(payload.startTime),
  end_time: normalizeTime(payload.endTime),
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
