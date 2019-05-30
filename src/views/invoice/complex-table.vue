<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.search" placeholder="RFC, cliente, factura" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <!-- <el-select v-model="listQuery.type" placeholder="Type" clearable class="filter-item" style="width: 130px">
        <el-option v-for="item in calendarTypeOptions" :key="item.key" :label="item.display_name+'('+item.key+')'" :value="item.key" />
      </el-select> -->
      <span style="font-size:12px;" class="filter-item">(Deuda más antigua: {{ unpaidDate }})</span>
      <el-date-picker v-model="listQuery.from" type="date" placeholder="Fecha inicial" class="filter-item" />
      <el-date-picker v-model="listQuery.to" type="date" placeholder="Fecha final" class="filter-item" />
      <el-select v-model="listQuery.promotor" placeholder="Promotor" clearable style="width: 210px" class="filter-item">
        <!--  <el-option key="0" label="-- Seleccionar --" value="" /> -->
        <el-option v-for="item in promotorList" :key="item.id" :label="item.first_name + ' ' + item.last_name" :value="item.id" />
      </el-select>
      <br>

      <span class="filter-item" style="font-weight: bold">Pagos: </span>
      <!-- <el-checkbox-group class="filter-item"> -->
      <el-checkbox v-model="listQuery.pay_1" label="Pagada" class="filter-item" />
      <el-checkbox v-model="listQuery.pay_3" label="Por confirmar" class="filter-item" />
      <el-checkbox v-model="listQuery.pay_2" label="No pagada" class="filter-item" />

      <!-- </el-checkbox-group> -->

