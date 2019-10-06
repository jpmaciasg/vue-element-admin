<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.search" placeholder="Usuario, nombre, apellido" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      
      
      <el-select v-model="listQuery.role" placeholder="Perfil" clearable style="width: 210px" class="filter-item" v-bind="enabledPromotorFilter">
        <el-option key="-1" label="-- Todos los perfiles --" value="0" />
        <el-option v-for="item in promotorList" :key="item.role_key" :label="item.role_label" :value="item.role_key" />
      </el-select>
      &nbsp;&nbsp;&nbsp;<span class="filter-item" style="font-weight: bold">Estado: </span>
      <!-- <el-checkbox-group class="filter-item"> -->
      <el-checkbox v-model="listQuery.act_1" label="Activo" class="filter-item" v-bind="enabledA1Filter" />
      <el-checkbox v-model="listQuery.act_0" label="Deshabilitado" class="filter-item" v-bind="enabledA0Filter" />

    


      <!-- <el-select v-model="listQuery.sort" style="width: 140px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in sortOptions" :key="item.key" :label="item.label" :value="item.key" />
      </el-select> -->
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        Buscar
      </el-button>
      <!-- <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        Add
      </el-button> -->
      <!-- <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-download" @click="handleDownload">
        Exportar
      </el-button> -->
      <el-button v-waves class="filter-item" type="primary" @click="handleReset">
        Borrar filtros
      </el-button>

    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
      :row-class-name="tableRowClassName"
      lazy
      @sort-change="sortChange"
    >
      <el-table-column label="ID" prop="id" sortable="custom" align="left" width="80">
        <template slot-scope="scope">
          <span>{{ scope.row.id }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Usuario" width="180px" align="left">
        <template slot-scope="scope">
          <span>{{ scope.row.username }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Nombre" sortable="custom" align="left" width="400">
        <template slot-scope="scope">
          <span>{{ scope.row.first_name }} {{ scope.row.last_name }} </span>
        </template>
      </el-table-column>
      
      <el-table-column label="Perfil" min-width="100px">
        <template slot-scope="scope">
          <span>{{ scope.row.role_label }}</span>
        </template>
      </el-table-column>




      <el-table-column label="Estatus" class-name="status-col" width="120">
        <template slot-scope="{row}">
          <el-tag :type="row.is_active | statusIFilter">
            {{ row.is_active | statusText }}
          </el-tag>
        </template>
      </el-table-column>



      <el-table-column label=" " align="center" width="100" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <router-link :to="'/users/edit/'+row.id">
            <el-button type="primary" size="small" icon="el-icon-edit">
              Ver
            </el-button>
          </router-link>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total>0"
      :total="total"
      :page.sync="listQuery.page"
      :limit.sync="listQuery.limit"
      @pagination="getList"
    />
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
import { fetchList, fetchRolesList } from '@/api/user'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import { mapGetters, mapMutations, mapActions } from 'vuex'

// arr to obj, such as { CN : "China", US : "USA" 

export default {
  name: 'UserList',
  components: { Pagination },
  directives: { waves },
  filters: {
    statusPFilter(status) {
      const statusPMap = {
        '1': 'success',
        '3': 'info',
        '2': 'danger'
      }
      return statusPMap[status]
    },
    statusIFilter(status) {
      const statusMap = {
        true: 'success',
        false: 'danger'
      }
      return statusMap[status]
    },
    statusPText(status) {
      const statusPTextMap = {
        '1': 'Pagada',
        '2': 'No pagada',
        '3': 'Confirmar'
      }
      return statusPTextMap[status]
    },
    statusText(status) {
      const statusTextMap = {
        true: 'Activo',
        false: 'Inhabilitado'
      }
      return statusTextMap[status]
    },
    typeFilter(type) {
      return calendarTypeKeyValue[type]
    },
/*,
    daysCount(value,start,status) {
        var dif;
        var d2;
        var d1= new Date(start);
        console.log(d1);

        if(status==1){
            d2=new Date(value);
            console.log(d2);
        }
        else{
            d2=new Date();
        }
        dif=Math.round((d2.getTime()-d1.getTime())/(1000*60*60*24));
        return  dif;
    }*/
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
    limit: 20,
    role: undefined,
    search: '',
    act_1: false, // true
    act_0: false, // false
    sort: 'first_name',
    //export: '',
  },
      // importanceOptions: [{ label: 'ID Ascending', key: '1' }, { label: 'ID Descending', key: '2' }, { label: 'Por confirmar', key: '2' }],
      // sortOptions: [{ label: 'ID Ascending', key: '+id' }, { label: 'ID Descending', key: '-id' }],
      statusOptions: ['published', 'draft', 'deleted'],
      // showReviewer: false,
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Edit',
        create: 'Create'
      },
      dialogPvVisible: false,
      pvData: [],
      downloadLoading: false,
      unpaidDate: '',
      promotorList: [],
      showPaidInvoices: false,
      currentRole: '',
      filterPermissions: {},
      userid: 0
    }
  },
  created() {
    // return this.$store.state.tagsView.cachedViews
    //console.log('created')
    //console.log(this.query)
    this.listQuery=Object.assign({}, this.queryu) || {
    page: 1,
    limit: 20,
    role: undefined,
    search: '',
    act_1: false, // true
    act_0: false, // false
    sort: 'first_name',
    //export: '',
  }
    this.filterOptions()
    this.getTotalRows()
    // this.getSumInvoices()
    // this.getPaymentsInvoices()
    this.getPromotors()

    if (this.roles.includes('admin')) {
      this.currentRole = 'admin'
    }
    if (this.roles.includes('operator')) {
      this.currentRole = 'operator'
    }
    if (this.roles.includes('promotor')) {
      this.currentRole = 'promotor'
    }
    if (this.roles.includes('executive')) {
      this.currentRole = 'executive'
    }
    if (this.roles.includes('supervisor')) {
      this.currentRole = 'supervisor'
    }

    //console.log('uid')
    this.userid = this.$store.state.user.userid
    //console.log(this.userid)
    // this.filterOptions()
    this.filterPermissions = this.filterRolePermissions
  },
  methods: {
      ...mapMutations({
          'SET_QUERYU': 'search/SET_QUERYU'
  }),
      ...mapActions({               // Add this
      'saveQueryU': 'search/saveQueryU'
  }),
    saveQueryParams: function(){
        //console.log('in save params')
        //console.log(this.listQuery)
        this.SET_QUERYU(this.listQuery);
        //console.log('after save')
        //console.log(this.listQuery)
        //console.log('after save, query:')
        //console.log(this.query)
    },
    getMinDate() {
      var params = {
        from: this.yearNow + '-' + this.monthNow + '-01',
        to: this.yearNow + '-' + this.monthNow + '-' + this.dayLast
      }
      fetchFirstUnpaidDate(params).then(response => {
        this.listQuery.from = JSON.parse(response.data)
        this.unpaidDate = this.listQuery.from
      })
    },
    getPromotors() {
      // this.listLoading = true
      fetchRolesList().then(response => {
        this.promotorList = response.data

        // Just to simulate the time of the request
        /* setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000) */
      })
    },
    getList() {
      this.listLoading = true
      this.saveQueryParams()
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
    getTotalRows() {
      this.listLoading = true
this.getList();
      // console.log('antes count');
      // console.log(this.listQuery);
      //fetchList(this.listQuery).then(response => {
        // this.list = response.data
       // this.total = parseInt(response.data)
        //console.log('got count' + this.total)

        //this.getList()
        // this.listLoading = false

        // Just to simulate the time of the request
        /* setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000) */
      //})
    },
    handleReset() {
        this.listQuery.search=''
        this.listQuery.limit=20
this.listQuery.page=1
        this.listQuery.sort='first_name'
        this.listQuery.role=undefined




    this.listQuery.act_1= false, // true
    this.listQuery.act_0= false, // false


      this.filterOptions()
      this.getTotalRows()
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getTotalRows()
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
      if (prop === 'id') {
        this.sortByID(order)
      }
    },
    sortByID(order) {
      if (order === 'ascending') {
        this.listQuery.sort = 'id'
      } else {
        this.listQuery.sort = '-id'
      }
      this.handleFilter()
    },
    handleCreate() {
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
      this.listQuery['payedrows'] = '' JP*/
      //this.listQuery = Object.assign({}, this.$store.state.search.query)

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
      //this.saveQuery()

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
      'queryu'
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
    },
    fo() {
      var foGeneral = {
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
      if (this.currentRole == 'promotor') {
        foGeneral['promotor'] = this.$store.state.user.userid
        foGeneral['pay_1'] = false
        foGeneral['pay_2'] = true
        foGeneral['pay_3'] = false
        foGeneral['act_0'] = false
        foGeneral['act_1'] = true
      }
      if (this.currentRole == 'operator') {
        foGeneral['promotor'] = undefined
        foGeneral['pay_1'] = false
        foGeneral['pay_2'] = true // true
        foGeneral['pay_3'] = false
        foGeneral['act_0'] = false
        foGeneral['act_1'] = true // true
      }
      if (this.roles.includes('admin')) {

      }
      if (this.currentRole == 'executive') {

      }
      if (this.currentRole == 'supervisor') {
        foGeneral['promotor'] = undefined
        foGeneral['pay_1'] = false
        foGeneral['pay_2'] = true
        foGeneral['pay_3'] = false
        foGeneral['act_0'] = false
        foGeneral['act_1'] = true
      }
      // console.log(filterOptionsGeneral);
      return foGeneral
    }
  }
}
</script>
