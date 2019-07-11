<template>
  <div class="createPost-container">
    <el-form ref="postForm" :model="postForm" :rules="rules" class="form-container">

      <!-- <sticky :z-index="10" :class-name="'sub-navbar '+postForm.status">
        <CommentDropdown v-model="postForm.comment_disabled" />
        <PlatformDropdown v-model="postForm.platforms" />
        <SourceUrlDropdown v-model="postForm.source_uri" />
        <el-button v-loading="loading" style="margin-left: 10px;" type="success" @click="submitForm">
          Publush
        </el-button>
        <el-button v-loading="loading" type="warning" @click="draftForm">
          Draft
        </el-button>
      </sticky>
-->
      <div class="createPost-main-container">
        <el-row>
          <el-col :span="12">
            <el-card class="box-card">
              <el-row>
                <div class="single-label">{{ postForm.fac_serie }} {{ postForm.fac_folio }}<br><br></div>
              </el-row>
              <el-row>
                <el-col :span="9" class="single-label">Estatus</el-col>
                <el-col :span="10">
                  <el-switch
                    v-model="postForm.fac_isactive"
                    style="display: block"
                    active-color="#13ce66"
                    inactive-color="#ff4949"
                    active-text="Activa"
                    inactive-text="Cancelada"
                    v-bind="isActiveEstatusEditable"
                    @change="updateInvoiceStatus"
                  />

                </el-col>
              </el-row>
            </el-card>
            <el-card class="box-card">
              <div class="text item">
                {{ postForm.fac_emisornombre }}<br>
                {{ postForm.fac_emisorrfc }}
              </div>
            </el-card>
            <el-card class="box-card">
              <div class="text item">
                {{ postForm.fac_receptornombre }}<br>
                {{ postForm.fac_receptorrfc }}
              </div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card class="box-card" style="">

              <el-row>
&nbsp;
              </el-row>
              <el-row>
                <el-col :span="8" class="text item"><span class="single-label">Subtotal:</span> {{ postForm.fac_subtotal }}</el-col><el-col :span="8"><span class="single-label">IVA:</span> {{ postForm.fac_iva }}</el-col><el-col :span="8"><span class="single-label">Total:</span> {{ postForm.fac_total }}</el-col>
              </el-row>
              <el-row>
&nbsp;
              </el-row>
              <el-row>
                <el-col :span="8" class="text item"><span class="single-label">Pagado:</span> {{ sumOfPayments }}</el-col><el-col :span="8"><span class="single-label">Pendiente:</span> {{ postForm.fac_total - postForm.fac_payments }}</el-col>
              </el-row>
              <el-row>
&nbsp;
              </el-row>
              <el-row>
                <el-col :span="6" class="text item"><span class="single-label">Estatus:</span></el-col>
                <el-col :span="14">
                  <el-radio-group v-model="postForm.fac_pagada" v-bind="isPaymentEstatusEditable" @change="updateInvoicePaymentStatus">
                    <el-radio-button label="1" v-bind="isPayedOptionEditable">Pagada</el-radio-button>
                    <el-radio-button label="2">No pagada</el-radio-button>
                    <el-radio-button label="3">Confirmar</el-radio-button>
                  </el-radio-group>

                </el-col>
              </el-row>
              <el-row>
&nbsp;
              </el-row>
              <el-row>
                <el-col :span="6" class="text item"><span class="single-label">Cobrado:</span></el-col>
                <el-col :span="14">
                  <el-date-picker v-model="postForm.fac_fechapago" type="date" placeholder="Cobrado" class="filter-item" value-format="yyyy-MM-dd" v-bind="isPayedOptionEditable" @change="updateInvoicePaymentDate" />
                  <span>[ {{ daysCount (postForm.fac_fechapago, postForm.fac_fecha, postForm.fac_pagada) }} ]</span>
                </el-col>
              </el-row>
              <el-row>
