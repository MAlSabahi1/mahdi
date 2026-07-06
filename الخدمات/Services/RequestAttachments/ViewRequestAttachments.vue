<template>
  <custom-data-table
    :="{
      headers:request_id?headers.slice(2):headers,
      items,
      getData,
      delItem: url,
      pagination: request_id ? false : true,
      showTop: request_id ? false : true,
    }"
  >
    <!-- actionList, -->
    <template v-slot:item-slot="{ item, key }">
      <v-chip
        variant="text"
        class="text-decoration-underline text-primary"
        v-if="key == 'request_name'"
        @click="
          moveToNex('request-details', { request_id: item['request_no'] }, {})
        "
      >
        {{ item[key] }}
      </v-chip>
      <span v-if="key=='file_url'">
        <a :href="item[key]" download class="text-decoration-none text-primary">
          <v-icon>mdi-folder-arrow-down</v-icon>
        </a>
      </span>
      <span v-if="['file_size'].includes(key)">
        <v-chip
          size="small"
          class="text-lowercase"
          :color="fileTypes[item['file_type']]?.color ?? null"
        >
          {{ item[key] }}
        </v-chip>
      </span>
      <span v-if="key == 'file_type'" class="">
        <v-icon
          v-if="fileTypes[item[key]]"
          :color="fileTypes[item[key]]?.color"
        >
          {{ fileTypes[item[key]]?.icon }}
        </v-icon>
        <v-chip v-else size="small" class="text-lowercase">
          {{ item[key] }}
        </v-chip>
      </span>
    </template>
  </custom-data-table>
</template>
<script>
export default {
  props: {
    request_id: Number,
    default: null,
  },
  data() {
    return {
      data: {},
      items: [],
      drawer: false,

      url: "d-services/services/attachments/",
      fileTypes: {
        PDF: {
          icon: "mdi-file-pdf-box",
          color: "red-darken-2",
        },
        Word: {
          icon: "mdi-file-work-box",
          color: "blue-darken-2",
        },

        Excel: {
          icon: "mdi-file-excel-box",
          color: "green-darken-2",
        },
        Image: {
          icon: "mdi-file-image",
          color: "deep-purple-darken-2",
        },
        Archive: {
          icon: "mdi-folder-zip-outline",
          color: "amber-darken-2",
        },
      },
    };
  },
  methods: {
    async getData(params = this.$params) {
      if (this.request_id) {
        const filters = {
          filters: [{ field: "fk_instance", value: this.request_id }],
        };
        return await this.$axios
          .post(`${this.url}filter/`, filters)
          .then((response) => {
            this.items = response.data;
            console.log(response.data, "======");
          });
      } else {
        return await this.$axios(this.url, params).then(
          (response) => (this.items = response.data)
        );
      }
    },
    moveToNex(screen, param, query) {
      this.$navigateTo({
        name: screen,
        params: param,
        query: query,
        blank: false,
      });
    },
    editItem(data) {
      this.data = { ...data };
      this.drawer = true;
    },

    moveToNex(screen, param, query) {
      this.$navigateTo({
        name: screen,
        params: param,
        query: query,
        blank: false,
      });
    },
  },
  computed: {
    headers() {
      return [
        { title: this.$t("request"), key: "request_name" },
        { title: this.$t("request_no"), key: "request_no" },
        { title: this.$t("file_name"), key: "file_name" },
        { title: this.$t("download"), key: "file_url"},
        {
          title: this.$t("file_type"),
          key: "file_type",
        },
        { title: this.$t("file_size"), key: "file_size" },
        { title: this.$t("uploaded_at"), key: "uploaded_at" },
        { title: this.$t("uploaded_by"), key: "fk_uploaded_by_name" },
      ];
    },
  },
};
</script>
