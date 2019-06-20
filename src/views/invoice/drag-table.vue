<template>
  <div class="missing-container">
    <el-row>
      <template v-for="r in missing">
        <el-card class="box-card" style="width: 130px;float:left;margin:10px;">
          <div class="single-label">{{ r.fac_serie }} {{ r.fac_folio }}<br></div>
        </el-card>
      </template>
    </el-row>
  </div>

</template>

<script>
import { getMissingInvoices } from '@/api/invoice'

export default {
  name: 'MissingInvoices',
  data() {
    return {
      missing: [],
      listLoading: false
    }
  },
  created() {
    // console.log('created');
    this.getMissingList()
  },
  methods: {
    getMissingList() {
      this.listLoading = true
      console.log('antes mis')
      getMissingInvoices().then(response => {
        console.log(response.data)
        this.missing = JSON.parse(response.data)
      		this.listLoading = false
      }).catch(err => {
        console.log(err)

        this.$notify({
          title: 'Error',
          message: 'Error al obtener facturas faltantes',
          type: 'warning',
          duration: 2000
        })
      })
    }
  }
}
</script>

<style>
.sortable-ghost{
  opacity: .8;
  color: #fff!important;
  background: #42b983!important;
}
</style>

<style scoped>
.icon-star{
  margin-right:2px;
}
.drag-handler{
  width: 20px;
  height: 20px;
  cursor: pointer;
}
.show-d{
  margin-top: 15px;
}
</style>
