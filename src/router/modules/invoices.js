/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const invoiceRouter = {
  path: '/invoices',
  component: Layout,
  redirect: '/invoices/list',
  name: 'InvoiceMenu',
  meta: {
    title: 'Facturas',
    icon: 'form'
  },
  children: [
    {
      path: 'list',
      component: () => import('@/views/invoice/complex-table'),
      name: 'ComplexTable',
      meta: {
        title: 'Listado',
        roles: ['admin', 'operator', 'promotor', 'supervisor']
      }
    },
    {
      path: 'add',
      component: () => import('@/views/invoice/dynamic-table/index'),
      name: 'DynamicTable',
      meta: { title: 'Agregar facturas' }
    },
    {
      path: 'missing',
      component: () => import('@/views/invoice/drag-table'),
      name: 'DragTable',
      meta: { title: 'Faltantes' }
    }
  ]
}
export default invoiceRouter
