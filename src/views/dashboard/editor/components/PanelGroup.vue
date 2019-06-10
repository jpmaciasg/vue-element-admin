<template>
  <el-row :gutter="40" class="panel-group">
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel">
        <div class="card-panel-icon-wrapper icon-people">
          <svg-icon icon-class="money" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            Ingresos <br>
            del mes
          </div>
          <count-to :start-val="0" :end-val="topEarnedMonth" :duration="1000" class="card-panel-num" />
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel">
        <div class="card-panel-icon-wrapper icon-message">
          <svg-icon icon-class="excel" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            Facturas <br>del mes
          </div>
          <count-to :start-val="0" :end-val="topInvoicedMonth" :duration="1000" class="card-panel-num" />
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel">
        <div class="card-panel-icon-wrapper icon-money">
          <svg-icon icon-class="money" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            Ingresos <br> hoy
          </div>
          <count-to :start-val="0" :end-val="topEarnedToday" :duration="1000" class="card-panel-num" />
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :lg="6" class="card-panel-col">
      <div class="card-panel">
        <div class="card-panel-icon-wrapper icon-shopping">
          <svg-icon icon-class="excel" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            Facturas <br>hoy
          </div>
          <count-to :start-val="0" :end-val="topInvoicedToday" :duration="1000" class="card-panel-num" />
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script>
import CountTo from 'vue-count-to'
import { fetchTopEarned, fetchTopInvoiced } from '@/api/invoice'

export default {
  components: {
    CountTo
  },
  data() {
    return {
      topEarnedMonth: 0,
      topInvoicedMonth: 0,
      topEarnedToday: 0,
      topInvoicedToday: 0
    }
  },
  computed: {
    dayNow: function() {
      var dateObject = new Date()
      var dd = dateObject.getDate()
      if (dd < 10) {
        dd = '0' + dd
      }
      return dd
    },
    dayLast: function() {
      var dateObject = new Date()
      var month = dateObject.getMonth() + 1
      var year = this.yearNow
      var d = new Date(year, month, 0)

      var dd = d.getDate()
      return dd
    },
    monthNow: function() {
      var dateObject = new Date()
      var mm = dateObject.getMonth() + 1
      if (mm < 10) {
        mm = '0' + mm
      }
      return mm
    },
    yearNow: function() {
      var dateObject = new Date()
      var yyyy = dateObject.getFullYear()
      return yyyy
    }
  },
  created() {
    this.getEarnedToday()
    this.getInvoicedToday()
    this.getEarnedMonth()
    this.getInvoicedMonth()
  },
  methods: {
    handleSetLineChartData(type) {
      this.$emit('handleSetLineChartData', type)
    },
    getEarnedToday() {
      var params = {
        from: this.yearNow + '-' + this.monthNow + '-' + this.dayNow,
        to: this.yearNow + '-' + this.monthNow + '-' + this.dayNow
      }
      fetchTopEarned(params).then(response => {
        this.topEarnedToday = JSON.parse(response.data)
      })
    },
    getInvoicedToday() {
      var params = {
        from: this.yearNow + '-' + this.monthNow + '-' + this.dayNow,
        to: this.yearNow + '-' + this.monthNow + '-' + this.dayNow
      }
      fetchTopInvoiced(params).then(response => {
        this.topInvoicedToday = JSON.parse(response.data)
      })
    },
    getEarnedMonth() {
      var params = {
        from: this.yearNow + '-' + this.monthNow + '-01',
        to: this.yearNow + '-' + this.monthNow + '-' + this.dayLast
      }
      fetchTopEarned(params).then(response => {
        this.topEarnedMonth = parseInt(JSON.parse(response.data))
      })
    },
    getInvoicedMonth() {
      var params = {
        from: this.yearNow + '-' + this.monthNow + '-01',
        to: this.yearNow + '-' + this.monthNow + '-' + this.dayLast
      }
      fetchTopInvoiced(params).then(response => {
        this.topInvoicedMonth = JSON.parse(response.data)
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.panel-group {
  margin-top: 18px;

  .card-panel-col {
    margin-bottom: 32px;
  }

  .card-panel {
    height: 108px;
    cursor: pointer;
    font-size: 12px;
    position: relative;
    overflow: hidden;
    color: #666;
    background: #fff;
    box-shadow: 4px 4px 40px rgba(0, 0, 0, .05);
    border-color: rgba(0, 0, 0, .05);

    &:hover {
      .card-panel-icon-wrapper {
        color: #fff;
      }

      .icon-people {
        background: #40c9c6;
      }

      .icon-message {
        background: #36a3f7;
      }

      .icon-money {
        background: #f4516c;
      }

      .icon-shopping {
        background: #34bfa3
      }
    }

    .icon-people {
      color: #40c9c6;
    }

    .icon-message {
      color: #36a3f7;
    }

    .icon-money {
      color: #f4516c;
    }

    .icon-shopping {
      color: #34bfa3
    }

    .card-panel-icon-wrapper {
      float: left;
      margin: 14px 0 0 14px;
      padding: 16px;
      transition: all 0.38s ease-out;
      border-radius: 6px;
    }

    .card-panel-icon {
      float: left;
      font-size: 48px;
    }

    .card-panel-description {
      float: right;
      font-weight: bold;
      margin: 26px;
      margin-left: 0px;

      .card-panel-text {
        line-height: 18px;
        color: rgba(0, 0, 0, 0.45);
        font-size: 16px;
        margin-bottom: 12px;
      }

      .card-panel-num {
        font-size: 20px;
      }
    }
  }
}

@media (max-width:550px) {
  .card-panel-description {
    display: none;
  }

  .card-panel-icon-wrapper {
    float: none !important;
    width: 100%;
    height: 100%;
    margin: 0 !important;

    .svg-icon {
      display: block;
      margin: 14px auto !important;
      float: none !important;
    }
  }
}
</style>
