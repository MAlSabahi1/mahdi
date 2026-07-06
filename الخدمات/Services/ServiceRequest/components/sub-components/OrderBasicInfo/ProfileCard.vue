<template>
  <div class="profile-card-pro" :class="[type]">
    <div class="d-flex align-center relative-z">
      <!-- Avatar/Icon Architecture -->
      <div class="visual-identity ml-5">
        <div v-if="type === 'user'" class="avatar-wrapper">
          <v-avatar :color="avatarColor" size="64" class="pro-avatar">
            <template v-if="image">
              <v-img :src="image" cover></v-img>
            </template>
            <span v-else-if="initials" class="text-h6 font-weight-black text-white">{{ initials }}</span>
            <v-icon v-else icon="mdi-account" color="white" size="32"></v-icon>
          </v-avatar>
          <div class="status-indicator"></div>
        </div>
        <div v-else class="org-icon-wrapper">
          <div class="icon-bg-glass"></div>
          <v-icon :icon="icon || 'mdi-office-building-marker-outline'" size="32" :color="iconColor"
            class="pro-org-icon"></v-icon>
        </div>
      </div>
  
      <!-- Content Stack -->
      <div class="content-stack flex-grow-1">
        <div class="d-flex align-center justify-space-between mb-1">
          <h3 class="profile-title">{{ title }}</h3>
        </div>
        <div class="profile-subtitle d-flex align-center">
          <v-icon icon="mdi-shield-check-outline" size="12" class="ml-1 opacity-60"></v-icon>
          {{ subtitle }}
        </div>
      </div>
    </div>

    <!-- Contact Info Strip -->
    <div class="contact-strip-pro mt-4">
      <div class="d-flex align-center flex-grow-1">
        <div class="contact-icon-box">
          <v-icon :icon="infoIcon" size="14" :color="type === 'user' ? 'primary' : 'indigo'"></v-icon>
        </div>
        <div class="d-flex flex-column overflow-hidden ml-2">
          <span class="text-tiny text-slate-400 font-weight-bold mb-n1">التواصل</span>
          <span class="contact-value text-truncate" :class="infoClass">
            {{ infoValue }}
          </span>
        </div>
      </div>
      <v-btn icon="mdi-arrow-left" variant="text" size="x-small" class="action-arrow"></v-btn>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProfileCard',
  props: {
    type: { type: String, default: 'user' }, // 'user' or 'org'
    title: { type: String, required: true },
    subtitle: { type: String, required: true },
    image: { type: String, default: '' },
    initials: { type: String, default: '' },
    avatarColor: { type: String, default: 'primary' },
    icon: { type: String, default: '' },
    iconColor: { type: String, default: 'indigo-accent-2' },
    infoIcon: { type: String, default: 'mdi-email-outline' },
    infoValue: { type: String, required: true },
    infoClass: { type: String, default: 'text-slate-600' }
  },
  data() {
    return {
      // isHovered: false
    };
  }
};
</script>

<style scoped>
.profile-card-pro {
  background: #ffffff;
  border-radius: 16px;
  border: 1px solid #f1f5f9;
  padding: 16px 20px;
  position: relative;
  overflow: hidden;
  height: 100%;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
}

/* .profile-card-pro:hover {
  transform: translateY(-2px);
  border-color: #e2e8f0;
  box-shadow: 0 12px 20px -5px rgba(0, 0, 0, 0.05);
}

.card-glow {
  position: absolute;
  top: -40%;
  right: -40%;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(37, 99, 235, 0.04) 0%, transparent 70%);
  pointer-events: none;
  transition: all 0.6s ease;
}

.profile-card-pro:hover .card-glow {
  background: radial-gradient(circle, rgba(37, 99, 235, 0.06) 0%, transparent 70%);
}

.card-mesh {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(#64748b 0.3px, transparent 0.3px);
  background-size: 16px 16px;
  opacity: 0.02;
  pointer-events: none;
} */

.relative-z {
  z-index: 2;
}

/* Avatar & Icon Styling */
.visual-identity {
  flex-shrink: 0;
  position: relative;
}

.pro-avatar {
  border: 2px solid white;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
  transition: all 0.4s ease;
}

.profile-card-pro:hover .pro-avatar {
  transform: scale(1.02) rotate(-2deg);
}

.status-indicator {
  position: absolute;
  bottom: 2px;
  left: 2px;
  width: 13px;
  height: 13px;
  background: #10b981;
  border: 2px solid white;
  border-radius: 50%;
  z-index: 2;
}

.org-icon-wrapper {
  width: 56px;
  height: 56px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-bg-glass {
  position: absolute;
  inset: 0;
  background: #f8fafc;
  border: 1px solid #f1f5f9;
  border-radius: 14px;
  /* transform: rotate(-3deg); */
  /* transition: all 0.4s ease; */
}

.profile-card-pro:hover .icon-bg-glass {
  /* transform: rotate(3deg) scale(1.02); */
  background: #eff6ff;
}

.pro-org-icon {
  z-index: 1;
}

/* Text Content */
.profile-title {
  font-size: 16px;
  font-weight: 800;
  color: #0f172a;
  line-height: 1.2;
}

.profile-subtitle {
  font-size: 12px;
  font-weight: 700;
  color: #64748b;
}

/* Live Status Animation */
.live-status {
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.pulse-dot {
  width: 4px;
  height: 4px;
  background: white;
  border-radius: 50%;
  display: inline-block;
}


/* Contact Strip */
.contact-strip-pro {
  background: #f8fafc;
  border-radius: 12px;
  padding: 10px 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 16px;
  transition: all 0.3s ease;
  border: 1px solid #f1f5f9;
}

.profile-card-pro:hover .contact-strip-pro {
  background: white;
  border-color: #e2e8f0;
}

.contact-icon-box {
  width: 32px;
  height: 32px;
  background: white;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 12px;
  border: 1px solid #f1f5f9;
}

.contact-value {
  font-size: 12px;
  font-weight: 800;
  color: #334155;
}

.action-arrow {
  color: #94a3b8;
  transition: all 0.3s ease;
}

.profile-card-pro:hover .action-arrow {
  transform: translateX(-4px);
  color: #2563eb;
}

.text-tiny {
  font-size: 9px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

@media (max-width: 600px) {
  .profile-card-pro {
    padding: 14px 16px;
  }

  .visual-identity {
    margin-left: 12px !important;
  }
}
</style>
