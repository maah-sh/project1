<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12">
        <v-card>
          <v-card-title>
          
          </v-card-title>
          <v-card-text>  
            <person-form @person-saved="updataPersonsData" ref="personFormRef"/>
          </v-card-text>
          <v-data-table
            :headers="headers"
            :items="persons"
            :loading="loading"
            class="elevation-1"
            :footer-props="{
              itemsPerPageOptions: [10, 25, 50, 100],
              showFirstLast: true,
              prevIcon: 'mdi-chevron-right',
              nextIcon: 'mdi-chevron-left'
            }"
          >
            <template v-slot:[`item.gender`]="{ item }">
              {{ item.gender === 0 ? 'مرد' : 'زن' }}
            </template>

            <template v-slot:[`item.phone_numbers`]="{ item }">
              {{ item.phone_numbers.map(phone => phone.phone_number).join(', ') }}
            </template>

            <template v-slot:[`item.addresses`]="{ item }">
              <div v-for="address in item.addresses" :key="address.id">
                {{ address.title }} : {{ address.description }}<br>  </div>
            </template>

            <template v-slot:[`item.registration_date`]="{ item }">
              {{ item.registration_date | moment('jYYYY/jMM/jDD') }}
            </template>

            <template v-slot:[`item.id`]="{ item }">
              <v-btn text color="blue" @click="open_edit_person_dialog(item.id)">ویرایش</v-btn>
              <v-btn text color="red" @click="remove_person(item.id)">حذف</v-btn>
            </template>

          </v-data-table>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';
import PersonForm from '../components/PersonForm.vue';

export default {
  components: {
    PersonForm,
  },
  data() {
    return {
      loading: true,
      persons: [],
      headers: [
        { text: 'نام', value: 'first_name', align: 'center' },
        { text: 'نام خانوادگی', value: 'last_name', align: 'center' },
        { text: 'جنسیت', value: 'gender', align: 'center' },
        { text: 'شماره تلفن‌ها', value: 'phone_numbers', align: 'center' },
        { text: 'آدرس', value: 'addresses', align: 'center' },
        { text: 'تاریخ ثبت نام', value: 'registration_date', align: 'center' },
        { text: 'تنظیمات', value: 'id', align: 'center' },
      ],
    };
  },
  mounted() {
    this.fetchPersons();
  },
  methods: {
    async fetchPersons() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/registry/persons/');
        this.persons = response.data;
      } catch (error) {
        console.error('Error fetching persons:', error);
        this.$snackbar.open({
          message: 'خطا در دریافت اطلاعات',
          color: 'error'
        })
      } finally {
        this.loading = false;
      }
    },
    updataPersonsData() {
      this.fetchPersons()
    },
    async remove_person(person_id) {
      await axios.delete(`http://127.0.0.1:8000/registry/persons/${person_id}/`)
      .then(response => {
        console.log('Person deleted:', response.data.message);
        this.updataPersonsData();
      })
      .catch(error => {
        console.error('Error deleting person:', error);
      });
    }, 
    async open_edit_person_dialog(person_id) {
      await axios.get(`http://127.0.0.1:8000/registry/persons/${person_id}/`)
      .then(response => {
        this.$refs.personFormRef.person = response.data;
        this.$refs.personFormRef.person_id_to_edit = person_id;
        this.$refs.personFormRef.create_person_dialog = true;
      })
      .catch(error => {
        console.error('Error fetching person:', error);
      });
    }
  },
};
</script>



