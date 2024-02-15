const puppeteer = require("puppeteer");
const fs = require("fs");

const { exec } = require("child_process");
const chain = process.argv[2]
const address = process.argv[3]
const file_path = process.argv[4]
const indicator = process.argv[5]
const user_style = process.argv[6]
const user_interval = process.argv[7]
const page_indcators = {
  'OBV': "On Balance Volume",
  'ADI': "Accumulation/Distribution",
  'ADX': "Average Directional Index",
  'AO': "Aroon",
  'MACD': "MACD",
  'RSI': "Relative Strength Index",
  'SO': "Stochastic",
  'BB': "Bollinger Bands",
  'IC': "Ichimoku Cloud",
  'MA': "MA Cross",
  'MAE': "MA with EMA Cross",
  'SD':  "Standard Deviation",
  'VWAP': "VWAP",
  'VPVR': "Volume Profile Visible Range",
  'VO': "Volume Oscillator"
}

default_interval = {
  '5m':"5 minutes",
  "1h":"1 hour",
  "6h":"4 hours",
  "1D":"1 day"
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}


(async () => {
  let indicato;
  if (indicator==="nu"){
    indicato=[]
  }
  else {
    indicato = indicator.split(",")
  }
  console.log(indicato)
  // await sleep(1000);
  // exec("killall chrome");
  // await sleep(1000);
  // exec(
  //   `"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --profile-directory="Default" --remote-debugging-port=9222`
  // );
  // await sleep(1000);

  const browserURL = "http://127.0.0.1:9222";

  const browser = await puppeteer.connect({ browserURL });
  const page = await browser.newPage()

  await page.setViewport({ width:1600, height: 900});
  
  await page.goto(
    `https://dexscreener.com/${chain}/${address}`,
    { timeout: 60000 }
  );
  // await sleep(5000);

  console.log("find frame")
  // open-indicators-dialog
  try{
    await page.waitForSelector('iframe[title="Financial Chart"]');
    let frameHandle;
    let frame;
    frameHandle = await page.$('iframe[title="Financial Chart"]');
    frame = await frameHandle.contentFrame()
    await frame.waitForSelector('div.group-MBOVGQRI div.wrap-n5bmFxyX span[tabindex="-1"]');
    await frame.$$eval('div.group-MBOVGQRI div.wrap-n5bmFxyX span[tabindex="-1"]', (el) => {el[3].click()});
    await sleep(1000)
    // await page.waitForSelector('iframe[name="tradingview_d6e53"]');
    // let frameHandle_full_chart;
    // let frame_full_chart;
    // frameHandle_full_chart = await page.$('iframe[name="tradingview_d6e53"]');
    // frame_full_chart = await frameHandle_full_chart.contentFrame()
    // const x = 200;
    // const y = 200;
    // // Move the mouse to the position and click
    // // await page.mouse.click(x, y);
    // await page.mouse.click(x, y, {button:'right'});
    
    await frame.waitForSelector('div[data-name="removeAllDrawingTools"] button.arrow-pbhJWNrt.accessible-pbhJWNrt', {timeout:1000});
    await frame.$eval('div[data-name="removeAllDrawingTools"] button.arrow-pbhJWNrt.accessible-pbhJWNrt', (el) => {el.click()}); 
    
    await frame.waitForSelector('div[data-name="remove-all"]', {timeout:1000});
    await frame.$eval('div[data-name="remove-all"]', (el) => {el.click()}); 
    // await frame.waitForSelector('div.menu-Tx5xMZww.context-menu.menuWrap-Kq3ruQo8 tr.item-GJX1EXhk.interactive-GJX1EXhk.normal-GJX1EXhk');
    // await frame.$$eval('div.menu-Tx5xMZww.context-menu.menuWrap-Kq3ruQo8 tr.item-GJX1EXhk.interactive-GJX1EXhk.normal-GJX1EXhk', (el) => {el[5].click()}); 
    await frame.waitForSelector('button[data-name="open-indicators-dialog"]', {timeout:1000});
    await frame.$$eval('button[data-name="open-indicators-dialog"]', (el) => {el[0].click()});
    for (let index = 0; index < indicato.length; index++) {
      let element = indicato[index];
      let title = page_indcators[element]
      console.log(title)
      await frame.waitForSelector(`div[data-title="${title}"]`, {timeout:1000});
      await frame.$eval(`div[data-title="${title}"]`, el => el.click());
    }
    await frame.waitForSelector('div[data-name="indicators-dialog"] button[data-name="close"]', {timeout:1000});
    await frame.$eval('div[data-name="indicators-dialog"] button[data-name="close"]', el => el.click());

    await frame.waitForSelector('button[data-tooltip="Bar\'s style"]', {timeout:1000});
    await frame.$$eval('button[data-tooltip="Bar\'s style"]', (el) => {el[0].click()});
    await frame.waitForSelector(`div[data-name="menu-inner"] div[data-value="${user_style}"]`, {timeout:1000});
    await frame.$eval(`div[data-name="menu-inner"] div[data-value="${user_style}"]`, (el) => {el.click()});
    // await sleep(2000)
    // const element = await frame.$('div.chart-container.top-full-width-chart.active');
    // const box = await element.boundingBox();
    await frame.waitForSelector(`button.button-S_1OCXUK.button-neROVfUe.button-GwQQdU8S.apply-common-tooltip.isInteractive-GwQQdU8S.isGrouped-GwQQdU8S.accessible-GwQQdU8S[aria-label="${default_interval[user_interval]}"]`, {timeout:1000});
    await frame.$$eval(`button.button-S_1OCXUK.button-neROVfUe.button-GwQQdU8S.apply-common-tooltip.isInteractive-GwQQdU8S.isGrouped-GwQQdU8S.accessible-GwQQdU8S[aria-label="${default_interval[user_interval]}"]`, (el) => {el[0].click()});
    // Take a screenshot of the specified element
    await sleep(2000)
    await page.screenshot({ path: file_path}); 
    await page.close();
    await browser.disconnect();
    await process.exit(0);
  }catch{
    await page.close()
    await page.close()
  }
})();


// document.querySelector('div.button-TPBYkbxL.button-gbkEfGm4.withText-gbkEfGm4.button-uO7HM85b.apply-common-tooltip.isInteractive-uO7HM85b').click()