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
  paymentStatus: PaymentStatus
  statusDetail: string | null
  error: string | null
  startCheckout: (pedidoId: number) => void
  setPreference: (preferenceId: string) => void
  updatePaymentStatus: (status: PaymentStatus, statusDetail?: string) => void
  resetPayment: () => void
}

export const usePaymentStore = create<PaymentState>()((set) => ({
  checkoutStep: 'idle',
  preferenceId: null,
  paymentStatus: null,
  statusDetail: null,
  error: null,
  startCheckout: () =>
    set({
      checkoutStep: 'creating',
      preferenceId: null,
      paymentStatus: null,
      statusDetail: null,
      error: null,
    }),
  setPreference: (preferenceId) =>
    set({
      checkoutStep: 'redirecting',
      preferenceId,
    }),
  updatePaymentStatus: (status, statusDetail) => {
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
    })
  },
  resetPayment: () =>
    set({
      checkoutStep: 'idle',
      preferenceId: null,
      paymentStatus: null,
      statusDetail: null,
      error: null,
    }),
}))