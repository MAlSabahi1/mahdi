from django.urls import path
from . import views

urlpatterns = [
    # ── Document Management (رفع/عرض/استبدال المرفقات) ──
    path('upload/', views.DocumentUploadView.as_view(), name='document-upload'),
    path('personnel/<str:military_number>/', views.PersonnelDocumentsView.as_view(), name='personnel-documents'),
    path('<int:pk>/replace/', views.DocumentReplaceView.as_view(), name='document-replace'),
    path('requirements/', views.AttachmentRequirementsView.as_view(), name='attachment-requirements'),
    path('validate/', views.ValidateAttachmentsView.as_view(), name='validate-attachments'),
]
