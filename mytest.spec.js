import {test, expect} from '@playwright/test';

test('my first', async ({ page }) => {
  await page.goto('https://www.saucedemo.com');

  await page.locator('input[name="user-name"]').fill('standard_user');
  await page.locator('input[name="password"]').fill('secret_sauce');
  await page.click('input[name="login-button"]');
  await page.waitForURL('https://www.saucedemo.com/inventory.html');
  await page.waitForTimeout(3000);

  await page.click("button[name=\"add-to-cart-sauce-labs-bolt-t-shirt\"]");
  await page.click("button[name=\"add-to-cart-test.allthethings()-t-shirt-(red)\"]");
  await expect(page.locator('.shopping_cart_badge')).toHaveText('2');
  await page.click('[data-test="shopping-cart-link"]');
  await page.waitForURL('https://www.saucedemo.com/cart.html');
  await page.waitForTimeout(1200);
  await page.click("button[name=\"remove-sauce-labs-bolt-t-shirt\"]");
  await page.waitForTimeout(1200);
  await expect(page.locator('.shopping_cart_badge')).toHaveText('1');

  //Continue Shopping
  await page.click("button[name=\"continue-shopping\"]");
  await page.waitForURL('https://www.saucedemo.com/inventory.html');
  await page.waitForTimeout(1200);
  await page.click("button[name=\"add-to-cart-sauce-labs-fleece-jacket\"]");
   await expect(page.locator('.shopping_cart_badge')).toHaveText('2');
  await page.click('[data-test="shopping-cart-link"]');
  await page.waitForURL('https://www.saucedemo.com/cart.html');
  await page.waitForTimeout(1200);

  //Checkout
  await page.click("button[name=\"checkout\"]");
  await page.waitForURL('**/checkout-step-one.html');
  await page.waitForTimeout(2000);

  //First negative path
  await page.locator('input[name="lastName"]').fill('Batocael');
  await page.locator('input[name="postalCode"]').fill('6000');
  await page.waitForTimeout(1000);
  await page.click('[data-test="continue"]');
  await page.waitForTimeout(1000);
  await expect(page.locator('[data-test="error"]')).toHaveText('Error: First Name is required');  

  //Second negative path
  await page.locator('input[name="firstName"]').fill('Rozellini');
  await page.locator('[data-test="lastName"]').clear();
    await page.locator('input[name="postalCode"]').fill('6000');
  await page.waitForTimeout(1000);
  await page.click('[data-test="continue"]');
  await expect(page.locator('[data-test="error"]')).toHaveText('Error: Last Name is required');  
  await page.waitForTimeout(1200);


  await page.locator('input[name="firstName"]').fill('Rozellini');
  await page.locator('input[name="lastName"]').fill('Batocael');
  await page.locator('input[name="postalCode"]').fill('6000');
  await page.waitForTimeout(1000);
  await page.click('[data-test="continue"]');
  await page.waitForTimeout(2000);

  await page.click('[data-test="finish"]');
  await page.waitForURL('https://www.saucedemo.com/checkout-complete.html');
  await page.waitForTimeout(2000);

  await page.click("button[name=\"back-to-products\"]");
  
});
