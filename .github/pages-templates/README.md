# GitHub Pages Templates

This directory contains HTML templates used by GitHub Actions workflows to generate the GitHub Pages site.

## Templates

### `index.html`
Main dashboard page that displays links to both Coverage and Allure reports.

**Placeholders:**
- `{{LAST_UPDATE}}` - Replaced with current UTC timestamp

**Used by:**
- `tests.yml` workflow (publish-allure job)
- `coverage.yml` workflow (publish-report job)

### `allure-placeholder.html`
Error page displayed when Allure report generation fails.

**Placeholders:**
- `{{BUILD_URL}}` - Replaced with GitHub Actions run URL

**Used by:**
- `tests.yml` workflow (publish-allure job)

### `allure-redirect.html`
Placeholder page with link to E2E Tests workflow when Allure report hasn't been generated yet.

**Placeholders:**
- `{{WORKFLOW_URL}}` - Replaced with E2E Tests workflow URL

**Used by:**
- `coverage.yml` workflow (publish-report job)

### `coverage-placeholder.html`
Error page displayed when Coverage report generation fails.

**Placeholders:**
- `{{BUILD_URL}}` - Replaced with GitHub Actions run URL

**Used by:**
- `coverage.yml` workflow (publish-report job) - when report fails

### `coverage-redirect.html`
Placeholder page with link to Coverage workflow when coverage report hasn't been generated yet.

**Placeholders:**
- `{{WORKFLOW_URL}}` - Replaced with Coverage workflow URL

**Used by:**
- `tests.yml` workflow (publish-allure job) - when coverage not yet run

### `allure-history.html`
History page showing all previous Allure test reports with build numbers and dates.

**Placeholders:**
- `{{BUILDS_JSON}}` - Replaced with JSON array of builds: `[{"number":"123","date":"2025-01-15 10:30 UTC"},...]`

**Used by:**
- `tests.yml` workflow (publish-allure job) - generates history page

### `coverage-history.html`
History page showing all previous Coverage reports with build numbers, dates, and coverage percentages.

**Placeholders:**
- `{{BUILDS_JSON}}` - Replaced with JSON array of builds: `[{"number":"123","date":"2025-01-15 10:30 UTC","coverage":85},...]`

**Used by:**
- `coverage.yml` workflow (publish-report job) - generates history page

## Report Versioning Structure

Reports are organized with full version history:

```
/allure/
  /latest/              ← Latest report (quick access)
  /builds/
    /123/               ← Report from build #123
    /124/               ← Report from build #124
  index.html            ← History page (allure-history.html)

/coverage/
  /latest/              ← Latest report (quick access)
  /builds/
    /123/               ← Report from build #123
  index.html            ← History page (coverage-history.html)
```

## How It Works

Both workflows checkout these templates using sparse-checkout and use `sed` to replace placeholders with actual values before deploying to GitHub Pages.

Example:
```bash
sed "s|{{LAST_UPDATE}}|$(date -u +"%Y-%m-%d %H:%M:%S UTC")|g" \
  .github/pages-templates/index.html > _site/index.html
```

## Benefits

- **Maintainability**: HTML is easier to edit in separate files
- **Reusability**: Same templates used by multiple workflows
- **Version Control**: Changes to page design are tracked separately
- **Clean Workflows**: Workflows are more readable without inline HTML
