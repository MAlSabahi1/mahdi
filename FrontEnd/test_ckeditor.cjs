const https = require('https');
https.get('https://cdn.ckeditor.com/ckeditor5/41.2.0/super-build/ckeditor.js', (res) => {
  let data = '';
  res.on('data', (chunk) => { data += chunk; });
  res.on('end', () => {
    const match = data.match(/window\.CKEDITOR/);
    console.log(match ? 'Found window.CKEDITOR' : 'Not found');
    const alignmentMatch = data.match(/Alignment/);
    console.log(alignmentMatch ? 'Found Alignment' : 'Not found');
  });
});
