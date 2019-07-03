import request from '@/utils/request'

export function fetchTopEarned(query) {
  return request({
    url: '/invoice/earned',
    method: 'get',
    params: query
  })
}

export function fetchTopInvoiced(query) {
  return request({
    url: '/invoice/invoiced',
    method: 'get',
    params: query
  })
}

export function fetchList(query) {
  return request({
    url: '/invoice/list',
    method: 'get',
    params: query
  })
}

export function fetchPromotorsList() {
  return request({
    url: '/user/promotors',
    method: 'get'
  })
}

export function fetchFirstUnpaidDate() {
  return request({
    url: '/invoice/firstunpaiddate',
    method: 'get'
  })
}

export function fetchInvoice(id) {
  return request({
    url: '/invoice/' + id,
    method: 'get'
  })
}

export function fetchPaymentsHistoryList(id) {
  return request({
    url: 'invoice/history/' + id,
    method: 'get'
  })
}

export function fetchEdHistoryList(id) {
  return request({
    url: 'invoice/epd/' + id,
    method: 'get'
  })
}

export function fetchLogs(id) {
  return request({
    url: 'invoice/log/' + id,
    method: 'get'
  })
}

export function deletePayment(id) {
  return request({
    url: 'invoice/history/' + id,
    method: 'delete'
  })
}
export function deleteLog(id) {
  return request({
    url: 'invoice/log/' + id,
    method: 'delete'
  })
}

/* export function fetchArticle(id) {
  return request({
    url: '/invoice/detail',
    method: 'get',
    params: { id }
  })
}

export function fetchPv(pv) {
  return request({
    url: '/article/pv',
    method: 'get',
    params: { pv }
  })
}*/

export function createArticle(data) {
  return request({
    url: '/article/create',
    method: 'post',
    data
  })
}

export function updateArticle(data) {
  return request({
    url: '/article/update',
    method: 'post',
    data
  })
}

export function updateInvoice(id, data) {
  return request({
    url: '/invoice/update/' + id,
    method: 'put',
    data
  })
}

export function addInvoicePayment(data) {
  return request({
    url: '/invoice/history',
    method: 'post',
    data
  })
}

export function addInvoiceLog(data) {
  return request({
    url: '/invoice/log',
    method: 'post',
    data
  })
}

export function getMissingInvoices() {
  return request({
    url: '/invoice/missing',
    method: 'get'
  })
}
