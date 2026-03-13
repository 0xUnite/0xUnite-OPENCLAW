import { chromium } from 'rebrowser-playwright';

async function main() {
  console.log('Launching...');
  
  const browser = await chromium.launch({
    headless: false,
    channel: 'chrome',
    args: ['--no-sandbox']
  });
  
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
  });
  
  const page = await context.newPage();
  
  await context.addInitScript(() => {
    delete Object.getPrototypeOf(navigator).webdriver;
  });
  
  try {
    console.log('Goto X...');
    const response = await page.goto('https://x.com/i/status/2022889900237001179', { 
      timeout: 15000 
    });
    console.log('Status:', response?.status());
    console.log('URL:', page.url());
    
    await page.waitForTimeout(2000);
    
    const title = await page.title();
    console.log('Title:', title);
    
  } catch (e) {
    console.error('Error:', e.message);
  }
  
  await browser.close();
}

main();