&nbsp;
              </el-row>
              <el-row>
                <el-col :span="6" class="text item"><span class="single-label">Promotor asignado:</span></el-col>
                <el-col :span="14">
                  <el-select v-model="postForm.fac_iduser" placeholder="Promotor" clearable class="filter-item" v-bind="isPromotorSelectionEnabled" @change="updatePromotor">
                    <!--  <el-option key="0" label="-- Seleccionar --" value="" /> -->
                    <el-option v-for="item in promotorList" :key="item.id" :label="item.first_name + ' ' + item.last_name" :value="item.id" />
                  </el-select>
                </el-col>
              </el-row>
              <el-row>
&nbsp;
              </el-row>
              <el-row>
                <el-col :span="6" class="text item"><span class="single-label">Fecha estimada de pago ({{ countOfEdUpdates }}):</span></el-col>
                <el-col :span="14">
                  <el-date-picker v-model="postForm.fac_expectedpaymentday" type="date" placeholder="Fecha estimada de pago" class="filter-item" value-format="yyyy-MM-dd" @change="updateInvoiceExpectedPaymentDate" />
                </el-col>
              </el-row>
              <el-row>
&nbsp;
              </el-row>
            </el-card>
          </el-col>
        </el-row>
        <el-row>
          <el-collapse v-model="activeNames" @change="handleChange">
            <el-collapse-item title="Conceptos" name="1">
              <el-card class="box-card">

                <el-row>
                  <el-col :span="6" class="text item"><span class="single-label">Cantidad</span></el-col>
                  <el-col :span="12" class="text item"><span class="single-label">Descripción</span></el-col>
                  <el-col :span="6" class="text item"><span class="single-label">Importe</span></el-col>
                </el-row>

                <el-row v-for="con in concepts">
                  <el-col :span="6" class="text item"><span>{{ con.cantidad }}</span></el-col>
                  <el-col :span="12" class="text item"><span>{{ con.descripcion }}</span></el-col>
                  <el-col :span="6" class="text item"><span>{{ con.importe }}</span></el-col>
                </el-row>
              </el-card>
            </el-collapse-item>
            <el-collapse-item title="Pagos" name="2">
              <el-row>
                <el-col :span="12" class="text item">
  &nbsp;
                  <el-timeline>
                    <el-timeline-item
                      v-for="(payment, index) in payments"
                      :key="index"
                      :icon="'caret-right'"
                      :type="'primary'"
                      :color="'#0bbd87'"
                      :size="'normal'"
                      :timestamp="payment.his_date"
                    >
                      {{ payment.his_amount }} <el-button @click="doDeletePayment(payment.his_key)">x</el-button>
                    </el-timeline-item>
                  </el-timeline>

                </el-col>
                <el-col :span="12">
                  <el-card class="box-card">
                    <el-row>
                      <el-col :span="6" class="text item"><span class="single-label">Fecha de pago:</span></el-col>
                      <el-col :span="14">
                        <el-date-picker v-model="inputPaymentDate" type="date" placeholder="Fecha" class="filter-item" value-format="yyyy-MM-dd" />
                      </el-col>
                    </el-row>
                    <el-row>
                      <el-col :span="6" class="text item"><span class="single-label">Monto:</span></el-col>
                      <el-col :span="14">
                        <el-input v-model="inputAmount" placeholder="Monto" style="width: 220px;" class="filter-item" @keyup.enter.native="" />
                      </el-col>
                    </el-row>
                    <el-row>
                      <el-col :span="6" class="text item">&nbsp;</el-col>
                      <el-col :span="14">
                        <el-button v-bind="isPaymentButonEnabled" @click="doSavePayment">Agregar</el-button>
                      </el-col>
                    </el-row>
                  </el-card>
                  <el-card class="box-card">
                    <p>Pagado: </p>
                    <div class="text item" style="font-size: 24px; font-weight: bold;">
                      {{ sumOfPayments }}
                    </div>
                  </el-card>

                </el-col>
              </el-row>
            </el-collapse-item>
            <el-collapse-item title="Bitácora" name="3">
              <el-row>
                <el-col :span="12" class="text item">
