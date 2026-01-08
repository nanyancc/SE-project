const API_BASE = import.meta.env.VITE_API_BASE || '/api'

const calcTotal = data =>
  (data.processScore ?? 0) * 0.2 +
  (data.openingScore ?? 0) * 0.1 +
  (data.midtermScore ?? 0) * 0.1 +
  (data.thesisScore ?? 0) * 0.3 +
  (data.defenseScore ?? 0) * 0.3

const toClient = payload => ({
  id: payload.id,
  studentId: payload.student_id,
  processScore: payload.process_score != null ? Number(payload.process_score) : null,
  openingScore: payload.opening_score != null ? Number(payload.opening_score) : null,
  midtermScore: payload.midterm_score != null ? Number(payload.midterm_score) : null,
  thesisScore: payload.thesis_score != null ? Number(payload.thesis_score) : null,
  defenseScore: payload.defense_score != null ? Number(payload.defense_score) : null,
  topicId: payload.topic_id,
  totalScore: payload.total_score != null ? Number(payload.total_score) : null,
  scoreLevel: payload.score_level,
  isPublished: payload.is_published,
  total: payload.total ?? calcTotal({
    processScore: payload.process_score,
    openingScore: payload.opening_score,
    midtermScore: payload.midterm_score,
    thesisScore: payload.thesis_score,
    defenseScore: payload.defense_score
  })
})

const toServer = payload => ({
  student_id: payload.studentId,
  topic_id: payload.topicId,
  process_score: payload.processScore ?? null,
  opening_score: payload.openingScore ?? null,
  midterm_score: payload.midtermScore ?? null,
  thesis_score: payload.thesisScore ?? null,
  defense_score: payload.defenseScore ?? null,
  is_published: payload.isPublished != null ? Number(payload.isPublished) : 0
})

const buildQuery = (filter, limit, offset) => {
  const params = new URLSearchParams()
  if (filter.studentId) params.set('studentId', filter.studentId)
  if (filter.topicId) params.set('topicId', filter.topicId)
  if (filter.range) params.set('range', filter.range)
  if (filter.level) params.set('level', filter.level)
  if (filter.published !== '' && filter.published !== undefined && filter.published !== null) {
    params.set('published', filter.published)
  }
  params.set('limit', String(limit))
  params.set('offset', String(offset))
  return params.toString()
}

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

export const getScores = async (filter, { limit = 200, offset = 0 } = {}) => {
  const qs = buildQuery(filter, limit, offset)
  const data = await fetchJson(`${API_BASE}/scores?${qs}`)
  return {
    items: (data.items || []).map(toClient),
    total: data.total ?? 0
  }
}

export const getScoreStats = async filter => {
  const qs = buildQuery(filter, 1, 0) // limit/offset not used in stats
  const data = await fetchJson(`${API_BASE}/scores/stats?${qs}`)
  return {
    count: data.count ?? 0,
    avg: data.avg ?? 0,
    max: data.max ?? 0,
    min: data.min ?? 0,
    passRate: data.pass_rate ?? 0,
    excellentRate: data.excellent_rate ?? 0
  }
}

export const updateScore = async (id, payload) => {
  const data = await fetchJson(`${API_BASE}/scores/${id}`, {
    method: 'PUT',
    body: JSON.stringify(toServer(payload))
  })
  return toClient(data)
}

export const createScore = async payload => {
  const data = await fetchJson(`${API_BASE}/scores`, {
    method: 'POST',
    body: JSON.stringify(toServer(payload))
  })
  return toClient(data)
}

export const batchUpdateStatus = async (ids, isPublished) => {
  return fetchJson(`${API_BASE}/scores/batch/status`, {
    method: 'POST',
    body: JSON.stringify({ ids, is_published: isPublished })
  })
}
