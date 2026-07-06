<template>
    <div class="official-archive-header">
        <div class="masthead-chassis pa-4 pa-md-6">
            <v-row align="center" no-gutters>
                <!-- Academic Identity -->
                <v-col cols="12" sm="12" md="auto">
                    <div class="d-flex align-center ga-4 ga-md-5">
                        <div class="brand-monolith-prime d-none d-sm-flex">
                            <v-icon color="primary" size="26">{{ icon }}</v-icon>
                        </div>
                        <div class="identity-anchor">
                            <div class="d-flex align-center ga-3 mb-1 flex-wrap">
                                <h1 class="archive-title-text">{{ title }}</h1>
                                <div class="live-status-badge">
                                    <span class="status-dot"></span>
                                    <span class="status-label">مركز التتبع والرقابة</span>
                                </div>
                            </div>
                            <div class="archive-intel d-none d-sm-block">
                                <v-icon icon="mdi-shield-check" size="14" class="ml-2" color="success"></v-icon>
                                <span>توثيق آلي لكافة الإجراءات الإدارية المعتمدة</span>
                            </div>
                        </div>
                    </div>
                </v-col>

                <v-spacer class="d-none d-md-block" />

                <!-- Operational Tools Matrix -->
                <v-col cols="12" sm="12" md="auto" class="mt-5 mt-md-0">
                    <div class="d-flex align-center flex-wrap ga-3 ga-md-4">
                        <!-- Responsive Search -->
                        <div class="search-vault">
                            <v-icon icon="mdi-magnify" class="ml-2 ml-md-3" color="slate-400" size="18"></v-icon>
                            <input :value="search" @input="$emit('update:search', $event.target.value)" type="text"
                                placeholder="البحث..." class="orbit-input" />
                        </div>

                        <!-- Action Cluster -->
                        <div class="d-flex align-center ga-2 ga-md-3 action-cluster">
                            <v-btn color="primary" variant="flat" class="prime-action-btn flex-grow-1 flex-md-grow-0"
                                height="44" :loading="loading" @click="$emit('export')">
                                <v-icon start size="18" class="d-none d-sm-inline-flex">mdi-file-export-outline</v-icon>
                                تصدير تقرير
                            </v-btn>

                            <v-btn icon variant="outlined" color="slate-200" class="tech-refresh-btn" width="44"
                                height="44" @click="$emit('refresh')">
                                <v-icon color="slate-600" size="20">mdi-refresh</v-icon>
                            </v-btn>
                        </div>
                    </div>
                </v-col>
            </v-row>
        </div>
    </div>
</template>

<script>
export default {
    name: 'RecordsHeader',
    props: {
        title: { type: String, default: 'سجلات العمليات' },
        icon: { type: String, default: 'mdi-shield-check' },
        loading: { type: Boolean, default: false },
        search: { type: String, default: '' }
    },
    emits: ['export', 'refresh', 'update:search']
};
</script>

<style scoped>

.official-archive-header {
    width: 100%;
}

.masthead-chassis {
    background: #ffffff;
    border: 1px solid #e2e8f0;
}

.brand-monolith-prime {
    width: 48px;
    height: 48px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.archive-title-text {
    font-size: 1.35rem !important;
    font-weight: 900 !important;
    color: #0f172a;
    letter-spacing: -0.02em;
    margin-bottom: 0;
}

.live-status-badge {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 2px 10px;
    background: #f0fdf4;
    border: 1px solid #dcfce7;
    border-radius: 100px;
}

.status-dot {
    width: 6px;
    height: 6px;
    background: #22c55e;
    border-radius: 50%;
}

.status-label {
    font-size: 10px;
    font-weight: 800;
    color: #166534;
    text-transform: uppercase;
}

.archive-intel {
    font-size: 12px;
    color: #94a3b8;
    font-weight: 600;
}

.search-vault {
    display: flex;
    align-items: center;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    height: 44px;
    padding: 0 12px;
    flex: 1;
    min-width: 200px;
}

.orbit-input {
    flex: 1;
    border: none;
    background: transparent;
    outline: none;
    font-size: 13.5px;
    font-weight: 600;
    color: #1e293b;
    padding-right: 4px;
}

.prime-action-btn {
    text-transform: none;
    font-size: 13px;
    font-weight: 800 !important;
    border-radius: 10px !important;
}

.tech-refresh-btn {
    background: #ffffff !important;
    border-color: #e2e8f0 !important;
    border-radius: 10px !important;
}

.action-cluster {
    flex: 1;
}

@media (min-width: 960px) {
    .search-vault {
        max-width: 300px;
        flex: none;
    }

    .action-cluster {
        flex: none;
    }

    .archive-title-text {
        font-size: 1.5rem !important;
    }
}

@media (max-width: 600px) {
    .masthead-chassis {
        padding: 16px !important;
    }

    .archive-title-text {
        font-size: 1.2rem !important;
    }

    .action-cluster {
        width: 100%;
    }

    .search-vault {
        width: 100%;
        min-width: 100%;
    }
}
</style>
