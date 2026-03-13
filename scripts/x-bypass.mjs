import { chromium } from 'rebrowser-playwright';

async function main() {
  console.log('Launching rebrowser-playwright...');
  
  const browser = await chromium.launch({
    headless: false,
    channel: 'chrome'
  });
  
  const context = await browser.newContext();
  const page = await context.newPage();
  
  // Remove webdriver property
  await context.addInitScript(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
  });
  
  try {
    console.log('Navigating to X.com...');
    await page.goto('https://x.com/i/status/2022889900237001179', { 
      waitUntil: 'networkidle',
      timeout: 30000 
    });
    
    console.log('Page title:', await page.title());
    console.log('URL:', page.url());
    
    // Wait for content
    await page.waitForTimeout(3000);
    
    const content = await page.content();
    console.log('Content length:', content.length);
    
    if (content.includes('errorContainer') || content.includes('Something went wrong')) {
      console.log('⚠️ X.com showing error page');
      const errorText = await page.textContent('.errorContainer').catch(() => 'N/A');
      console.log('Error:', errorText);
    } else {
      console.log('✅ Success! Content loaded');
      const text = await page.textContent('body');
      console.log('Text preview:', text.substring(0, 500));
    }
    
  } catch (e) {
    console.error('Error:', e.message);
  }
  
  await browser.close();
  console.log('Done');
}

main();
