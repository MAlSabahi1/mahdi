# Excel Ingestion UI/API Specification Document

This document outlines the architectural contract, asynchronous processing strategy, and Vue.js frontend specifications for the Personnel Data Excel Ingestion engine. It serves as the blueprint for building the user interface that interacts with the robust `import_raw_data` backend engine.

---

## 1. The API Contract (Backend Interface)

To support seamless uploads, previews, and final execution, the backend will expose a unified API endpoint designed to handle both immediate dry-runs and deferred asynchronous processing.

### **Endpoint Definition**
*   **URL:** `POST /api/v1/personnel/import/`
*   **Content-Type:** `multipart/form-data`
*   **Authentication:** Requires elevated admin privileges (e.g., Token/Session based auth with `can_import_data` permission).

### **Request Payload Parameters**
| Parameter | Type | Required | Description |
| :--- | :--- | :---: | :--- |
| `file` | File (Excel) | Yes | The `.xlsx` file containing the personnel data. |
| `preview_only` | Boolean | Yes | If `true`, triggers a synchronous `dry-run` to return parsing statistics without committing to the database. If `false`, initiates the actual import. |
| `sheet_name` | String | No | Optional sheet name to parse. Defaults to the active sheet. |

### **Response Formats**

#### A. Success: Dry-Run Preview (`preview_only: true`)
When previewing, the API responds synchronously with the anticipated results, providing the UI with everything needed for the dashboard.
```json
{
  "status": "success",
  "data": {
    "batch_id": "uuid-string",
    "stats": {
      "total_rows": 10543,
      "will_create": 10500,
      "will_update": 43,
      "will_skip": 0,
      "monthly_variables_detected": 3,
      "monthly_variables_names": ["متغير_يناير_2024", "متغير_فبراير_2024", "متغير_مارس_2024"],
      "name_corrections_pending": 120
    },
    "warnings": {
      "unmatched_departments": [
        {"raw_value": "إدارة المنشآت القديمة", "count": 45, "action": "Will map to NULL, raw value saved to notes"}
      ],
      "unknown_ranks": [],
      "unknown_statuses": [
        {"raw_value": "إجازة مفتوحة", "count": 2, "action": "Will default to 'بدون عمل'"}
      ]
    }
  }
}
```

#### B. Success: Actual Import Initiation (`preview_only: false`)
When committing the actual import, the API responds with a task tracking ID.
```json
{
  "status": "accepted",
  "message": "File accepted for processing.",
  "data": {
    "batch_id": "uuid-string",
    "task_id": "celery-task-uuid-string"
  }
}
```

#### C. Failure: Validation Errors
```json
{
  "status": "error",
  "error_code": "INVALID_FILE_FORMAT",
  "message": "The uploaded file is missing required columns (e.g., 'الرقم العسكري')."
}
```

---

## 2. Asynchronous Processing Strategy

Processing tens of thousands of rows cannot block the standard HTTP request-response cycle. The architecture relies on an asynchronous worker queue.

### **The Flow**
1.  **File Staging:** The Django view receives the file, saves it to a temporary quarantine/storage location (e.g., `/tmp/imports/` or an S3 bucket), and generates a `batch_id`.
2.  **Task Delegation:** The view dispatches a Celery task (e.g., `process_excel_import.delay(file_path, batch_id)`) and immediately returns a `task_id` to the client.
3.  **Background Execution:** A dedicated Celery worker executes the logic defined in `import_raw_data.py`.
4.  **Progress Tracking:**
    *   **Option A (WebSockets/Django Channels):** The worker pushes real-time progress updates (e.g., `{"progress": 45, "processed": 4500, "total": 10000}`) to a specific WebSocket channel subscribed to by the UI.
    *   **Option B (Polling):** The UI periodically calls a status endpoint (`GET /api/v1/personnel/import/status/{task_id}/`) reading from a Redis cache or a `TaskProgress` table updated by the worker.

---

## 3. Vue.js UI Component Architecture

The frontend must provide a frictionless, confidence-inspiring experience for the administrator handling massive datasets.

### **Core Components**

#### 1. `<ExcelDropzone />`
*   **Function:** The initial landing area for the user.
*   **Features:**
    *   Drag-and-drop support for `.xlsx` and `.csv` files.
    *   Client-side validation (file size limits, correct extension).
    *   Visual feedback during the file upload to the server.

#### 2. `<DryRunDashboard />` (The Preview Screen)
*   **Function:** Displays the results of the `preview_only: true` API call. This is the critical "Point of No Return" checkpoint.
*   **Features:**
    *   **Data Summary Cards:** Visual counters for "New Records", "Updates", "Dynamic Variables Found", and "Name Corrections Queued".
    *   **Dynamic Variable Alert:** A highlighted section showing exactly which "متغير" columns were detected, ensuring the user knows no data is being dropped.
    *   **Soft Mapping Warning Panel:** A dedicated alert box (using yellow/amber warning colors) detailing the "Unmatched Departments".
        *   *UX Note:* Explicitly explain to the user: *"The following X departments were not found in the system hierarchy. Personnel will still be imported, but their department fields will be empty, and the original text will be saved in their 'Notes' field."*
    *   **Action Buttons:** `[Cancel & Discard]` vs. `[Confirm & Start Import]`.

