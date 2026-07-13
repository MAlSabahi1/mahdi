<template>
  <div class="ckeditor-container" :class="{ 'is-disabled': disabled }">
    <div ref="editorElement"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  height: {
    type: String,
    default: '300px'
  },
  placeholder: {
    type: String,
    default: 'اكتب المحتوى هنا...'
  },
  toolbar: {
    type: Array,
    default: null
  }
})

const emit = defineEmits(['update:modelValue'])

const editorElement = ref<HTMLElement | null>(null)
let editorInstance: any = null
let isUpdating = false

const loadCKEditor = () => {
  return new Promise((resolve) => {
    if ((window as any).CKEDITOR) {
      resolve(true)
      return
    }

    if (document.getElementById('ckeditor-script')) {
      // Script is loading, wait for it
      const interval = setInterval(() => {
        if ((window as any).CKEDITOR && (window as any).CKEDITOR.translations && (window as any).CKEDITOR.translations.ar) {
          clearInterval(interval)
          resolve(true)
        }
      }, 100)
      return
    }

    const script = document.createElement('script')
    script.id = 'ckeditor-script'
    script.src = 'https://cdn.ckeditor.com/ckeditor5/41.2.0/super-build/ckeditor.js'
    
    script.onload = () => {
      const scriptAr = document.createElement('script')
      scriptAr.src = 'https://cdn.ckeditor.com/ckeditor5/41.2.0/super-build/translations/ar.js'
      scriptAr.onload = () => {
        if (!(window as any).CKEDITOR.translations) (window as any).CKEDITOR.translations = {};
        (window as any).CKEDITOR.translations.ar = true;
        resolve(true)
      }
      document.head.appendChild(scriptAr)
    }
    document.head.appendChild(script)
  })
}

onMounted(async () => {
  await loadCKEditor()
  initEditor()
})

const initEditor = () => {
  if (!editorElement.value || !(window as any).CKEDITOR) return

  ;(window as any).CKEDITOR.ClassicEditor
    .create(editorElement.value, {
      language: 'ar',
      placeholder: props.placeholder,
      plugins: [
        'Essentials', 'Paragraph', 'Heading', 'Bold', 'Italic', 'Underline', 'Strikethrough',
        'Alignment', 'List', 'Table', 'TableToolbar', 'BlockQuote', 'Image', 'ImageUpload',
        'ImageToolbar', 'ImageCaption', 'ImageStyle', 'ImageResize', 'Base64UploadAdapter',
        'FontFamily', 'FontSize', 'FontColor', 'FontBackgroundColor'
      ],
      fontFamily: {
        options: [
          'default',
          { title: 'Arial', model: 'Arial, Helvetica, sans-serif' },
          { title: 'Courier New', model: 'Courier New, Courier, monospace' },
          { title: 'Georgia', model: 'Georgia, serif' },
          { title: 'Tahoma', model: 'Tahoma, Geneva, sans-serif' },
          { title: 'Times New Roman', model: 'Times New Roman, Times, serif' },
          { title: 'كايرو (Cairo)', model: 'Cairo, sans-serif' },
          { title: 'تجاول (Tajawal)', model: 'Tajawal, sans-serif' },
          { title: 'المراعي (Almarai)', model: 'Almarai, sans-serif' },
          { title: 'تشانجا (Changa)', model: 'Changa, sans-serif' },
          { title: 'لطيف (Lateef)', model: 'Lateef, serif' },
          { title: 'أميري (Amiri)', model: 'Amiri, serif' },
          { title: 'رقعة (Aref Ruqaa)', model: 'Aref Ruqaa, serif' },
          { title: 'نسخ (Noto Naskh)', model: 'Noto Naskh Arabic, serif' },
          { title: 'كوفي (Noto Kufi)', model: 'Noto Kufi Arabic, sans-serif' },
          { title: 'Traditional Arabic', model: 'Traditional Arabic, serif' }
        ],
        supportAllValues: true
      },
      fontSize: {
        options: [
          9, 10, 11, 12, 13, 14, 15, 16, 18, 20, 22, 24, 28, 32, 36
        ]
      },
      alignment: {
        options: [ 'left', 'right', 'center', 'justify' ]
      },
      toolbar: props.toolbar ? { items: props.toolbar } : {
        items: [
          'heading', '|',
          'fontFamily', 'fontSize', 'fontColor', 'fontBackgroundColor', '|',
          'bold', 'italic', 'underline', 'strikethrough', '|',
          'alignment', '|',
          'bulletedList', 'numberedList', '|',
          'insertTable', 'blockQuote', '|',
          'undo', 'redo', '|',
          'imageUpload'
        ]
      },
      image: {
        toolbar: ['imageTextAlternative', 'toggleImageCaption', 'imageStyle:inline', 'imageStyle:block', 'imageStyle:side']
      },
      table: {
        contentToolbar: ['tableColumn', 'tableRow', 'mergeTableCells']
      }
    })
    .then((editor: any) => {
      editorInstance = editor

      // Set initial data
      if (props.modelValue) {
        editor.setData(props.modelValue)
      }

      // Handle disabled state
      if (props.disabled) {
        editor.enableReadOnlyMode('custom-read-only')
      }

      // Set height
      editor.ui.view.editable.element.style.minHeight = props.height

      // Handle changes
      editor.model.document.on('change:data', () => {
        isUpdating = true
        emit('update:modelValue', editor.getData())
        setTimeout(() => { isUpdating = false }, 100)
      })
    })
    .catch((error: any) => {
      console.error('CKEditor Init Error:', error)
    })
}

watch(() => props.modelValue, (newValue) => {
  if (editorInstance && !isUpdating) {
    editorInstance.setData(newValue || '')
  }
})

watch(() => props.disabled, (newValue) => {
  if (editorInstance) {
    if (newValue) {
      editorInstance.enableReadOnlyMode('custom-read-only')
    } else {
      editorInstance.disableReadOnlyMode('custom-read-only')
    }
  }
})

onBeforeUnmount(() => {
  if (editorInstance) {
    editorInstance.destroy()
  }
})
</script>

<style>
.ck.ck-editor__editable_inline {
  direction: rtl;
  text-align: right;
  border-radius: 0 0 0.5rem 0.5rem !important;
  border-color: #d1d5db !important;
}
.ck.ck-toolbar {
  border-radius: 0.5rem 0.5rem 0 0 !important;
  border-color: #d1d5db !important;
  background: #f9fafb !important;
}
.ck.ck-button {
  cursor: pointer;
}
.dark .ck.ck-editor__editable_inline {
  background-color: #1f2937 !important;
  border-color: #374151 !important;
  color: #f3f4f6 !important;
}
.dark .ck.ck-toolbar {
  background-color: #111827 !important;
  border-color: #374151 !important;
}
.dark .ck.ck-button {
  color: #e5e7eb !important;
}
.dark .ck.ck-button:hover,
.dark .ck.ck-button.ck-on {
  background-color: #374151 !important;
}
</style>
