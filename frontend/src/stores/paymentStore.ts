import { create } from 'zustand'

export type CheckoutStep =
  | 'idle'
  | 'creating'
  | 'redirecting'
  | 'processing'
  | 'approved'
  | 'rejected'
  | 'error'

export type PaymentStatus = 'pending' | 'approved' | 'rejected' | 'in_process' | 'cancelled' | 'refunded' | 'error' | null

interface PaymentState {
  checkoutStep: CheckoutStep
  preferenceId: string | null
  pedidoId: number | null
  paymentStatus: PaymentStatus
  statusDetail: string | null
  error: string | null
  timeoutId: number | null
  startCheckout: (pedidoId: number) => void
  setPreference: (preferenceId: string) => void
  updatePaymentStatus: (status: PaymentStatus, statusDetail?: string) => void
  resetPayment: () => void
}

export const usePaymentStore = create<PaymentState>()((set, get) => ({
  checkoutStep: 'idle',
  preferenceId: null,
  pedidoId: null,
  paymentStatus: null,
  statusDetail: null,
  error: null,
  timeoutId: null,
  startCheckout: (pedidoId) => {
    const { timeoutId: prevTimeoutId } = get()
    if (prevTimeoutId !== null) {
      clearTimeout(prevTimeoutId)
    }
    set({
      checkoutStep: 'creating',
      preferenceId: null,
      pedidoId,
      paymentStatus: null,
      statusDetail: null,
      error: null,
      timeoutId: null,
    })
  },
  setPreference: (preferenceId) => {
    const { timeoutId: prevTimeoutId } = get()
    if (prevTimeoutId !== null) {
      clearTimeout(prevTimeoutId)
    }
    const timeoutId = window.setTimeout(() => {
      const state = usePaymentStore.getState()
      if (state.checkoutStep === 'redirecting') {
        state.updatePaymentStatus('cancelled', 'timeout')
      }
    }, 30000)
    set({
      checkoutStep: 'redirecting',
      preferenceId,
      timeoutId,
    })
  },
  updatePaymentStatus: (status, statusDetail) => {
    const { timeoutId } = get()
    if (timeoutId !== null) {
      clearTimeout(timeoutId)
    }
    let checkoutStep: CheckoutStep = 'processing'
    if (status === 'approved') checkoutStep = 'approved'
    else if (status === 'rejected') checkoutStep = 'rejected'
    else if (status === 'error') checkoutStep = 'error'
    else if (status === 'in_process') checkoutStep = 'processing'
    else if (status === 'cancelled' || status === 'refunded') checkoutStep = 'rejected'
    set({
      checkoutStep,
      paymentStatus: status,
      statusDetail: statusDetail ?? null,
      timeoutId: null,
    })
  },
  resetPayment: () =>
    set({
      checkoutStep: 'idle',
      preferenceId: null,
      pedidoId: null,
      paymentStatus: null,
      statusDetail: null,
      error: null,
      timeoutId: null,
    }),
}))