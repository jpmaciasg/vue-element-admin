/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const clientRouter = {
  path: '/clients',
  component: Layout,
  redirect: '/clients/list',
  name: 'ClientMenu',
  meta: {
    title: 'Clientes',
    icon: 'peoples'
  },
  children: [
    {
      path: 'list',
      component: () => import('@/views/table/complex-table'),
      name: 'ComplexTable',
      meta: {
        title: 'Listado',
        roles: ['admin', 'operator', 'promotor', 'supervisor']
      }
    },
    {
      path: 'add',
      component: () => import('@/views/table/dynamic-table/index'),
      name: 'Agregar',
      meta: { title: 'Dynamic Table' }
    },
    {
      path: 'import',
      component: () => import('@/views/table/drag-table'),
      name: 'Importar',
      meta: { title: 'Drag Table' }
    } /* ,
     {
      path: 'inline-edit-table',
      component: () => import('@/views/table/inline-edit-table'),
      name: 'InlineEditTable',
      meta: { title: 'Inline Edit' }
    } */
  ]
}
export default clientRouter
