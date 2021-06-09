import Vue from 'vue'
import VueRouter from 'vue-router'
import PatientList from './views/PatientList'

Vue.use(VueRouter)

export default new VueRouter({
    mode: 'history',
    base: '/',
    routes:[
        {
            path: '/',
            name: 'patientList',
            component: PatientList,
        }
    ]
})