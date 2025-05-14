<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12">
          <v-toolbar  dense>
            <v-tabs>
              <v-tab
                v-for="link in links"
                :key="link.route"
                :to="link.route"
                text
                :class="{ 'active': $route.path === link.route }"
              >
              {{ link.text }}
              </v-tab>
            </v-tabs>

          </v-toolbar>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      links: [
        { text: 'ثبت اطلاعات', route: '/' },
        { text: 'گزارش', route: '/report' },
      ],
    };
  },
};
</script>

<style scoped>
.v-toolbar {
  background-color: white;
}

.v-tab {
  margin: 0 10px;
  font-size: 16px;
}

.v-tab.active {
  font-weight: bold;
}
</style>