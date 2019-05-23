<template>
  <div class="dashboard-container">
    <component :is="currentRole" />
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import adminDashboard from './admin'
import operatorDashboard from './operator'
import promotorDashboard from './promotor'
import executiveDashboard from './executive'
import supervisorDashboard from './supervisor'

export default {
  name: 'Dashboard',
  components: { adminDashboard, operatorDashboard, promotorDashboard, executiveDashboard, supervisorDashboard },
  data() {
    return {
      currentRole: 'adminDashboard'
    }
  },
  computed: {
    ...mapGetters([
      'roles'
    ])
  },
  created() {
    if (this.roles.includes('admin')) {
      this.currentRole = 'adminDashboard'
    }
    if (this.roles.includes('operator')) {
      this.currentRole = 'operatorDashboard'
    }
    if (this.roles.includes('promotor')) {
      this.currentRole = 'promotorDashboard'
    }
    if (this.roles.includes('executive')) {
      this.currentRole = 'executiveDashboard'
    }
    if (this.roles.includes('supervisor')) {
      this.currentRole = 'supervisorDashboard'
    }
  }
}
</script>
