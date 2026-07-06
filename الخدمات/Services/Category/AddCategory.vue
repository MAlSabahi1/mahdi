<template>
  <drawer :data="data" click="d-services/workflow/categories/" :getData="getData">
    <template v-slot>
         <fields :data="data" url="categories" />
    </template>
  </drawer>
</template>
<script>
export default {
  props: {
    data: Object,
  },
  data(){
    return{
      data:{}
    }
  }
};
</script>
