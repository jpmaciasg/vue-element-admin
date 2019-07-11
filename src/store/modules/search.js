import Cookies from 'js-cookie'

const state = {
  query: Cookies.getJSON('query') || {
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
      //console.log('en set_query');
      //console.log(query);
    state.query = Object.assign({}, query)//query
    //console.log('after assign')
    //console.log(state.query)
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
