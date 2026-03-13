#!/usr/bin/env node

/**
 * X.com Tweet Fetcher using rebrowser-playwright
 * Usage: node x-fetch.js <tweet-url>
 * Example: node x-fetch.js https://x.com/i/status/2022889900237001179
 */

import { chromium } from 'rebrowser-playwright';

const args = process.argv.slice(2);
const url = args[0] || 'https://x.com/i/status/2022889900237001179';

async function fetchTweet(tweetUrl) {
  console.log('Launching browser...');
  
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
    console.log('Fetching:', tweetUrl);
    await page.goto(tweetUrl, { 
      waitUntil: 'domcontentloaded',
      timeout: 15000 
    });
    
    console.log('Title:', await page.title());
    
    // Wait for content to load
    await page.waitForTimeout(3000);
    
    // Get tweet content
    const tweet = await page.textContent('article').catch(() => 'N/A');
    
    if (tweet && tweet.length > 10) {
      console.log('\n=== Tweet Content ===');
      console.log(tweet.substring(0, 2000));
    } else {
      // Fallback: get main content
      const main = await page.textContent('main').catch(() => 'N/A');
      console.log('\n=== Main Content ===');
      console.log(main.substring(0, 1500));
    }
    
  } catch (e) {
    console.error('Error:', e.message);
  }
  
  await browser.close();
  console.log('\nDone');
}

fetchTweet(url);
