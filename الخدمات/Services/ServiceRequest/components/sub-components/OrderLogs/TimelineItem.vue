<template>
    <div class="timeline-item">
        <div class="timeline-marker">
            <div class="marker-node" :class="type">
                <v-icon :icon="icon" size="14"></v-icon>
            </div>
            <div v-if="!isLast" class="marker-line"></div>
        </div>

        <div class="timeline-content">
            <div class="d-flex flex-wrap justify-space-between align-center mb-2 gap-2">
                <div class="d-flex align-center">
                    <v-avatar size="24" class="ml-2" color="slate-100">
                        <v-icon icon="mdi-account" size="14" color="slate-400"></v-icon>
                    </v-avatar>
                    <span class="text-body-2 font-weight-black text-slate-900">{{ user }}</span>
                    <v-chip size="x-small" :color="color" variant="tonal" class="mr-3 font-weight-black px-2">
                        {{ action }}
                    </v-chip>
                </div>
                <div class="d-flex align-center gap-3">
                    <span class="text-caption font-weight-bold text-slate-400">{{ time }}</span>
                    <v-btn variant="text" color="primary" size="x-small" class="font-weight-black rounded-lg"
                        prepend-icon="mdi-comment-plus-outline" @click="$emit('add-note')">
                        إضافة ملاحظة
                    </v-btn>
                </div>
            </div>
            <p class="text-body-2 text-slate-600 font-weight-medium mb-0 leading-relaxed">
                {{ details }}
            </p>
            <div v-if="comment" class="log-comment-box mt-3 pa-4 rounded-xl bg-slate-50 border">
                <div class="text-caption font-weight-black text-slate-400 mb-1">ملاحظة:</div>
                <div class="text-body-2 font-weight-bold text-slate-700">{{ comment }}</div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'TimelineItem',
    props: {
        user: { type: String, required: true },
        action: { type: String, required: true },
        type: { type: String, default: 'info' },
        time: { type: String, required: true },
        details: { type: String, required: true },
        comment: { type: String, default: '' },
        icon: { type: String, default: 'mdi-circle' },
        color: { type: String, default: 'slate' },
        isLast: { type: Boolean, default: false }
    },
    emits: ['add-note']
};
</script>

<style scoped>
.timeline-item {
    display: flex;
    gap: 24px;
    padding-bottom: 40px;
}

.timeline-marker {
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
}

.marker-node {
    width: 32px;
    height: 32px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f8fafc;
    border: 2px solid #f1f5f9;
    color: #94a3b8;
    z-index: 2;
}

.marker-node.success {
    background: #f0fdf4;
    border-color: #dcfce7;
    color: #10b981;
}

.marker-node.warning {
    background: #fff7ed;
    border-color: #ffedd5;
    color: #f59e0b;
}

.marker-node.info {
    background: #eff6ff;
    border-color: #dbeafe;
    color: #2563eb;
}

.marker-node.primary {
    background: #f5f3ff;
    border-color: #ede9fe;
    color: #8b5cf6;
}

.marker-line {
    position: absolute;
    top: 32px;
    bottom: -40px;
    width: 2px;
    background: #f1f5f9;
    z-index: 1;
}

.timeline-content {
    flex-grow: 1;
    padding-top: 4px;
}

.log-comment-box {
    border-color: #f1f5f9 !important;
}
</style>
