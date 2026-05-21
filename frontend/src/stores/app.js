import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', {
  state: () => ({
    homeSlide: 0,
  }),
})
