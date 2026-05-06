import { useStore } from '../store/useStore'

export function ChartViewer() {
  const { imageDataUrl } = useStore()
  if (!imageDataUrl) return null

  return (
    <div className="overflow-hidden rounded-2xl border border-zinc-200 bg-white shadow-sm">
      <div className="border-b border-zinc-200 px-5 py-3 text-sm font-medium text-zinc-900">업로드된 이미지</div>
      <div className="p-4">
        <img
          src={imageDataUrl}
          alt="uploaded chart"
          className="max-h-[360px] w-full rounded-xl object-contain"
        />
      </div>
    </div>
  )
}

