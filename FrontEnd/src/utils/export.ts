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
