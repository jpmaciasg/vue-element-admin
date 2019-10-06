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
        path: 'edit/:id(\\d+)',
        component: () => import('@/views/user/UserDetail'),
        name: 'EditUser',
        meta: {
          title: 'Ver usuario',
          noCache: true,
          activeMenu: '/user/list'
        },
        hidden: true
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
