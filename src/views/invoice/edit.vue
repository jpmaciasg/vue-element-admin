<template>
  <invoice-detail :is-edit="true" />
</template>

<script>
import InvoiceDetail from './components/InvoiceDetail'

export default {
  name: 'EditForm',
  components: { InvoiceDetail }
}
</script>

