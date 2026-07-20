export function exportToCSV(columns: any[], data: any[], filename = 'export.csv') {
  if (!data || !data.length) {
    return;
  }

  // Extract visible columns
  const visibleColumns = columns.filter(col => col.key !== 'actions');

  // Create headers row
  const headers = visibleColumns.map(col => `"${col.label || col.key}"`).join(',');

  // Create data rows
  const rows = data.map(row => {
    return visibleColumns.map(col => {
      let val = row[col.key] ?? '';
      // Escape quotes and format as string to preserve leading zeros in CSV
      val = String(val).replace(/"/g, '""');
      return `"${val}"`;
    }).join(',');
  });

  // Combine headers and rows
  const csvContent = [headers, ...rows].join('\n');

  // Add BOM for Excel Arabic support
  const bom = new Uint8Array([0xef, 0xbb, 0xbf]);
  const blob = new Blob([bom, csvContent], { type: 'text/csv;charset=utf-8;' });

  // Trigger download
  const link = document.createElement('a');
  if (link.download !== undefined) {
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }
}

import * as ExcelJS from 'exceljs'
import { saveAs } from 'file-saver'

export async function exportToExcel(
  columns: any[], 
  data: any[], 
  filename = 'export.xlsx', 
  reportTitle = 'الكشف الشهري',
  isCompact: boolean = true
) {
  if (!data || !data.length) {
    return;
  }

  // Extract visible columns
  const visibleColumns = columns.filter(col => col.key !== 'actions');
  const colCount = visibleColumns.length;

  const workbook = new ExcelJS.Workbook();
  workbook.creator = 'نظام الموارد البشرية';
  workbook.created = new Date();

  const worksheet = workbook.addWorksheet(reportTitle.substring(0, 31), {
    views: [{ rightToLeft: true, showGridLines: false }],
    pageSetup: { paperSize: 9, orientation: 'landscape', fitToPage: true, fitToWidth: 1, fitToHeight: 0 }
  });

  // 1. Setup Columns Widths (Auto-fit with generous Arabic text padding)
  worksheet.columns = visibleColumns.map(col => {
    // Calculate the maximum length of content in this column
    let maxLength = (col.label || col.key).length;
    data.forEach(row => {
      const val = row[col.key];
      if (val !== null && val !== undefined) {
        const valStr = String(val);
        if (valStr.length > maxLength) maxLength = valStr.length;
      }
    });

    let finalWidth = 10;

    if (isCompact) {
      // Compact fit: Arabic text connects (ligatures), so it physically takes less width than char count
      finalWidth = Math.min(22, Math.max(6, (maxLength * 0.8) + 1));

      // Explicit visual overrides for specific known columns
      if (col.key === 'index') {
        finalWidth = 4.5; // Keep index column very small
      } else if (['military_number', 'national_id', 'phone', 'officer_number'].includes(col.key)) {
        // Numerical columns (English digits) are wider and don't connect
        finalWidth = Math.max(9, maxLength + 0.5);
      } else if (['unit', 'status', 'expense_status', 'status_type', 'category', 'rank', 'job_title'].includes(col.key)) {
        // Exact fit for clear Arabic text columns (tightest possible without wrapping)
        finalWidth = Math.max(5, maxLength * 0.75 + 0.5);
      } else if (['full_name', 'name'].includes(col.key)) {
        finalWidth = Math.min(28, Math.max(15, maxLength * 0.9));
      } else if (['notes', 'remarks'].includes(col.key)) {
        finalWidth = Math.min(25, Math.max(12, maxLength * 0.9));
      }
    } else {
      // Spacious fit: comfortable but reasonable padding (not overly wide)
      finalWidth = Math.min(32, Math.max(10, (maxLength * 1.05) + 3));
      
      if (col.key === 'index') {
        finalWidth = 5;
      } else if (['military_number', 'national_id', 'phone', 'officer_number'].includes(col.key)) {
        finalWidth = Math.max(12, maxLength + 2);
      } else if (['status', 'status_type', 'force_classification', 'category'].includes(col.key)) {
        finalWidth = Math.max(14, maxLength * 0.95 + 3);
      } else if (['full_name', 'name'].includes(col.key)) {
        finalWidth = Math.max(22, maxLength * 1.05 + 2);
      } else if (['notes', 'remarks'].includes(col.key)) {
        finalWidth = Math.max(20, maxLength * 1.05 + 2);
      }
    }

    return {
      key: col.key,
      width: finalWidth
    };
  });

  // ==========================================
  // 1. MAIN TITLE (Free Floating)
  // ==========================================
  const colCountSafe = Math.max(colCount || 1, 3);
  const row1 = worksheet.addRow([reportTitle]);
  row1.height = 30;
  worksheet.mergeCells(1, 1, 1, colCountSafe);

  const titleCell = worksheet.getCell(1, 1);
  titleCell.font = { name: 'Cairo', size: 14, bold: true, color: { argb: 'FF000000' }, underline: 'single' };
  titleCell.alignment = { vertical: 'middle', horizontal: 'center' };
  // No background, no borders for title

  // Row 2: Empty Spacer
  worksheet.addRow([]);

  // ==========================================
  // 2. DATA TABLE
  // ==========================================
  const tableStartRow = 3;
  const headerLabels = visibleColumns.map(c => c.label || c.key);
  const headerRow = worksheet.addRow(headerLabels);
  // Removed hardcoded height to allow auto-fit for wrapped headers

  headerRow.eachCell((cell) => {
    cell.fill = {
      type: 'pattern',
      pattern: 'solid',
      fgColor: { argb: 'FFF3F4F6' }
    };
    cell.font = { name: 'Cairo', size: 11, bold: true, color: { argb: 'FF000000' } };
    cell.alignment = { vertical: 'middle', horizontal: 'center', wrapText: true };
    cell.border = {
      top: { style: 'thick', color: { argb: 'FF000000' } }, // Thick top for table header
      left: { style: 'thin', color: { argb: 'FF000000' } },
      bottom: { style: 'medium', color: { argb: 'FF000000' } },
      right: { style: 'thin', color: { argb: 'FF000000' } }
    };
  });

  data.forEach((rowData, index) => {
    const rowValues = visibleColumns.map(col => {
      const val = rowData[col.key];
      return (val !== null && val !== undefined && val !== '') ? val : '—';
    });

    const row = worksheet.addRow(rowValues);
    // Removed hardcoded height to allow auto-fit for multi-line wrapped text


    const isEven = index % 2 === 0;
    row.eachCell((cell, colNumber) => {
      const colKey = visibleColumns[colNumber - 1]?.key;
      const rightAlignCols = ['notes', 'remarks', 'appointment_info'];
      const align = rightAlignCols.includes(colKey) ? 'right' : 'center';

      cell.fill = {
        type: 'pattern',
        pattern: 'solid',
        fgColor: { argb: isEven ? 'FFFFFFFF' : 'FFF9FAFB' }
      };

      const isName = ['full_name', 'name'].includes(colKey);
      cell.font = { name: 'Cairo', size: 10, bold: isName, color: { argb: 'FF000000' } };
      cell.alignment = { vertical: 'middle', horizontal: align, wrapText: true, indent: align === 'right' ? 1 : 0 };

      cell.border = {
        top: { style: 'thin', color: { argb: 'FF000000' } },
        left: { style: 'thin', color: { argb: 'FF000000' } },
        bottom: { style: 'thin', color: { argb: 'FF000000' } },
        right: { style: 'thin', color: { argb: 'FF000000' } }
      };
    });
  });

  // Apply Thick Outer Border ONLY to the Data Table
  const tableEndRow = worksheet.lastRow.number;
  for (let r = tableStartRow; r <= tableEndRow; r++) {
    const row = worksheet.getRow(r);
    const firstCell = row.getCell(1);
    const lastCell = row.getCell(colCountSafe);

    firstCell.border = { ...firstCell.border, right: { style: 'thick', color: { argb: 'FF000000' } } };
    lastCell.border = { ...lastCell.border, left: { style: 'thick', color: { argb: 'FF000000' } } };

    // Bottom border for the last row of the table
    if (r === tableEndRow) {
      for (let c = 1; c <= colCountSafe; c++) {
        const cCell = row.getCell(c);
        cCell.border = { ...cCell.border, bottom: { style: 'thick', color: { argb: 'FF000000' } } };
      }
    }
  }

  // ==========================================
  // 4. FOOTER
  // ==========================================
  worksheet.addRow([]); // Spacer
  const footerRow = worksheet.addRow([`إجمالي السجلات: ${data.length}`]);
  footerRow.height = 30;
  worksheet.mergeCells(footerRow.number, 1, footerRow.number, colCountSafe);
  const footerCell = footerRow.getCell(1);
  footerCell.font = { name: 'Cairo', size: 12, bold: true, color: { argb: 'FF000000' } };
  footerCell.alignment = { vertical: 'middle', horizontal: 'right', indent: 1 };
  // Footer is free-floating, no borders

  // Generate buffer and trigger download
  const buffer = await workbook.xlsx.writeBuffer();
  const blob = new Blob([buffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
  saveAs(blob, filename);
}
