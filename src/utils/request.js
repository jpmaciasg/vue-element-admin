import axios from 'axios'
import { Message } from 'element-ui'
import store from '@/store'
import { getToken } from '@/utils/auth'

// create an axios instance
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API, // url = base url + request url
  withCredentials: false, // send cookies when cross-domain requests
  timeout: 120000 // 5000 // request timeout
})

// request interceptor
service.interceptors.request.use(
  config => {
    // do something before request is sent

    if (store.getters.token) {
      // let each request carry token
      // ['X-Token'] is a custom headers key
      // please modify it according to the actual situation
      config.headers['Authorization'] = 'Bearer ' + getToken()
    }
    return config
  },
  error => {
    // do something with request error
    console.log(error) // for debug
    return Promise.reject(error)
  }
)

// response interceptor
service.interceptors.response.use(
  /**
   * If you want to get http information such as headers or status
   * Please return  response => response
  */
  // response => response
  /**
   * Determine the request status by custom code
   * Here is just an example
   * You can also judge the status by HTTP Status Code
   */
  response => {
    const res = response.data

    // if the custom code is not 20000, it is judged as an error.
    if (response.status < 200 || response.status > 299) {
    /* Message({
        message: res.message || 'error',
        type: 'error',
        duration: 5 * 1000
      })*/

      // 50008: Illegal token; 50012: Other clients logged in; 50014: Token expired;
      if (response.status === 500) { // || res.code === 50012 || res.code === 50014) {
        // to re-login
        Message({
          message: 'Error en la aplicación',
          type: 'error',
          duration: 5 * 1000
        })
      }

      if (response.status === 404) { // || res.code === 50012 || res.code === 50014) {
        // to re-login
        Message({
          message: 'Recurso no encontrado',
          type: 'error',
          duration: 5 * 1000
        })
      }
      if (response.status === 401) { // || res.code === 50012 || res.code === 50014) {
        // to re-login
        Message({
          message: 'Sesión expirada',
          type: 'error',
          duration: 5 * 1000
        }).then(() => {
          store.dispatch('user/logout').then(() => {
            // location.reload()
          })
        })
      }
      return Promise.reject(res.message || 'error')
    } else {
      return response
    }
  },
  error => {
    console.log('err' + error) // for debug
    Message({
      message: error.message,
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service
