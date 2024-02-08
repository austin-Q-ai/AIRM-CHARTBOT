const puppeteer = require("puppeteer");
const fs = require("fs");
const { click } = require("puppeteer-utilz");

const { exec } = require("child_process");
const datasource = process.argv[2]
const blocsize = process.argv[3]
const file_path = process.argv[4]
let loading = false;

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

(async () => {

  // exec("killall chrome");
  // exec(
  //   `"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --profile-directory="Default" --remote-debugging-port=9222`
  // );
  // await sleep(1000);

  const browserURL = "http://127.0.0.1:9222";

  const browser = await puppeteer.connect({ browserURL });
  const page = await browser.newPage()

  await page.setViewport({ width:1600, height: 900});

  await page.goto(`https://www.tradingview.com/heatmap/crypto/#%7B%22dataSource"%3A"${datasource}"%2C%22blockColor"%3A%22change"%2C%22blockSize"%3A"${blocsize}"%2C%22grouping"%3A%22no_group"%7D`);

  await sleep(5000);
  try {
    await page.$eval('button.nav-button-znwuaSC1.size-large-znwuaSC1.close-button-urtYxNVo', el => el.click());
  } catch{}

  try {
    const element = await page.$('div.canvasContainer-OLfCe9c0');
    const box = await element.boundingBox();

    // Take a screenshot of the specified element
    await page.screenshot({ path: file_path, clip: box });
    await page.close();
    await browser.disconnect();
    await process.exit(0);
  } catch{
    await page.close()
    await page.close()
  }

})();


// document.querySelector('div.button-TPBYkbxL.button-gbkEfGm4.withText-gbkEfGm4.button-uO7HM85b.apply-common-tooltip.isInteractive-uO7HM85b').click()