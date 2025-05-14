<template>
    <v-dialog
      v-model="create_person_dialog"
      persistent
      max-width="600px"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          color="primary"
          dark
          v-bind="attrs"
          v-on="on"
        >
          ثبت فرد جدید
        </v-btn>
      </template>
      
      <v-card>
        <v-card-title>
          <span>ثبت فرد جدید</span>
        </v-card-title>
        <v-card-text>
          <v-container>

          <v-form ref="person_create_form" v-model="valid">
            <v-row>
              <v-col cols="12" class="pt-0 pb-0">  
                <vue-persian-datetime-picker 
                  v-model="person.registration_date"  
                  label="تاریخ"
                  color="#5788b7"
                  format="YYYY-MM-DD" 
                  display-format="jYYYY/jMM/jDD"
                  :rules="requiredRules"
                >
                </vue-persian-datetime-picker>
              </v-col>
              

              <v-col cols="6" class="pt-0 pb-0">  
                <v-text-field v-model="person.first_name" label="نام" :rules="requiredRules"></v-text-field>
              </v-col>
              <v-col cols="6" class="pt-0 pb-0">  
                <v-text-field v-model="person.last_name" label="نام خانوادگی" :rules="requiredRules"></v-text-field>
              </v-col>

              <v-col cols="12" class="pt-0 pb-0">  
                <v-select v-model="person.gender" :items="genders" label="جنسیت" :rules="selectedRequiredRules"></v-select>
              </v-col>
          
              <v-col cols="4" class="pt-0 pb-0">  
                <v-text-field v-model="phone_number.phone_number" label="شماره تلفن جدید"></v-text-field>
              </v-col>
              <v-col cols="2" class="pt-0 pb-0">  
                <v-btn @click="addNumber" color="blue" outlined ><v-icon color="blue">mdi-plus</v-icon></v-btn>
              </v-col>
              <v-col cols="6" class="pt-0 pb-0">
                <v-chip-group column>
                  <v-chip
                    outlined  
                    label
                    class="ma-2"
                    color="black"
                    v-for="number in person.phone_numbers"
                    :key="number"
                    :value="number"
                    close
                    @click:close="removeNumber(number)"
                  >
                    {{ number.phone_number }}
                  </v-chip>
                </v-chip-group>
              </v-col>
              
            
              <v-col cols="12" class="pt-5 pb-0">
              
                <v-row>  
                  <p class="font-weight-bold pa-3 " style="color:black;">
                    لیست آدرس‌ها
                  </p>
                  
                  <v-dialog
                      v-model="create_address_dialog_c"
                      persistent
                      max-width="400px"
                      >
                      <template v-slot:activator="{ on, attrs }">
                          <v-btn outlined color="blue" v-bind="attrs" v-on="on" >افزودن آدرس جدید</v-btn>
                      </template>
                      
                      <v-card>
                          <v-card-title><span>افزودن آدرس جدید</span></v-card-title>
                          <v-card-text>
                              <v-container>
                                  <v-form ref="create_address_form_c" v-model="valid">
                                      <v-text-field v-model="address.title" label="عنوان" :rules="requiredRules"></v-text-field>
                                      <v-textarea v-model="address.description" label="توضیحات" :rules="requiredRules"></v-textarea>
                                  </v-form>
                              </v-container>
                          </v-card-text>
                          <v-card-actions>
                              <v-spacer></v-spacer>
                              <v-btn text color="red"  @click="cancel_add_address_c">لغو</v-btn>
                                
                              <v-btn v-if="address_to_edit === null" text color="green"  @click="add_address">افزودن</v-btn>
                              <v-btn v-else text color="blue"  @click="edit_address">ویرایش</v-btn>

                          </v-card-actions>
                      </v-card>
                  </v-dialog>
                
                </v-row>

                <v-simple-table>
                  <template>
                    <thead>
                      <tr>
                        <th>
                          عنوان
                        </th>
                        <th>
                          توضیحات
                        </th>
                        <th></th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr
                        v-for="address_item in person.addresses"
                        :key="address_item"
                      >
                        <td>{{ address_item.title }}</td>
                        <td>{{ address_item.description }}</td>
                        <td>
                          <v-btn text color="blue" @click="open_edit_address_dialog(address_item)">ویرایش</v-btn>
                          <v-btn text color="red" @click="remove_address(address_item)">حذف</v-btn>
                        </td>
                      </tr>
                    </tbody>
                  </template>
                </v-simple-table>
                


              </v-col>

            </v-row>

          </v-form>
            
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn outlined color="red"  @click="cancel_create_person">لغو</v-btn>
          
          <v-btn v-if="person_id_to_edit === null" outlined color="green"  @click="submit_create_person">ذخیره</v-btn>
          <v-btn v-else outlined color="green"  @click="submit_edit_person(person_id_to_edit)">ذخیره تغییرات</v-btn>

        </v-card-actions>
      </v-card>
    </v-dialog>
