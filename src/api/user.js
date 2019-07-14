import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/user/login',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/user/info',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/user/logout',
    method: 'post'
  })
}

export function fetchList(query) {
    return request({
      url: '/user/list',
      method: 'get',
      params: query
    })
  }

  export function fetchRolesList() {
    return request({
      url: '/user/roles',
      method: 'get'
    })
  }
  
