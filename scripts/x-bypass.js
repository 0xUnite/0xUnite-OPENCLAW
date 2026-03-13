const playwright = require('playwright-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const enabledPlugins = StealthPlugin();
playwright.chromium.use(enabledPlugins);

async function main() {
  console.log('Launching browser with existing Chrome profile...');
  
  // Use existing Chrome profile
  const userDataDir = process.env.HOME + '/Library/Application Support/Google/Chrome';
  
  const browser = await playwright.chromium.launch({ 
    headless: false,
    userDataDir: userDataDir,
    args: [
      '--disable-blink-features=AutomationControlled',
      '--no-sandbox'
    ]
  });
  
  const context = await browser.contexts()[0] || await browser.newContext();
  const page = await context.newPage();
  
  try {
    console.log('Navigating to X.com...');
    await page.goto('https://x.com/i/status/2022889900237001179', { 
      waitUntil: 'networkidle',
      timeout: 30000 
    });
    
    console.log('Page title:', await page.title());
    console.log('URL:', page.url());
    
    // Wait for content
    await page.waitForTimeout(2000);
    
    const content = await page.content();
    console.log('Content length:', content.length);
    
    if (content.includes('errorContainer') || content.includes('Something went wrong')) {
      console.log('⚠️ X.com still showing error');
    } else {
      const text = await page.textContent('body');
      console.log('Text preview:', text.substring(0, 300));
    }
    
  } catch (e) {
    console.error('Error:', e.message);
  }
  
  await browser.close();
  console.log('Done');
}

main();
