const https = require('https');
https.get('https://cdn.ckeditor.com/ckeditor5/41.2.0/super-build/ckeditor.js', (res) => {
  let data = '';
  res.on('data', (chunk) => { data += chunk; });
  res.on('end', () => {
    console.log(data.substring(0, 500));
  });
});
