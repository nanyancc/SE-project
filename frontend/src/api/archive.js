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

const fmt = val => {
  if (!val) return ''
  return (val || '').toString().replace('T', ' ').slice(0, 19)
}

const toClient = doc => ({
  id: doc.id,
  studentId: doc.student_id ?? doc.studentId,
  fileName: doc.file_name,
  fileType: doc.file_type,
  filePath: doc.file_path,
  version: doc.version,
  uploadTime: fmt(doc.upload_time ?? doc.uploadTime),
  auditStatus: doc.audit_status ?? doc.auditStatus
})

const toServer = payload => ({
  student_id: payload.studentId,
  file_name: payload.fileName,
  file_type: payload.fileType,
  file_path: payload.filePath,
  version: payload.version,
  audit_status: payload.auditStatus
})

export const listArchiveDocs = async studentId => {
  const data = await fetchJson(
    `${API_BASE}/extra/archive-docs?studentId=${studentId}`
  )
  return data.map(toClient)
}

export const createArchiveDoc = async payload => {
  const data = await fetchJson(`${API_BASE}/extra/archive-docs`, {
    method: 'POST',
    body: JSON.stringify(toServer(payload))
  })
  return toClient(data)
}

export const updateArchiveDoc = async (id, payload) => {
  const data = await fetchJson(`${API_BASE}/extra/archive-docs/${id}`, {
    method: 'PUT',
    body: JSON.stringify(toServer(payload))
  })
  return toClient(data)
}