&nbsp;
                  <el-timeline>
                    <el-timeline-item
                      v-for="(log, index) in invoicelog"
                      :key="index"
                      :icon="'caret-right'"
                      :type="'primary'"
                      :color="'#0bbd87'"
                      :size="'normal'"
                      :timestamp="log.log_datetime | humanDate"
                    >
                      {{ log.username }}: {{ log.log_text }}  <el-button @click="doDeleteLog(log.log_key)">x</el-button>
                    </el-timeline-item>
                  </el-timeline>

                </el-col>
                <el-col :span="12">
                  <el-card class="box-card">
                    <el-row>
                      <el-col :span="6" class="text item"><span class="single-label">Comentario:</span></el-col>
                      <el-col :span="14">
                        <el-input v-model="inputLog" type="textarea" placeholder="Comentario" style="width: 400px;" class="filter-item" @keyup.enter.native="doSaveLog" />
                      </el-col>
                    </el-row>
                    <el-row>
&nbsp;
                    </el-row>
                    <el-row>
                      <el-col :span="6" class="text item">&nbsp;</el-col>
                      <el-col :span="14">
                        <el-button v-bind="isLogButonEnabled" @click="doSaveLog">Agregar</el-button>
                      </el-col>
                    </el-row>
                  </el-card>

                </el-col>
              </el-row>
            </el-collapse-item>
            <el-collapse-item title="Complementos" name="4">
              <el-card class="box-card">
                <el-row>
                  <el-col :span="6" class="text item"><span class="single-label">&nbsp;</span></el-col>
                  <el-col :span="14">
                    <el-input v-model="postForm.fac_complemento" type="textarea" placeholder="Complementos" style="width: 700px;" class="filter-item" @keyup.enter.native="handleAddAmount" />
                  </el-col>
                </el-row>
                <el-row>
&nbsp;
                </el-row>
                <el-row>
                  <el-col :span="6" class="text item">&nbsp;</el-col>
                  <el-col :span="14">
                    <el-button v-bind="isComplementButonEnabled" @click="updateInvoiceComplement"> Guardar</el-button>
                  </el-col>
                </el-row>
              </el-card>
            </el-collapse-item>
            <el-collapse-item title="Cliente" name="5">
              <el-card class="box-card">
                <el-row>
                  <el-col :span="6" class="text item"><span class="single-label">Nombre: </span></el-col>
                  <el-col :span="14">
                    {{ postFormClient.contact_fullname }}
                  </el-col>
                </el-row>
                <el-row>
&nbsp;
                </el-row>
                <el-row>
                  <el-col :span="6" class="text item"><span class="single-label">RFC</span></el-col>
                  <el-col :span="14">
                    {{ postFormClient.contact_taxid }}
                  </el-col>
                </el-row>
                <el-row>
&nbsp;
                </el-row>
                <el-row>
                  <el-col :span="6" class="text item"><span class="single-label">Correo electrònico:</span></el-col>
                  <el-col :span="14">
                    <el-input v-model="postFormClient.contact_email" placeholder="E-mail" style="width: 500px;" class="filter-item" />
                  </el-col>
                </el-row>
                <el-row>
&nbsp;
                </el-row>
                <el-row>
                  <el-col :span="6" class="text item"><span class="single-label">Dirección:</span></el-col>
                  <el-col :span="14">
                    <el-input v-model="postFormClient.contact_address" type="textarea" placeholder="Calle, num, CP" style="width: 500px;" class="filter-item" />
                  </el-col>
                </el-row>
                <el-row>
&nbsp;
                </el-row>
                <el-row>
                  <el-col :span="6" class="text item"><span class="single-label">Observaciones:</span></el-col>
                  <el-col :span="14">
                    <el-input v-model="postFormClient.contact_comment" type="textarea" placeholder="Observaciones" style="width: 500px;" class="filter-item" @keyup.enter.native="doSaveClient" />
                  </el-col>
                </el-row>
                <el-row>
