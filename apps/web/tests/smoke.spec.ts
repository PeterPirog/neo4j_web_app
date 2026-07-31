import { expect, test } from "@playwright/test";

test("dashboard loads", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Neo4j Graph Platform" })).toBeVisible();
});

test("navigation contains main product areas", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("navigation")).toContainText("People");
  await expect(page.getByRole("navigation")).toContainText("Cities");
  await expect(page.getByRole("navigation")).toContainText("Relations");
  await expect(page.getByRole("navigation")).toContainText("Residences");
  await expect(page.getByRole("navigation")).toContainText("Permissions");
  await expect(page.getByRole("navigation")).toContainText("AI / GraphRAG");
  await expect(page.getByRole("navigation")).toContainText("ML");
});

test("people page loads", async ({ page }) => {
  await page.goto("/people");
  await expect(
    page.getByRole("heading", { exact: true, name: "People" }),
  ).toBeVisible();
});

test("relations page loads", async ({ page }) => {
  await page.goto("/relations");
  await expect(
    page.getByRole("heading", { exact: true, name: "Relations" }),
  ).toBeVisible();
});

test("cities page loads", async ({ page }) => {
  await page.goto("/cities");
  await expect(
    page.getByRole("heading", { exact: true, name: "Cities" }),
  ).toBeVisible();
});

test("residences page loads", async ({ page }) => {
  await page.goto("/residences");
  await expect(
    page.getByRole("heading", { exact: true, name: "Residences" }),
  ).toBeVisible();
});
