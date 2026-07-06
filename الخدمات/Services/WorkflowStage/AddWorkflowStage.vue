<template>
  <drawer :data="data" :getData="getData" click="d-services/workflow-stages/">
    <template v-slot>
      <fields :data="data" url="workflow-stage" :attr="{

      }" />
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