&nbsp;
                </el-row>
                <el-row>
                  <el-col :span="6" class="text item">&nbsp;</el-col>
                  <el-col :span="14">
                    <el-button @click="doSaveClient">Guardar</el-button>
                  </el-col>
                </el-row>
              </el-card>
            </el-collapse-item>
            <el-collapse-item title="Fecha esperada de pago" name="6">
              <el-row>
                <el-col :span="12" class="text item">
  &nbsp;
                  <el-timeline>
                    <el-timeline-item
                      v-for="(change, index) in edchanges"
                      :key="index"
                      :icon="'caret-right'"
                      :type="'primary'"
                      :color="'#0bbd87'"
                      :size="'normal'"
                      :timestamp="change.ed_date | humanDate"
                    >
                      Cambio de [ {{ change.ed_olddate }} ] a [ {{ change.ed_newdate }} ] por {{ change.username }}<!-- <el-button @click="doDeletePayment(payment.his_key)">x</el-button> -->
                    </el-timeline-item>
                  </el-timeline>

                </el-col>

              </el-row>
            </el-collapse-item>
          </el-collapse>

        </el-row>
      </div>
    </el-form>
  </div>
</template>

<script>
import Tinymce from '@/components/Tinymce'
import Upload from '@/components/Upload/SingleImage3'
import MDinput from '@/components/MDinput'
import Sticky from '@/components/Sticky' // 粘性header组件
import { validURL } from '@/utils/validate'
import { fetchInvoice, fetchPromotorsList, fetchPaymentsHistoryList, updateInvoice, addInvoicePayment, fetchLogs, addInvoiceLog, deleteLog, deletePayment, fetchEdHistoryList } from '@/api/invoice'
import { fetchContact, updateContact } from '@/api/client'
import { searchUser } from '@/api/remote-search'
import Warning from './Warning'
import { CommentDropdown, PlatformDropdown, SourceUrlDropdown } from './Dropdown'
import { mapGetters } from 'vuex'

