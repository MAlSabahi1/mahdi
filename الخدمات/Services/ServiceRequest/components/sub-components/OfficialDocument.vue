<template>
    <div ref="documentContainer"  >
        <!-- Action Bar (Hidden during print) -->
        <slot></slot>

    </div>
</template>

<script>

export default {
    name: 'OfficialDocument',

};
</script>

<style scoped>
.official-document-container {
    background: #f1f5f9;
    min-height: 100vh;
}
</style>
