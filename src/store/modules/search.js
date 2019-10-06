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
  },
  queryu: Cookies.getJSON('queryu') || {
    page: 1,
    limit: 20,
    role: undefined,
    search: '',
    act_1: false, // true
    act_0: false, // false
    sort: 'first_name',
    //export: '',
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
  },
  SET_QUERYU: (state, query) => {
    //console.log('en set_query');
    //console.log(query);
  state.queryu = Object.assign({}, query)//query
  //console.log('after assign')
  //console.log(state.query)
  Cookies.set('queryu', state.queryu)
}
}

const actions = {
  saveQuery({ commit, query }) {
    commit('SET_QUERY', query)
  },
  saveQueryU({ commit, query }) {
    commit('SET_QUERYU', query)
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
