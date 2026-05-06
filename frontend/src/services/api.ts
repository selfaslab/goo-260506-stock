import type { PredictResponse } from '../types'

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000'

export async function predictFromBase64(imageBase64OrDataUrl: string): Promise<PredictResponse> {
  const res = await fetch(`${API_BASE}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ image: imageBase64OrDataUrl }),
  })

  if (!res.ok) {
    let detail = `HTTP ${res.status}`
    try {
      const j = await res.json()
      detail = j?.detail ? String(j.detail) : detail
    } catch {
      // ignore
    }
    throw new Error(detail)
  }

  return (await res.json()) as PredictResponse
}

