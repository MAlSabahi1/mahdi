<template>
  <drawer :data="data" :getData="getData" click="d-services/grant-sources/">
    <template v-slot>
      <fields
        :data="data"
        url="grant-source"
        :attr="{
          email: {
            rules: [$email],
          },
          phone: {
            rules: [$min_length(6), $max_length(15)],
          },
        }"
      />
    </template>
  </drawer>
</template>
<script>
export default {
  props: {
    data: Object,
  },
};
</script>
