import { create } from 'zustand'
import type { PredictResponse } from '../types'

type StoreState = {
  loading: boolean
  error?: string
  imageDataUrl?: string
  result?: PredictResponse
  setLoading: (v: boolean) => void
  setError: (e?: string) => void
  setImage: (dataUrl?: string) => void
  setResult: (r?: PredictResponse) => void
  reset: () => void
}

export const useStore = create<StoreState>((set) => ({
  loading: false,
  error: undefined,
  imageDataUrl: undefined,
  result: undefined,
  setLoading: (v) => set({ loading: v }),
  setError: (e) => set({ error: e }),
  setImage: (dataUrl) => set({ imageDataUrl: dataUrl }),
  setResult: (r) => set({ result: r }),
  reset: () => set({ loading: false, error: undefined, imageDataUrl: undefined, result: undefined }),
}))

