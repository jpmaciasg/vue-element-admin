<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.search" placeholder="Folio" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        Buscar
      </el-button>

    </div>
        <div v-if="list">
            <el-col :span="12">
            <el-card class="box-card">
                
<el-row>
                <div class="single-label">{{ list[0].fac_serie }} {{ list[0].fac_folio  }}</div>
              </el-row>
              <el-row>
                <div class="single-label">{{ list[0].fac_receptornombre }}</div>
              </el-row>
              <el-row>
                <div class="single-label">{{ list[0].fac_total | parseMoney }}</div>
              </el-row>
              <el-row>
                <div class="single-label">{{ list[0].fac_pagadatext }}</div>
              </el-row>
              <el-row>
                <div class="single-label">{{ list[0].fac_isactivetext }}</div>
              </el-row>

                
              
            </el-card>
            </el-col>
            <el-col :span="12">
            <el-card class="box-card"  style="height: 130px;">
              <el-row>
                  <div v-if="list[0].fac_complemento ">
                <div class="single-label">{{ list[0].fac_complemento }}</div>
                </div>
                <div v-else>
                Esta factura no tiene complementos.
                </div>
              </el-row>

                
              
            </el-card>
            </el-col>
            </div>
                <div v-else>
                
                </div>

  </div>
</template>
<style>
  .el-table .warning-row {
   /*background: oldlace;*/
    background: #fcebcb;
  }

  .el-table .danger-row{
    background: #ff49491a;
  }

  .el-table .success-row {
    background: #f0f9eb;
  }
</style>

<script>
import { fetchList, fetchPv, updateArticle, fetchFirstUnpaidDate, fetchPromotorsList } from '@/api/invoice'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import { mapGetters } from 'vuex'


