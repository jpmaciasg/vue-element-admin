/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const userRouter = {
  path: '/users',
  component: Layout,
  redirect: '/users/list',
  name: 'UserMenu',
  meta: {
    title: 'Usuarios',
    icon: 'user',
    roles: ['admin', 'operator', 'promotor', 'supervisor']
  },
  children: [
    {
      path: 'list',
      component: () => import('@/views/user/user-list'),
      name: 'UserListTable',
      meta: {
        title: 'Lista de usuarios',
        roles: ['admin', 'operator', 'promotor', 'supervisor']
      }
    },
    {
      path: 'dynamic-table',
      component: () => import('@/views/table/dynamic-table/index'),
      name: 'Agregar',
      meta: { title: 'Dynamic Table' }
    }/* ,
    {
      path: 'drag-table',
      component: () => import('@/views/table/drag-table'),
      name: 'DragTable',
      meta: { title: 'Drag Table' }
    },
    {
      path: 'inline-edit-table',
      component: () => import('@/views/table/inline-edit-table'),
      name: 'InlineEditTable',
      meta: { title: 'Inline Edit' }
    }*/
  ]
}
export default userRouter