</template>

<script>
import axios from 'axios';
import VuePersianDatetimePicker from 'vue-persian-datetime-picker';


  export default {
    components: {
      VuePersianDatetimePicker,
    },
    data () {
      return {
        create_person_dialog: false,
        create_address_dialog_c: false,
        valid: true,
        person: {
            first_name: '',
            last_name: '',
            gender: null,
            registration_date: '',
            phone_numbers: [],
            addresses: [],
        },
        phone_number: {
          phone_number: '',
        },
        address: {
            title: '',
            description: '',
        },
        genders: [
            { text: 'مرد', value: 0 },
            { text: 'زن', value: 1 },
        ],
        requiredRules: [(v) => !!v || 'این فیلد الزامی است'],
        selectedRequiredRules: [(v) => v==0 || v==1 || 'این فیلد الزامی است'],

        address_to_edit: null,
        person_id_to_edit: null
        
        };
    },
    methods: {
        resetCreatePersonForm () {
            this.person.first_name = "";
            this.person.last_name = "";
            this.person.gender = null;
            this.person.registration_date = "";
            this.person.phone_numbers = [];
            this.person.addresses = [];
            this.person_id_to_edit = null;
            this.$refs.person_create_form.resetValidation();
        },
        resetCreateAddressForm () {
            this.address.title = "";
            this.address.description = "";
            this.address_to_edit = null;
            this.$refs.create_address_form_c.resetValidation();
        },
        async submit_create_person() {
            if (this.$refs.person_create_form.validate()) {
                console.log('Create Person Form data:', JSON.parse(JSON.stringify(this.person)))
                try {
                 const response = await axios.post('http://127.0.0.1:8000/registry/persons/', this.person);
                 console.log(response.data)
                 this.$emit('person-saved');
                } catch (error) {
                    console.error('Error creating person:', error);
                    this.$snackbar.open({
                    message: 'خطا در ذخیره اطلاعات',
                    color: 'error'
                    })
                }
                this.resetCreatePersonForm();
                this.create_person_dialog = false;
            }
        },
        async submit_edit_person(person_id) {
            console.log(person_id);
            console.log('Update Person Form data:', JSON.parse(JSON.stringify(this.person)))
            if (this.$refs.person_create_form.validate()) {

                await axios.put(`http://127.0.0.1:8000/registry/persons/${person_id}/`, this.person)
                .then(response => {
                  console.log('Person updated:', response.data);
                  this.$emit('person-saved');
                })
                .catch(error => {
                  console.error('Error updating person:', error);
                });

                this.resetCreatePersonForm();
                this.create_person_dialog = false;
            }
        },
        cancel_create_person() {
            this.resetCreatePersonForm();
            this.create_person_dialog = false;
        },
        add_address() {
            if (this.$refs.create_address_form_c.validate()) {
                const address_data = JSON.parse(JSON.stringify(this.address))
                this.person.addresses.push(address_data);
                this.resetCreateAddressForm();
                this.create_address_dialog_c = false;
            }
        },
        remove_address(address_item) {
          this.person.addresses.splice(this.person.addresses.indexOf(address_item), 1)
        },
        cancel_add_address_c() {
            this.resetCreateAddressForm();
            this.create_address_dialog_c = false;
        },
        addNumber() {
          
            const number_data = JSON.parse(JSON.stringify(this.phone_number))
            this.person.phone_numbers.push(number_data);
            this.phone_number.phone_number = '';
          
        },
        removeNumber(number) {
          this.person.phone_numbers.splice(this.person.phone_numbers.indexOf(number), 1)
        },
        open_edit_address_dialog(address_item) {
          this.address_to_edit = address_item;
          this.address.title = this.address_to_edit.title;
          this.address.description = this.address_to_edit.description;
          this.create_address_dialog_c = true;
        },
        edit_address() {
            if (this.$refs.create_address_form_c.validate()) {
                this.address_to_edit.title = this.address.title;
                this.address_to_edit.description = this.address.description;
                this.resetCreateAddressForm();
                this.create_address_dialog_c = false;
            }
        },
    }
  }
</script>