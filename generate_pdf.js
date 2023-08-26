const fs = require('fs');
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  const htmlFilePath = './generated_resume.html';
  let htmlContent = fs.readFileSync(htmlFilePath, 'utf8');

  const cssFilePath = '../dist/output.css';
  const cssContent = fs.readFileSync(cssFilePath, 'utf8');

  // Inject the CSS content into the HTML
  htmlContent = htmlContent.replace('</head>', `<style>${cssContent}</style></head>`);

  await page.setContent(htmlContent);

  // Generate a PDF
  const pdfFilePath = 'output.pdf';
  await page.pdf({ path: pdfFilePath, format: 'A4' });

  await browser.close();
})();