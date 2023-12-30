import { test, expect } from '@playwright/test';

test('has correct titles', async ({ page }) => {
  await page.goto('/');

  await expect(page).toHaveTitle(/der bloggende schärmu/);
  await expect(page.locator('h1')).toHaveText('Schärmu\'s Blog');
});
