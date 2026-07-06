<template>
    <div class="logs-premium-suite">
        <v-row class="g-6">
            <!-- Header -->
            <v-col cols="12">
                <div class="d-flex flex-wrap justify-space-between align-center mb-8 gap-6">
                    <div class="d-flex align-center">
                        <div class="section-icon-box ml-4">
                            <v-icon icon="mdi-history" color="primary"></v-icon>
                        </div>
                        <div>
                            <h3 class="text-h6 font-weight-black text-slate-900 mb-0">سجل النشاطات والعمليات</h3>
                            <p class="text-caption text-slate-400 font-weight-bold mb-0">تتبع زمني لكافة الإجراءات
                                المتخذة على الطلب</p>
                        </div>
                    </div>
                    <div class="d-flex gap-3">
                        <v-btn variant="tonal" color="slate-600" class="rounded-xl font-weight-black px-6 h-52"
                            prepend-icon="mdi-filter-variant" @click="$emit('filter')">
                            تصفية السجل
                        </v-btn>
                        <v-btn variant="tonal" color="primary" class="rounded-xl font-weight-black px-6 h-52"
                            prepend-icon="mdi-download" @click="$emit('export')">
                            تصدير التقرير
                        </v-btn>
                    </div>
                </div>
            </v-col>

            <!-- Timeline -->
            <v-col cols="12">
                <v-card class="rounded-3xl elevation-0 border pa-8 bg-white">
                    <div class="timeline-container">
                        <TimelineItem v-for="(log, index) in logs" :key="index" v-bind="log"
                            :icon="getLogIcon(log.type)" :color="getLogColor(log.type)"
                            :is-last="index === logs.length - 1" @add-note="$emit('add-note', log)" />
                    </div>

                    <div class="text-center mt-10">
                        <v-btn variant="text" color="primary" class="font-weight-black" append-icon="mdi-chevron-down"
                            @click="$emit('view-all')">
                            عرض كامل السجل
                        </v-btn>
                    </div>
                </v-card>
            </v-col>
        </v-row>
    </div>
</template>

<script>
import TimelineItem from './sub-components/OrderLogs/TimelineItem.vue';

export default {
    name: 'OrderLogs',
    components: {
        TimelineItem
    },
    props: {
        logs: {
            type: Array,
            required: true,
            default: () => []
        }
    },
    emits: ['filter', 'export', 'view-all', 'add-note'],
    methods: {
        getLogIcon(type) {
            const map = { success: 'mdi-check', warning: 'mdi-alert-outline', info: 'mdi-information-variant', primary: 'mdi-plus', error: 'mdi-close' };
            return map[type] || 'mdi-circle';
        },
        getLogColor(type) {
            const map = { success: 'success', warning: 'warning', info: 'info', primary: 'primary', error: 'error' };
            return map[type] || 'slate';
        }
    }
};
</script>

<style scoped>
.section-icon-box {
    width: 48px;
    height: 48px;
    background: #eff6ff;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.timeline-container {
    padding-right: 20px;
}

.h-52 {
    height: 52px !important;
}
</style>