<!--
      <el-radio-group v-model="listQuery.payment" class="filter-item"> Test
      <el-radio label="Pagada"></el-radio>
      <el-radio label="Por confirmar"></el-radio>
      <el-radio label="No pagada"></el-radio>
      <el-radio label="Omitir"></el-radio>
      </el-radio-group> -->

      &nbsp;&nbsp;&nbsp;<span class="filter-item" style="font-weight: bold">Estado: </span>
      <!-- <el-checkbox-group class="filter-item"> -->
      <el-checkbox v-model="listQuery.act_1" label="Activa" class="filter-item" />
      <el-checkbox v-model="listQuery.act_0" label="Cancelada" class="filter-item" />
      <!--  </el-checkbox-group> -->
      <!--
    </el-checkbox-group>
      <el-radio-group v-model="listQuery.active" class="filter-item">
      <el-radio label="Activa"></el-radio>
      <el-radio label="Cancelada"></el-radio>
      <el-radio label="Omitir"></el-radio>
      </el-radio-group> -->
      <br>
      <div v-if="currentRole=='admin' || currentRole == 'executive'">
        <span style="font-size:12px;" class="filter-item">Fecha pago:</span>
        <el-date-picker v-model="listQuery.fromp" type="date" placeholder="Fecha inicial" class="filter-item" />
        <el-date-picker v-model="listQuery.top" type="date" placeholder="Fecha final" class="filter-item" />
        <br>
      </div>

      <!-- <el-select v-model="listQuery.sort" style="width: 140px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in sortOptions" :key="item.key" :label="item.label" :value="item.key" />
      </el-select> -->
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        Buscar
      </el-button>
      <!-- <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        Add
      </el-button> -->
      <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-download" @click="handleDownload">
        Exportar
      </el-button>
      <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" @click="handleReset">
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
      @sort-change="sortChange"
    >
      <el-table-column label="ID" prop="fac_key" sortable="custom" align="center" width="80">
        <template slot-scope="scope">
          <span>{{ scope.row.fac_key }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Factura" sortable="custom" align="center" width="100">
        <template slot-scope="scope">
          <span>{{ scope.row.fac_serie }} {{ scope.row.fac_folio }} </span>
        </template>
      </el-table-column>
      <el-table-column label="Fecha" width="150px" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.fac_fecha | parseTime('{y}-{m}-{d} {h}:{i}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Cliente" min-width="200px">
        <!-- <template slot-scope="{row}">
          <span class="link-type" @click="handleUpdate(row)">{{ row.fac_receptornombre }}</span>
          <el-tag>{{ row.type | typeFilter }}</el-tag>
        </template> -->
        <template slot-scope="scope">
          <span>{{ scope.row.fac_receptornombre }}<br>{{ scope.row.fac_receptorrfc }}</span>
        </template>
      </el-table-column>
      <el-table-column label="Total" width="120px" align="center">
        <template slot-scope="scope">
          <span>Total: {{ scope.row.fac_total | parseMoney }}</span><br><span>Pagado: {{ scope.row.fac_payments }}</span><br><span>Deuda: {{ scope.row.fac_debt }}</span>
        </template>
      </el-table-column>
      <!-- <el-table-column v-if="showReviewer" label="Reviewer" width="110px" align="center">
        <template slot-scope="scope">
          <span style="color:red;">{{ scope.row.reviewer }}</span>
        </template>
      </el-table-column> -->
      <!-- <el-table-column label="Imp" width="80px">
        <template slot-scope="scope">
          <svg-icon v-for="n in +scope.row.importance" :key="n" icon-class="star" class="meta-item__icon" />
        </template>
      </el-table-column> -->
      <!-- <el-table-column label="Readings" align="center" width="95">
        <template slot-scope="{row}">
          <span v-if="row.pageviews" class="link-type" @click="handleFetchPv(row.pageviews)">{{ row.pageviews }}</span>
          <span v-else>0</span>
        </template>
      </el-table-column> -->
      <el-table-column label="Estado" class-name="status-col" width="120">
        <template slot-scope="{row}">
          <el-tag :type="row.fac_pagada | statusFilter">
            {{ row.fac_pagada | statusText }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label=" " align="center" width="100" class-name="small-padding fixed-width">
        <template slot-scope="{row}">
          <router-link :to="'/invoices/edit/'+row.fac_key">
            <el-button type="primary" size="small" icon="el-icon-edit">
              Ver
            </el-button>
          </router-link>
          <!-- <el-button type="primary" size="mini" @click="handleUpdate(row)">
            Ver
          </el-button> -->
          <!-- <el-button v-if="row.status!='1'" size="mini" type="success" @click="handleModifyStatus(row,'published')">
            Pagada
          </el-button>
          <el-button v-if="row.status!='3'" size="mini" @click="handleModifyStatus(row,'draft')">
            Confirmar
          </el-button>
          <el-button v-if="row.status!='2'" size="mini" type="danger" @click="handleModifyStatus(row,'deleted')">
            No Pagada
          </el-button> -->
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

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="70px" style="width: 400px; margin-left:50px;">
        <el-form-item label="Type" prop="type">
          <el-select v-model="temp.type" class="filter-item" placeholder="Please select">
            <el-option v-for="item in calendarTypeOptions" :key="item.key" :label="item.display_name" :value="item.key" />
          </el-select>
        </el-form-item>
        <el-form-item label="Date" prop="timestamp">
          <el-date-picker v-model="temp.timestamp" type="datetime" placeholder="Please pick a date" />
        </el-form-item>
        <el-form-item label="Title" prop="title">
          <el-input v-model="temp.title" />
        </el-form-item>
        <el-form-item label="Status">
          <el-select v-model="temp.status" class="filter-item" placeholder="Please select">
            <el-option v-for="item in statusOptions" :key="item" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item label="Imp">
          <el-rate v-model="temp.importance" :colors="['#99A9BF', '#F7BA2A', '#FF9900']" :max="3" style="margin-top:8px;" />
        </el-form-item>
        <el-form-item label="Remark">
          <el-input v-model="temp.remark" :autosize="{ minRows: 2, maxRows: 4}" type="textarea" placeholder="Please input" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          Cancel
        </el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">
          Confirm
        </el-button>
      </div>
    </el-dialog>

    <el-dialog :visible.sync="dialogPvVisible" title="Reading statistics">
      <el-table :data="pvData" border fit highlight-current-row style="width: 100%">
        <el-table-column prop="key" label="Channel" />
        <el-table-column prop="pv" label="Pv" />
      </el-table>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogPvVisible = false">Confirm</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { fetchList, fetchPv, updateArticle, fetchFirstUnpaidDate, fetchPromotorsList } from '@/api/invoice'
import waves from '@/directive/waves' // waves directive
import { parseTime, parseMoney } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import { mapGetters } from 'vuex'

const calendarTypeOptions = [
  { key: 'CN', display_name: 'China' },
  { key: 'US', display_name: 'USA' },
  { key: 'JP', display_name: 'Japan' },
  { key: 'EU', display_name: 'Eurozone' }
]

// arr to obj, such as { CN : "China", US : "USA" }
const calendarTypeKeyValue = calendarTypeOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'InvoiceListTable',
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        '1': 'success',
        '3': 'info',
        '2': 'danger'
      }
      return statusMap[status]
    },
    statusText(status) {
      const statusTextMap = {
        '1': 'Pagada',
        '2': 'No pagada',
        '3': 'Confirmar'
      }
      return statusTextMap[status]
    },
    typeFilter(type) {
      return calendarTypeKeyValue[type]
    }
  },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        promotor: undefined,
        search: '',
        pay_1: false,
        pay_2: true,
        pay_3: true,
        act_1: true,
        act_0: false,
        sort: '-fac_fecha',
        from: undefined,
        to: undefined,
        fromp: undefined,
        top: undefined,
        export: '',
        countrows: ''
      },
      importanceOptions: [{ label: 'ID Ascending', key: '1' }, { label: 'ID Descending', key: '2' }, { label: 'Por confirmar', key: '2' }],
      calendarTypeOptions,
      sortOptions: [{ label: 'ID Ascending', key: '+id' }, { label: 'ID Descending', key: '-id' }],
      statusOptions: ['published', 'draft', 'deleted'],
      showReviewer: false,
      temp: {
        id: undefined,
        importance: 1,
        remark: '',
        timestamp: new Date(),
        title: '',
        type: '',
        status: 'published'
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Edit',
        create: 'Create'
      },
      dialogPvVisible: false,
      pvData: [],
      rules: {
        type: [{ required: true, message: 'type is required', trigger: 'change' }],
        timestamp: [{ type: 'date', required: true, message: 'timestamp is required', trigger: 'change' }],
        title: [{ required: true, message: 'title is required', trigger: 'blur' }]
      },
      downloadLoading: false,
      unpaidDate: '',
      promotorList: [],
      showPaidInvoices: false,
      currentRole: ''
    }
  },
  created() {
    // return this.$store.state.tagsView.cachedViews
    this.getTotalRows()
    this.getPromotors()
    this.getMinDate()

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
    console.log(this.currentRole)
  },
  methods: {
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
      fetchPromotorsList().then(response => {
        this.promotorList = response.data

        // Just to simulate the time of the request
        /* setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000) */
      })
    },
    getList() {
      this.listLoading = true
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
      this.listQuery.countrows = '1'
      fetchList(this.listQuery).then(response => {
        // this.list = response.data
        this.total = parseInt(response.data)
        this.listQuery.countrows = ''
        this.getList()
        // this.listLoading = false

        // Just to simulate the time of the request
        /* setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000) */
      })
    },
    handleReset() {
      var r = {
        page: 1,
        limit: 20,
        promotor: undefined,
        search: '',
        pay_1: false,
        pay_2: true,
        pay_3: true,
        act_1: true,
        act_0: false,
        sort: '-fac_fecha',
        from: undefined,
        to: undefined,
        fromp: undefined,
        top: undefined,
        export: '',
        countrows: ''
      }
      this.listQuery = r
      // this.listQuery.page = 1
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
          const tHeader = ['FACTURA', 'FECHA', 'CLIENTE', 'RFC', 'TOTAL', 'PAGADO', 'DEUDA', 'ESTATUS']
          const filterVal = ['fac_folio', 'fac_fecha', 'fac_receptornombre', 'fac_receptorrfc', 'fac_total', 'fac_payments', 'fac_debt', 'fac_pagadatext']
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
    }
  },
  computed: {
    ...mapGetters([
      'roles'
    ])
  }
}
</script>
