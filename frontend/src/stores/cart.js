import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getCart, addToCart, updateCartItem, removeCartItem, clearCart } from '../api/cart'

export const useCartStore = defineStore('cart', () => {
  const items = ref([])
  const loading = ref(false)

  const count = computed(() => items.value.length)
  const selectedItems = computed(() => items.value.filter((i) => i.selected))
  const selectedTotal = computed(() =>
    selectedItems.value.reduce((sum, i) => sum + i.subtotal_yuan, 0)
  )

  async function fetchCart() {
    loading.value = true
    try {
      const res = await getCart()
      items.value = res.data.items
    } finally {
      loading.value = false
    }
  }

  async function addItem(skuId, quantity = 1) {
    const res = await addToCart({ sku_id: skuId, quantity })
    if (res.data?.items) items.value = res.data.items
    else await fetchCart()
  }

  async function updateItem(skuId, data) {
    const res = await updateCartItem(skuId, data)
    if (res.data?.items) items.value = res.data.items
    else await fetchCart()
  }

  async function removeItem(skuId) {
    await removeCartItem(skuId)
    items.value = items.value.filter((i) => i.sku_id !== skuId)
  }

  async function clear() {
    await clearCart()
    items.value = []
  }

  return { items, loading, count, selectedItems, selectedTotal, fetchCart, addItem, updateItem, removeItem, clear }
}, {
  persist: {
    pick: ['items'],
  },
})
