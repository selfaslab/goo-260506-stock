import React, { useCallback } from 'react'
import { predictFromBase64 } from '../services/api'
import { useStore } from '../store/useStore'

function fileToDataUrl(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(String(reader.result))
    reader.onerror = () => reject(new Error('FileReader failed'))
    reader.readAsDataURL(file)
  })
}

export function Upload() {
  const { loading, setLoading, setError, setImage, setResult, reset } = useStore()

  const onChange = useCallback(
    async (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0]
      if (!file) return
      reset()
      setLoading(true)
      try {
        const dataUrl = await fileToDataUrl(file)
        setImage(dataUrl)
        const r = await predictFromBase64(dataUrl)
        setResult(r)
      } catch (err) {
        setError(err instanceof Error ? err.message : String(err))
      } finally {
        setLoading(false)
      }
    },
    [reset, setError, setImage, setLoading, setResult],
  )

  return (
    <div className="rounded-2xl border border-zinc-200 bg-white p-5 shadow-sm">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <div className="text-lg font-semibold text-zinc-900">차트 이미지 업로드</div>
          <div className="text-sm text-zinc-600">PNG/JPG 권장. (MVP는 선형 차트에 최적화)</div>
        </div>
        <label className="inline-flex cursor-pointer items-center justify-center rounded-xl bg-zinc-900 px-4 py-2 text-sm font-medium text-white hover:bg-zinc-800">
          <input className="hidden" type="file" accept="image/*" onChange={onChange} disabled={loading} />
          {loading ? '분석 중...' : '업로드'}
        </label>
      </div>
    </div>
  )
}