export default {
  name: 'InvoiceDetail',
  components: { Tinymce, MDinput, Upload, Sticky, Warning, CommentDropdown, PlatformDropdown, SourceUrlDropdown },
  props: {
    isEdit: {
      type: Boolean,
      default: false
    }
  },
  data() {
    const validateRequire = (rule, value, callback) => {
      if (value === '') {
        this.$message({
          message: rule.field + '为必传项',
          type: 'error'
        })
        callback(new Error(rule.field + '为必传项'))
      } else {
        callback()
      }
    }
    const validateSourceUri = (rule, value, callback) => {
      if (value) {
        if (validURL(value)) {
          callback()
        } else {
          this.$message({
            message: '外链url填写不正确',
            type: 'error'
          })
          callback(new Error('外链url填写不正确'))
        }
      } else {
        callback()
      }
    }
    return {
      postForm: {},
      recoverForm: {},
      postFormClient: {},
      recoverFormClient: {},
      loading: false,
      isActive: true,
      paymentStatus: 2,
      userListOptions: [],
      rules: {
        image_uri: [{ validator: validateRequire }],
        title: [{ validator: validateRequire }],
        content: [{ validator: validateRequire }],
        source_uri: [{ validator: validateSourceUri, trigger: 'blur' }]
      },
      tempRoute: {},
      xmlInvoice: {},
      concepts: [],
      activeNames: [],
      payments: [{
        content: 'Custom icon',
        timestamp: '2018-04-12 20:46',
        size: 'large',
        type: 'primary',
        icon: 'el-icon-more'
      }, {
        content: 'Custom color',
        timestamp: '2018-04-03 20:46',
        color: '#0bbd87'
      }, {
        content: 'Custom size',
        timestamp: '2018-04-03 20:46',
        size: 'large'
      }, {
        content: 'Default node',
        timestamp: '2018-04-03 20:46'
      }],
      edchanges: [],
      invoicelog: [],
      inputAmount: undefined,
      inputPaymentDate: undefined,
      inputPromotor: undefined,
      inputObservaciones: undefined,
      inputComplementos: undefined,
      inputLog: undefined,
      promotorList: [],
      userid: 0,
      invoiceClient: {},
      currentRole: '',
      sumOfPayments: 0,
      countOfEdUpdates: 0,
      meid: 0
    }
  },
  computed: {
    contentShortLength() {
      return this.postForm.content_short.length
    },
    displayTime: {
      // set and get is useful when the data
      // returned by the back end api is different from the front end
      // back end return => "2013-06-25 06:59:25"
      // front end need timestamp => 1372114765000
      get() {
        return (+new Date(this.postForm.display_time))
      },
      set(val) {
        this.postForm.display_time = new Date(val)
      }
    },
    isActiveEstatusEditable() {
      // return {
      if (this.currentRole == 'admin' || this.currentRole == 'operator') {
        return {}
      } else { return { [`disabled`]: true } }

      // }
    },
    isPaymentEstatusEditable() {
      // return {
      if (this.currentRole == 'admin' || this.currentRole == 'operator') {
        return {}
      } else { return { [`disabled`]: true } }

      // }
    },
    isPayedOptionEditable() {
      // return {
      if (this.currentRole == 'admin') {
        return {}
      } else { return { [`disabled`]: true } }

      // }
    },
    isPaymentButonEnabled() {
      if (this.currentRole == 'admin' || this.currentRole == 'operator') {
        return {}
      } else { return { [`disabled`]: true } }
    },
    isLogButonEnabled() {
      if (this.currentRole == 'executive') {
        return { [`disabled`]: true }
      } else { return {} }
    },
    isComplementButonEnabled() {
      if (this.currentRole == 'admin' || this.currentRole == 'operator') {
        return {}
      } else { return { [`disabled`]: true } }
    },
    isPromotorSelectionEnabled() {
      if (this.currentRole == 'promotor' || this.userid == 23) {
        return { [`disabled`]: true }
      } else { return {} }
    },
    ...mapGetters([
      'roles'
    ])
  },
  created() {
    if (this.isEdit) {
      const id = this.$route.params && this.$route.params.id
      this.fetchData(id)
      this.fetchPaymentHistory(id)
      this.fetchLogHistory(id)
      this.getPromotors()
      this.fetchEdHistory(id)
      // this.getClient(id)
    } else {
      this.postForm = {}
    }

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
    // console.log(this.$store.state.user.roles);
    this.userid = this.$store.state.user.userid
    // console.log('meid'+this.meid);

    // Why need to make a copy of this.$route here?
    // Because if you enter this page and quickly switch tag, may be in the execution of the setTagsViewTitle function, this.$route is no longer pointing to the current page
    // https://github.com/PanJiaChen/vue-element-admin/issues/1221
    this.tempRoute = Object.assign({}, this.$route)
  },
  methods: {
    fetchPaymentHistory(id) {
      fetchPaymentsHistoryList(id).then(response => {
        this.payments = response.data // JSON.parse(response.data);
        // if (Array.isArray(this.payments)){
        // console.log(this.payments[0]['his_amount'])
        // }
        var t = 0
        this.payments.forEach(function(e) {
          t += parseInt(e.his_amount)
        })
        this.sumOfPayments = t
      }).catch(err => {
        console.log(err)
      })
    },
    fetchEdHistory(id) {
      fetchEdHistoryList(id).then(response => {
        this.edchanges = response.data // JSON.parse(response.data);
        // if (Array.isArray(this.payments)){
        // console.log(this.payments[0]['his_amount'])
        // }

        this.countOfEdUpdates = this.edchanges.length
      }).catch(err => {
        console.log(err)
      })
    },
    /* getClient(id){
      fetchClient(id).then(response => {
        var convert = require('xml-js')
        var tmpData = response.data
        /* if (typeof(tmpData.fac_isactive)=='string') {
          if(tmpData.fac_isactive=='true'){
            tmpData.fac_isactive=true;
          }
          else
            tmpData.fac_isactive=false;
        }* /

        this.postFormClient = Object.assign({}, tmpData)
        this.recoverFormClient = Object.assign({}, tmpData)
      });
    },*/
    fetchLogHistory(id) {
      fetchLogs(id).then(response => {
        this.invoicelog = response.data
      }).catch(err => {
        console.log(err)
      })
    },
    fetchData(id) {
      fetchInvoice(id).then(response => {
        var convert = require('xml-js')
        var tmpData = response.data
        /* if (typeof(tmpData.fac_isactive)=='string') {
          if(tmpData.fac_isactive=='true'){
            tmpData.fac_isactive=true;
          }
          else
            tmpData.fac_isactive=false;
        }*/

        this.postForm = Object.assign({}, tmpData)
        this.recoverForm = Object.assign({}, tmpData)

        this.sumOfPayments = this.postForm.fac_payments
        this.countOfEdUpdates = this.postForm.fac_edupdatescount
        console.log('estatus:')
        console.log(this.postForm.fac_isactive)

        // just for test
        this.postForm.title += `   Article Id:${this.postForm.fac_key}`
        this.postForm.content_short += `   Article Id:${this.postForm.fac_key}`
        this.xmlInvoice = JSON.parse(convert.xml2json(this.postForm.fac_xml, { compact: true, spaces: 4 }))
        // console.log('JP1');

        // set tagsview title
        this.setTagsViewTitle()

        // set page title
        this.setPageTitle()

        /* process invoice*/
        var comprobante, conceptos, concepto
        comprobante = this.xmlInvoice['cfdi:Comprobante']
        var attsComprobante = comprobante['_attributes']
        var keyCantidad = ''; var keyDescripcion = ''; var keyImporte = ''
        if (attsComprobante['Version'] != undefined) {
          // v 3.3
          keyCantidad = 'Cantidad'
          keyDescripcion = 'Descripcion'
          keyImporte = 'Importe'
        } else {
          // v 3.2
          keyCantidad = 'cantidad'
          keyDescripcion = 'descripcion'
          keyImporte = 'importe'
        }
        // console.log(tmp);
        conceptos = comprobante['cfdi:Conceptos']
        // console.log(conceptos);
        // console.log(self.xml)
        //

        // console.log(conceptos)
        var co = []
        if (Array.isArray(conceptos)) {
          // console.log('conceptos es arreglo')
          conceptos.forEach(function(concepto) {
            // console.log(concepto);
            // a b c
          })
        } else {
          // console.log('conceptos es objeto')
          Object.keys(conceptos).forEach(function(key) {
            console.log('key:' + key)
            concepto = conceptos[key]
            // concepto es arreglo
            if (Array.isArray(concepto)) {
              // console.log('conceptO es arreglo')
              concepto.forEach(function(c) {
                var atributos = c['_attributes']
                // console.log(atributos)
                var elemento = { cantidad: atributos[keyCantidad], descripcion: atributos[keyDescripcion], importe: atributos[keyImporte] }
                co.push(elemento)
              })
            } else {
              // console.log('conceptO es objeto')
              var atributos = concepto['_attributes']
              // console.log(atributos)
              var elemento = { cantidad: atributos[keyCantidad], descripcion: atributos[keyDescripcion], importe: atributos[keyImporte] }
              co.push(elemento)
            }

            // concepto=conceptos[key];
            // console.log('concepto:');
            // console.log(concepto)
            // var atributos=concepto['_attributes'];
            // console.log(atributos)
            // var elemento={cantidad:atributos[keyCantidad], descripcion:atributos[keyDescripcion] , importe:atributos[keyImporte]}
            // co.push(elemento);
          })
        }

        // console.log(co);
        this.concepts = co

        if (this.postForm.fac_idclient) {
          this.getInvoiceClient()
        }
      }).catch(err => {
        console.log(err)
      })
    },
    getPromotors() {
      // this.listLoading = true
      fetchPromotorsList().then(response => {
        this.promotorList = response.data
      })
    },
    getInvoiceClient() {
      // this.listLoading = true
      fetchContact(this.postForm.fac_idclient).then(response => {
        var tmpData = response.data

        this.postFormClient = Object.assign({}, tmpData)
        this.recoverFormClient = Object.assign({}, tmpData)
      }).catch(err => {
        console.log(err)

        this.postFormClient = Object.assign({}, recoverFormClient)

        this.$notify({
          title: 'Error',
          message: 'Error al guardar datos del cliente',
          type: 'warning',
          duration: 2000
        })
      })
    },
    doSavePartialInvoice(data, keys) {
      updateInvoice(this.postForm.fac_key, data).then(response => {
        this.recoverForm = Object.assign({}, this.postForm)
        this.$notify({
          title: 'Actualizar',
          message: 'Factura actualizada',
          type: 'success',
          duration: 2000
        })

        if (('fac_expectedpaymentday' in data)) {
          this.fetchEdHistory(this.postForm.fac_key)
        }
      }).catch(err => {
        console.log(err)

        keys.forEach(function(k) {
          this.postForm[k] = this.recoverForm[k]
        })
        this.$notify({
          title: 'Error',
          message: 'Error al guardar la factura',
          type: 'warning',
          duration: 2000
        })
      })
    },
    doSaveClient() {
      updateContact(this.postFormClient.id, this.postFormClient).then(response => {
        this.recoverFormClient = Object.assign({}, this.postFormClient)
        this.$notify({
          title: 'Actualizar',
          message: 'Datos de cliente actualizados',
          type: 'success',
          duration: 2000
        })
      }).catch(err => {
        console.log(err)

        this.postFormClient = Object.assign({}, recoverFormClient)

        this.$notify({
          title: 'Error',
          message: 'Error al guardar la factura',
          type: 'warning',
          duration: 2000
        })
      })
    },
    updateInvoiceStatus() {
      var data = {
        fac_isactive: this.postForm.fac_isactive
      }
      var keys = ['fac_isactve']
      this.doSavePartialInvoice(data, keys)
    },
    updateInvoicePaymentStatus() {
      var data = {
        fac_pagada: this.postForm.fac_pagada
      }
      var keys = ['fac_pagada']
      this.doSavePartialInvoice(data, keys)
    },
    updateInvoicePaymentDate() {
      var data = {
        fac_fechapago: this.postForm.fac_fechapago
      }
      var keys = ['fac_fechapago']
      this.doSavePartialInvoice(data, keys)
    },
    updateInvoiceExpectedPaymentDate() {
      var data = {
        fac_expectedpaymentday: this.postForm.fac_expectedpaymentday
      }
      var keys = ['fac_expectedpaymentday']
      this.doSavePartialInvoice(data, keys)
    },
    updatePromotor() {
      var data = {
        fac_iduser: this.postForm.fac_iduser
      }
      var keys = ['fac_iduser']
      this.doSavePartialInvoice(data, keys)
    },
    updateInvoiceComplement() {
      var data = {
        fac_complemento: this.postForm.fac_complemento
      }
      var keys = ['fac_complemento']
      this.doSavePartialInvoice(data, keys)
    },
    updateInvoiceUserAndClient() {
      var data = {
        fac_iduser: this.postForm.fac_iduser
      }
      var keys = ['fac_iduser']
      this.doSavePartialInvoice(data, keys)
    },
    doSaveLog() {
      // console.log(this.userid);
      var uid = this.userid
      var data = {
        log_text: this.inputLog,
        log_invoice: this.postForm.fac_key,
        log_date: new Date(),
        log_cuser: uid
      }
      if (this.inputLog != undefined && this.inputLog != '') {
        addInvoiceLog(data).then(response => {
          this.$notify({
            title: 'Bitacora',
            message: 'Registro guardado',
            type: 'success',
            duration: 2000
          })
          this.inputLog = ''
          this.fetchLogHistory(this.postForm.fac_key)
        }).catch(err => {
          console.log(err)
        })
      }
    },
    doDeletePayment(id) {
      deletePayment(id).then(response => {
        // this.recoverForm = Object.assign({}, this.postForm)
        this.$notify({
          title: 'Pagos',
          message: 'Registro eliminado',
          type: 'success',
          duration: 2000
        })

        this.fetchPaymentHistory(this.postForm.fac_key)
      })
    },
    doDeleteLog(id) {
      deleteLog(id).then(response => {
        // this.recoverForm = Object.assign({}, this.postForm)
        this.$notify({
          title: 'Bitacora',
          message: 'Registro eliminado',
          type: 'success',
          duration: 2000
        })

        this.fetchLogHistory(this.postForm.fac_key)
      })
    },
    doSavePayment() {
      var data = {
        his_amount: this.inputAmount,
        his_invoice: this.postForm.fac_key,
        his_date: this.inputPaymentDate
      }
      if (this.inputAmount != '' && this.inputPaymentDate != undefined && this.inputPaymentDate != '') {
        addInvoicePayment(data).then(response => {
        // this.recoverForm = Object.assign({}, this.postForm)
          this.$notify({
            title: 'Pagos',
            message: 'Pago registrado',
            type: 'success',
            duration: 2000
          })
          this.inputAmount = ''
          this.inputPaymentDate = ''
          this.fetchPaymentHistory(this.postForm.fac_key)
        }).catch(err => {
          console.log(err)
        })
      }
    },
    setTagsViewTitle() {
      const title = 'Factura'
      const route = Object.assign({}, this.tempRoute, { title: `${title}-${this.postForm.fac_serie} ${this.postForm.fac_folio}` })
      this.$store.dispatch('tagsView/updateVisitedView', route)
    },
    setPageTitle() {
      const title = 'Factura'
      document.title = `${title} - ${this.postForm.fac_serie} ${this.postForm.fac_folio}`
    },
    draftForm() {
      if (this.postForm.content.length === 0 || this.postForm.title.length === 0) {
        this.$message({
          message: '请填写必要的标题和内容',
          type: 'warning'
        })
        return
      }
      this.$message({
        message: '保存成功',
        type: 'success',
        showClose: true,
        duration: 1000
      })
      this.postForm.status = 'draft'
    },
    getRemoteUserList(query) {
      searchUser(query).then(response => {
        if (!response.data.items) return
        this.userListOptions = response.data.items.map(v => v.name)
      })
    },
    handleChange(val) {
      console.log(val)
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
  filters: {
    // Filter definitions
    humanDate(value) {
      const options = {
        year: 'numeric',
        month: 'numeric',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric'
      }
      var d = new Date(value)
      return new Intl.DateTimeFormat('es-MX', options).format(d)// d.toDateString() + " " + d.toTimeString();
    }
  }
}
</script>

<style lang="scss" scoped>
@import "~@/styles/mixin.scss";

.single-label{
 font-weight: bold;
 font-size: 14px;
}
.createPost-container {
  position: relative;

  .createPost-main-container {
    padding: 40px 45px 20px 50px;

    .postInfo-container {
      position: relative;
      @include clearfix;
      margin-bottom: 10px;

      .postInfo-container-item {
        float: left;
      }
    }
  }

  .word-counter {
    width: 40px;
    position: absolute;
    right: 10px;
    top: 0px;
  }
}

.article-textarea /deep/ {
  textarea {
    padding-right: 40px;
    resize: none;
    border: none;
    border-radius: 0px;
    border-bottom: 1px solid #bfcbd9;
  }
}
</style>
