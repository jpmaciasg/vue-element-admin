import Cookies from 'js-cookie'

const state = {
  query: Cookies.get('query') || {
    page: 1,
    limit: 20,
    promotor: undefined,
    search: '',
    pay_1: false,
    pay_2: false, // true
    pay_3: false, // true
    act_1: false, // true
    act_0: false, // false
    sort: '-fac_fecha',
    from: undefined,
    to: undefined,
    fromp: undefined,
    top: undefined,
    fromc: undefined,
    toc: undefined,
    export: '',
    countrows: '',
    sumrows: '',
    payedrows: ''
  }
}

const mutations = {
  SET_QUERY: (state, query) => {
    state.query = query
    Cookies.set('query', state.query)
  }
}

const actions = {
  saveQuery({ commit, query }) {
    commit('SET_QUERY', query)
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
