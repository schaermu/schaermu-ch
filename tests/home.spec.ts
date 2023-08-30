import { test, expect } from '@playwright/test';

test('has correct titles', async ({ page }) => {
  await page.goto('/');

  await expect(page).toHaveTitle(/der begrüssende schärmu/);
  await expect(page.locator('h1')).toHaveText('Willkommen!');
});

test('contains 2 cards linking to blog and cv', async ({ page }) => {
  await page.goto('/');
  const articles = await page.locator('article');

  await expect(articles).toHaveCount(2);

  for (const article of await page.locator('article').all()) {
    await expect(article.locator('a').nth(0)).toHaveAttribute('href', /(blog|cv)/)
  }
});