#### 3. `<ImportProgressBar />`
*   **Function:** Displays real-time progress once the actual import begins.
*   **Features:**
    *   Listens to WebSockets or polls the backend.
    *   Displays a fluid progress bar, estimated time remaining (ETA), and rows processed per second.

---

## 4. Error Handling & Quarantine UX

Data integrity relies on visibility into what went wrong.

### **Quarantine Management Interface**
If specific rows fail database validation completely (e.g., extreme corruption not handled by Soft Mapping) or if the import encounters systemic errors, the system must not silently drop them.

1.  **`<ErrorDataGrid />` Component:**
    *   Reads from the `RawDataImport` model where `status = 'error'`.
    *   Displays a high-performance Vue grid (e.g., AG-Grid or similar) showing the raw Excel data alongside the specific validation error message generated by Django.
2.  **Actionable Recoveries:**
    *   **Download Error Report:** A button to export the failed rows back into an Excel file (`download_errors.xlsx`). The admin can fix the typos in Excel and re-upload just that file.
    *   *(Future Enhancement)* **Inline Editing:** Allow the admin to correct the specific raw data fields directly in the grid and click "Retry Row".

### **System Crash Recovery**
If the Celery worker dies mid-process, the UI should detect a stalled task (no progress updates for > 30 seconds) and display a clear error message allowing the user to safely retry or resume based on the `batch_id`.

---

## 5. Pluggable Column Validation Architecture

To ensure the engine is highly scalable and strictly enforces data integrity, the backend will implement a **Column-by-Column Validation Engine**. The UI must be capable of rendering these granular errors intuitively.

### **Backend Design Philosophy**
1. **Isolated Validation Classes:** Every column (e.g., `national_id`, `military_number`, `phone_number`) will have its own isolated validation class/function in the backend (e.g., `NationalIDValidator`).
2. **Extensibility:** The architecture must be "pluggable." Adding a new rule (e.g., "National ID must be exactly 11 digits") requires only adding a new rule to that column's validator without touching the core import logic.
3. **Comprehensive Testing:** Because rules are isolated, each column validator can be unit-tested independently with a high degree of coverage.

### **Surfacing Errors to the UI**
When a row fails validation, the API will not just return a generic "Row Failed" error. It will return a structured JSON object mapping the exact column to its specific violations.

**Example Error Payload in Quarantine Data:**
```json
{
  "row_index": 452,
  "status": "error",
  "errors": {
    "الرقم الوطني": ["National ID must contain exactly 11 digits.", "This ID is already registered to another user."],
    "تاريخ الميلاد": ["Date is in the future."]
  },
  "raw_data": { ... }
}
```

### **UI Integration for Cell-Level Errors**
*   In the `<ErrorDataGrid />`, cells containing errors will be highlighted in **red**.
*   Hovering over the red cell will display a tooltip containing the exact error messages generated by the backend validator.
*   This ensures the administrator knows *exactly* which cell needs correcting before re-uploading, eliminating guesswork.

---

## 6. Active Month EAV Mutation (Current Period Processing)

While bulk historical data is uploaded via Excel files, day-to-day administrative data entry for the *current* month requires a lightning-fast, spreadsheet-like interface. To avoid corrupting the database schema with temporary columns (Anti-Pattern), we implemented a **Direct EAV Mutation API**.

### **Architectural Strategy**
1. **No Temporary Columns:** The `PersonnelMaster` table remains strictly normalized. There is no `current_month_variable` temporary column.
2. **Dynamic Joining (Prefetch):** The Frontend requests a list of personnel for a specific active month (e.g., `?month=2026-05`). The Backend dynamically joins the `HistoricalMonthlyVariables` table for that exact month and injects it as a `current_variable` field in the API response.
3. **Inline Upserting:** When an admin types a value into the Data Grid, the Frontend sends a `PATCH` request to the `/api/v1/personnel/upsert-variable/` endpoint. The Backend immediately performs an `update_or_create` on the `HistoricalMonthlyVariables` table.

### **Frontend Implementation**
*   **The Grid Column:** The Data Grid will display a dynamic column titled "متغير الشهر الحالي" (Current Month Variable).
*   **Data Binding:** This column is bound to the `current_variable` field returned by the `active-variables` endpoint.
*   **Auto-Save (Debounced):** Editing this cell triggers a debounced API call to save the data immediately to the EAV store. If the cell is cleared, the backend deletes the corresponding EAV record.
*   **Export Integration:** A "Monthly Services Export" service aggregates the core personnel data with the EAV variables for the selected month, generating a flat Excel file that perfectly mimics the Ministry's requested format.
