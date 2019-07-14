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
        title: 'Lista de facturas',
        roles: ['admin', 'operator', 'promotor', 'supervisor', 'executive']
      }
    },
    {
      path: 'add',
      component: () => import('@/views/invoice/dynamic-table/index'),
      name: 'InvoiceListTable',
      meta: { title: 'Agregar facturas' }
    },
    {
      path: 'missing',
      component: () => import('@/views/invoice/drag-table'),
      name: 'MissingInvoices',
      meta: { title: 'Faltantes' }
    },
    {
      path: 'edit/:id(\\d+)',
      component: () => import('@/views/invoice/edit'),
      name: 'EditInvoice',
      meta: {
        title: 'Ver factura',
        noCache: true,
        activeMenu: '/invoice/list'
      },
      hidden: true
    },
    {
        path: 'complements',
        component: () => import('@/views/invoice/invoice-complement'),
        name: 'Complements',
        meta: {
          title: 'Complementos',
          roles: ['admin', 'operator', 'promotor', 'supervisor', 'executive']
        }
    }/*,
    {
        path: 'invoicefilelog',
        component: () => import('@/views/invoice/complex-table'),
        name: 'InvoiceFileLog',
        meta: {
          title: 'Historico de archivos',
          roles: ['admin', 'operator']
        }
    }*/
  ]
}
export default invoiceRouter