export default {
  name: 'InvoiceComplement',
  directives: { waves },
  filters: {
    parseMoney(amount, decimalCount = 2, decimal = '.', thousands = ',') {
      try {
        decimalCount = Math.abs(decimalCount)
        decimalCount = isNaN(decimalCount) ? 2 : decimalCount

        const negativeSign = amount < 0 ? '-' : ''

        const i = parseInt(amount = Math.abs(Number(amount) || 0).toFixed(decimalCount)).toString()
        const j = (i.length > 3) ? i.length % 3 : 0

        return negativeSign + (j ? i.substr(0, j) + thousands : '') + i.substr(j).replace(/(\d{3})(?=\d)/g, '$1' + thousands) + (decimalCount ? decimal + Math.abs(amount - i).toFixed(decimalCount).slice(2) : '')
      } catch (e) {
        console.log(e)
        return ''
      }
    }
  },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: 0,
      suma: 0,
      pagado: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 1,
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
      downloadLoading: false,
      currentRole: '',
      filterPermissions: {},
      userid: 0
    }
  },
  created() {
    // return this.$store.state.tagsView.cachedViews
    //this.filterOptions()
    //this.getTotalRows()




    console.log('uid')
    this.userid = this.$store.state.user.userid
    console.log(this.userid)
    // this.filterOptions()
    //this.filterPermissions = this.filterRolePermissions
  },
  methods: {
    getList() {
      this.listLoading = true
      // console.log(this.listQuery);
      // this.$store.dispatch('search/saveQuery', this.listQuery)
      fetchList(this.listQuery).then(response => {
        this.list = response.data
        // this.total = this.list.total //response.data.total
        this.listLoading = false

        // Just to simulate the time of the request
        /* setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000) */
      })
    },
    handleReset() {
        this.list=null;
    },
    handleFilter() {
      //this.listQuery.page = 1
      //this.getTotalRows()
      console.log(this.listQuery.search);
      if (this.listQuery.search == ''){
        this.handleReset();
      }
      else{
          
          this.getList();
      }
      
    },
    handleModifyStatus(row, status) {
      this.$message({
        message: 'Éxito',
        type: 'success'
      })
      row.status = status
    },
    sortChange(data) {
      const { prop, order } = data
      if (prop === 'fac_key') {
        this.sortByID(order)
      }
    },
    sortByID(order) {
      if (order === 'ascending') {
        this.listQuery.sort = 'fac_key'
      } else {
        this.listQuery.sort = '-fac_key'
      }
      this.handleFilter()
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        importance: 1,
        remark: '',
        timestamp: new Date(),
        title: '',
        status: 'published',
        type: ''
      }
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          this.temp.id = parseInt(Math.random() * 100) + 1024 // mock a id
          this.temp.author = 'vue-element-admin'
          /* createArticle(this.temp).then(() => {
            this.list.unshift(this.temp)
            this.dialogFormVisible = false
            this.$notify({
              title: 'Success',
              message: 'Created Successfully',
              type: 'success',
              duration: 2000
            })
          }) */
        }
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.temp.timestamp = new Date(this.temp.timestamp)
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.timestamp = +new Date(tempData.timestamp) // change Thu Nov 30 2017 16:41:05 GMT+0800 (CST) to 1512031311464
          updateArticle(tempData).then(() => {
            for (const v of this.list) {
              if (v.id === this.temp.id) {
                const index = this.list.indexOf(v)
                this.list.splice(index, 1, this.temp)
                break
              }
            }
            this.dialogFormVisible = false
            this.$notify({
              title: 'Success',
              message: 'Update Successfully',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleDelete(row) {
      this.$notify({
        title: 'Success',
        message: 'Delete Successfully',
        type: 'success',
        duration: 2000
      })
      const index = this.list.indexOf(row)
      this.list.splice(index, 1)
    },
    handleFetchPv(pv) {
      fetchPv(pv).then(response => {
        this.pvData = response.data.pvData
        this.dialogPvVisible = true
      })
    },
    handleDownload() {
      this.downloadLoading = true
      this.listQuery.export = '1'
      fetchList(this.listQuery).then(response => {
        var dlist = response.data
        this.listQuery.export = ''
        // this.total = this.list.total //response.data.total
        // this.listLoading = false

        // Just to simulate the time of the request
        /* setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000) */

        import('@/vendor/Export2Excel').then(excel => {
          const tHeader = ['FECHA', 'FACTURA', 'CLIENTE', 'RFC', 'SUBTOTAL', 'IVA', 'TOTAL', 'PAGADO', 'FECHA_ESPERADA_DE_PAGO', 'ESTADO', 'ESTATUS', 'DEUDA', 'PROMOTOR']
          const filterVal = ['fac_fecha', 'fac_folio', 'fac_receptornombre', 'fac_receptorrfc', 'fac_subtotal', 'fac_iva', 'fac_total', 'fac_payments', 'fac_expectedpaymentday', 'fac_pagadatext', 'fac_isactivetext', 'fac_debt', 'username']
          const data = this.formatJson(filterVal, dlist)
          excel.export_json_to_excel({
            header: tHeader,
            data,
            filename: 'facturas'
          })
          this.downloadLoading = false
        })
      })
    },
    formatJson(filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => {
        if (j === 'fac_fecha') {
          return parseTime(v[j])
        } else {
          return v[j]
        }
      }))
    },
    filterOptions() {
      /* this.listQuery['page'] = 1
      this.listQuery['limit'] = 20
      this.listQuery['promotor'] = undefined
      this.listQuery['search'] = ''
      this.listQuery['pay_1'] = false
      this.listQuery['pay_2'] = false // true
      this.listQuery['pay_3'] = false // true
      this.listQuery['act_1'] = false // true
      this.listQuery['act_0'] = false // false
      this.listQuery['sort'] = '-fac_fecha'
      this.listQuery['from'] = undefined
      this.listQuery['to'] = undefined
      this.listQuery['fromp'] = undefined
      this.listQuery['top'] = undefined
      this.listQuery['fromc'] = undefined
      this.listQuery['toc'] = undefined
      this.listQuery['export'] = ''
      this.listQuery['countrows'] = ''
      this.listQuery['sumrows'] = ''
      this.listQuery['payedrows'] = '' */
      this.listQuery = Object.assign({}, this.$store.state.search.query)

      if (this.currentRole == 'promotor') {
        this.listQuery['promotor'] = this.$store.state.user.userid
        this.listQuery['pay_1'] = false
        this.listQuery['pay_2'] = true
        this.listQuery['pay_3'] = false
        this.listQuery['act_0'] = false
        this.listQuery['act_1'] = true
      }
      if (this.currentRole == 'operator') {
        this.listQuery['promotor'] = undefined
        this.listQuery['pay_1'] = false
        this.listQuery['pay_2'] = true // true
        this.listQuery['pay_3'] = false
        this.listQuery['act_0'] = false
        this.listQuery['act_1'] = true // true
      }
      if (this.roles.includes('admin')) {

      }
      if (this.currentRole == 'executive') {

      }
      if (this.currentRole == 'supervisor') {
        this.listQuery['promotor'] = undefined
        this.listQuery['pay_1'] = false
        this.listQuery['pay_2'] = true
        this.listQuery['pay_3'] = false
        this.listQuery['act_0'] = false
        this.listQuery['act_1'] = true
      }

    // console.log(filterOptionsGeneral);
      // return filterOptionsGeneral
    },
    tableRowClassName({ row, rowIndex }) {
      if (row.fac_expectedpaymentday === null) {
        return 'danger-row'
      } else {
        var d1 = new Date()
        var d2 = new Date(row.fac_expectedpaymentday)
        d1.setUTCHours(13)
        d2.setUTCHours(13)
        d1.setUTCMinutes(0)
        d2.setUTCMinutes(0)
        d1.setUTCSeconds(0)
        d2.setUTCSeconds(0)
        d1.setUTCMilliseconds(0)
        d2.setUTCMilliseconds(0)

        if (d1.getTime() > d2.getTime()) {
          return 'danger-row'
        } else if (d1.getTime() === d2.getTime()) {
          return 'warning-row'
        }
      }

      return ''
    },
    daysCount(value, start, status) {
      var dif
      var d2
      var d1 = new Date(start)

      if (status == 1 && value != null) {
        d2 = new Date(value)
      } else {
        d2 = new Date()
      }
      dif = Math.round((d2.getTime() - d1.getTime()) / (1000 * 60 * 60 * 24))
      return dif
    }
  },
  computed: {
    ...mapGetters([
      'roles',
      'query'
    ]),
    enabledPromotorFilter() {
      var r = {}
      if (this.filterPermissions['promotor'] == false) {
        r = { [`disabled`]: true }
      }
      return r
    },
    enabledP1Filter() {
      var r = {}
      if (this.filterPermissions['pay_1'] == false) {
        r = { [`disabled`]: true }
      }
      return r
    },
    enabledP2Filter() {
      var r = {}
      if (this.filterPermissions['pay_2'] == false) {
        r = { [`disabled`]: true }
      }
      return r
    },
    enabledP3Filter() {
      var r = {}
      if (this.filterPermissions['pay_3'] == false) {
        r = { [`disabled`]: true }
      }
      return r
    },
    enabledA0Filter() {
      var r = {}
      if (this.filterPermissions['act_0'] == false) {
        r = { [`disabled`]: true }
      }
      return r
    },
    enabledA1Filter() {
      var r = {}
      if (this.filterPermissions['act_1'] == false) {
        r = { [`disabled`]: true }
      }
      return r
    },
    filterRolePermissions() {
      var permissionsGeneral = {
        promotor: true,
        pay_1: true,
        pay_2: true,
        pay_3: true,
        act_1: true,
        act_0: true
      }
      if (this.currentRole == 'promotor') {
        permissionsGeneral['promotor'] = false
        permissionsGeneral['pay_1'] = false
        permissionsGeneral['pay_2'] = false
        permissionsGeneral['pay_3'] = false
        permissionsGeneral['act_0'] = false
        permissionsGeneral['act_1'] = false
      }
      if (this.currentRole == 'operator') {
        permissionsGeneral['promotor'] = true
        permissionsGeneral['pay_1'] = true
        permissionsGeneral['pay_2'] = true
        permissionsGeneral['pay_3'] = false
        permissionsGeneral['act_0'] = false
        permissionsGeneral['act_1'] = false
      }
      if (this.roles.includes('admin')) {

      }
      if (this.currentRole == 'executive') {

      }
      if (this.currentRole == 'supervisor') {
        permissionsGeneral['promotor'] = true
        permissionsGeneral['pay_1'] = true
        permissionsGeneral['pay_2'] = true
        permissionsGeneral['pay_3'] = false
        permissionsGeneral['act_0'] = false
        permissionsGeneral['act_1'] = false
      }

      return permissionsGeneral
    }
  }
}
</script>
