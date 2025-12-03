# Tailwind CSS v4 Upgrade Guide

## Overview

**Purpose:** Guide for upgrading Tailwind CSS projects from v3 to v4.

**Key Points:**
- Tailwind CSS v4.0 is a major version with some breaking changes
- Targets Safari 16.4+, Chrome 111+, and Firefox 128+
- **Important!** Use upgrade tool for most migrations

## Upgrade Options

### Using Upgrade Tool

- **Recommended Method:** Use official upgrade tool
- Command:
```terminal
$ npx @tailwindcss/upgrade
```

**Requirements and Recommendations:**
- Requires Node.js 20 or higher
- Run in a new git branch
- Carefully review diff
- Test project thoroughly after migration

**Important!** Review all breaking changes in v4 even when using the upgrade tool - there may be additional changes in your project that the tool doesn't catch

### Manual Upgrade Steps

#### PostCSS Configuration

- **Changes:**
  - Tailwind package is now a dedicated `@tailwindcss/postcss` package
  - Imports and vendor prefixing now handled automatically
  - Remove `postcss-import` and `autoprefixer`

**Before (v3):**
```javascript
export default {
  plugins: {
    "postcss-import": {},      // Remove
    tailwindcss: {},            // Remove
    autoprefixer: {},           // Remove
  },
};
```

**After (v4):**
```javascript
export default {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};
```

#### Vite Configuration

- Migrate to dedicated Tailwind Vite plugin

**Example Vite Config:**
```typescript
import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [tailwindcss()],
});
```

#### CLI Usage

- Tailwind CLI now in `@tailwindcss/cli` package

**Update CLI Commands:**
```terminal
# Old
npx tailwindcss -i input.css -o output.css

# New
npx @tailwindcss/cli -i input.css -o output.css
```

## Breaking Changes

### Browser Requirements

- **Important!** v4.0 designed for modern browsers
- Targets:
  - Safari 16.4
  - Chrome 111
  - Firefox 128
- Uses modern CSS features like `@property` and `color-mix()`

### Tailwind Directives

- Replace `@tailwind` directives with standard CSS import

**Before:**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

**After:**
```css
@import "tailwindcss";
```

### Removed Utilities

- Removed deprecated utilities from v3

**Deprecated Utilities Mapping:**
- `bg-opacity-*` → `bg-black/50`
- `text-opacity-*` → `text-black/50`
- `border-opacity-*` → `border-black/50`
- `divide-opacity-*` → `divide-black/50`
- `ring-opacity-*` → `ring-black/50`
- `placeholder-opacity-*` → `placeholder-black/50`
- `flex-shrink-*` → `shrink-*`
- `flex-grow-*` → `grow-*`
- `text-ellipsis` → `text-ellipsis`
- `box-decoration-slice` → `box-decoration-slice`
- `box-decoration-clone` → `box-decoration-clone`

### Renamed Utilities

**Utility Renaming:**
- `shadow-sm` → `shadow-xs`
- `shadow` → `shadow-sm`
- `drop-shadow-sm` → `drop-shadow-xs`
- `drop-shadow` → `drop-shadow-sm`
- `blur-sm` → `blur-xs`
- `blur` → `blur-sm`
- `backdrop-blur-sm` → `backdrop-blur-xs`
- `backdrop-blur` → `backdrop-blur-sm`
- `rounded-sm` → `rounded-xs`
- `rounded` → `rounded-sm`
- `outline-none` → `outline-hidden`
- `ring` → `ring-3`

**Why Renamed:**
- Ensures every utility has a named value (no more bare utilities like `shadow` or `blur`)
- Bare versions (e.g., `shadow`, `blur`, `rounded`) still work for backward compatibility
- But `<utility>-sm` utilities will look different unless updated to `<utility>-xs` versions

**Migration Example:**
```html
<!-- v3 -->
<input class="shadow-sm" />

<!-- v4 -->
<input class="shadow-xs" />

<!-- v3 -->
<input class="shadow" />

<!-- v4 -->
<input class="shadow-sm" />
```

**Outline Utility Changes:**
- `outline` now sets `outline-width: 1px` by default
- All `outline-<number>` utilities default to `outline-style: solid`
- No need to combine with `outline` class anymore

**Example:**
```html
<!-- Before -->
<input class="outline outline-2" />

<!-- After -->
<input class="outline-2" />
```

### Gradient Variant Behavior

- In v3, overriding gradients with variants would reset the entire gradient
- In v4, gradient values are preserved (consistent with other utilities)

**Migration Example:**
```html
<!-- v3: to-yellow-400 became transparent in dark mode -->
<div class="bg-linear-to-r from-red-500 to-yellow-400 dark:from-blue-500">

<!-- v4: Need explicit via-none to unset three-stop gradients -->
<div class="bg-linear-to-r from-red-500 via-orange-400 to-yellow-400 dark:via-none dark:from-blue-500 dark:to-teal-400">
```

### Space-Between Selector

- Changed for performance on large pages
- Now uses `:not(:last-child)` with `margin-bottom` instead of adjacent sibling selector

**Before:**
```css
.space-y-4 > :not([hidden]) ~ :not([hidden]) {
  margin-top: 1rem;
}
```

**After:**
```css
.space-y-4 > :not(:last-child) {
  margin-bottom: 1rem;
}
```

**Recommendation:** Migrate to `flex` or `grid` with `gap`:
```html
<!-- Before -->
<div class="space-y-4 p-4">

<!-- After -->
<div class="flex flex-col gap-4 p-4">
```

### Container Configuration

- Remove `center` and `padding` options from config
- Use `@utility` directive for customization

**Example:**
```css
@utility container {
  margin-inline: auto;
  padding-inline: 2rem;
}
```

### Default Border Color

- Changed from `gray-200` to `currentColor`
- Always specify color explicitly:

```html
<div class="border border-gray-200 px-2 py-3">
```

**Preserve v3 Behavior:**
```css
@layer base {
  *,
  ::after,
  ::before,
  ::backdrop,
  ::file-selector-button {
    border-color: var(--color-gray-200, currentColor);
  }
}
```

### Default Ring Width and Color

- Width changed from 3px to 1px
- Color changed from `blue-500` to `currentColor`

**Migration:**
```html
<!-- Before -->
<button class="focus:ring">

<!-- After -->
<button class="focus:ring-3 focus:ring-blue-500">
```

**Preserve v3 Behavior:**
```css
@theme {
  --default-ring-width: 3px;
  --default-ring-color: var(--color-blue-500);
}
```
*Note: These variables are for compatibility only, not idiomatic v4 usage*

### Preflight Changes

**Placeholder Color:**
- Changed from `gray-400` to current text color at 50% opacity

**Preserve v3 Behavior:**
```css
@layer base {
  input::placeholder,
  textarea::placeholder {
    color: var(--color-gray-400);
  }
}
```

**Button Cursor:**
- Changed from `pointer` to `default`

**Preserve v3 Behavior:**
```css
@layer base {
  button:not(:disabled),
  [role="button"]:not(:disabled) {
    cursor: pointer;
  }
}
```

**Dialog Margins:**
- Now reset to match other elements

**Preserve v3 Behavior:**
```css
@layer base {
  dialog {
    margin: auto;
  }
}
```

**Hidden Attribute:**
- Display classes no longer override `hidden` attribute
- Remove attribute to make element visible
- Does not apply to `hidden="until-found"`

### Custom Utilities

- Replace `@layer utilities` and `@layer components` with `@utility` directive
- Custom utilities now support variants automatically
- Sorted by property count (fewer properties = lower specificity)

**Migration:**
```css
/* Before */
@layer utilities {
  .tab-4 {
    tab-size: 4;
  }
}

/* After */
@utility tab-4 {
  tab-size: 4;
}
```

**Component Utilities:**
```css
/* Before */
@layer components {
  .btn {
    border-radius: 0.5rem;
    padding: 0.5rem 1rem;
    background-color: ButtonFace;
  }
}

/* After */
@utility btn {
  border-radius: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: ButtonFace;
}
```

### Variant Stacking Order

- Changed from right-to-left to left-to-right (matches CSS syntax)

**Migration:**
```html
<!-- Before -->
<ul class="py-4 first:*:pt-0 last:*:pb-0">

<!-- After -->
<ul class="py-4 *:first:pt-0 *:last:pb-0">
```

*Note: Mostly affects `*` (direct child) and typography plugin variants*

### Hover Styles on Mobile

- `hover` variant now only applies when primary input supports hover
- Uses `@media (hover: hover)`

**Override for Old Behavior:**
```css
@custom-variant hover (&:hover);
```

**Recommendation:** Treat hover as enhancement, not requirement

### Transitioning Outline Color

- `transition` and `transition-color` now include `outline-color`

**Migration:**
```html
<!-- Before (color would transition from default) -->
<button class="transition hover:outline-2 hover:outline-cyan-500"></button>

<!-- After (set color unconditionally) -->
<button class="outline-cyan-500 transition hover:outline-2"></button>
```

## Using Variables and Prefixes

### Variable Syntax

**Before:**
```html
<div class="bg-(--brand-color)"></div>
```

**After:**
```html
<div class="bg-(--brand-color)"></div>
```

### Prefix Usage

- Prefixes now look like variants (always at beginning of class name)

**Example:**
```html
<div class="tw:flex tw:bg-red-500 tw:hover:bg-red-600">
  <!-- ... -->
</div>
```

**Configuration:**

When using a prefix, configure theme variables without the prefix:

```css
@import "tailwindcss" prefix(tw);

@theme {
  --font-display: "Satoshi", "sans-serif";
  --breakpoint-3xl: 120rem;
  --color-avocado-100: oklch(0.99 0 0);
  --color-avocado-200: oklch(0.98 0.04 113.22);
  --color-avocado-300: oklch(0.94 0.11 115.03);
  /* ... */
}
```

Generated CSS variables will include the prefix to avoid conflicts:

```css
:root {
  --tw-font-display: "Satoshi", "sans-serif";
  --tw-breakpoint-3xl: 120rem;
  --tw-color-avocado-100: oklch(0.99 0 0);
  --tw-color-avocado-200: oklch(0.98 0.04 113.22);
  --tw-color-avocado-300: oklch(0.94 0.11 115.03);
  /* ... */
}
```

## Advanced Topics

### Using theme() Function

- Prefer CSS variables over `theme()` when possible
- For media queries, use new CSS variable syntax

**Migration:**
```css
/* Before */
.my-class {
  background-color: theme(colors.red.500);
}
@media (width >= theme(screens.xl)) {
  /* ... */
}

/* After - prefer CSS variables */
.my-class {
  background-color: var(--color-red-500);
}
@media (width >= theme(--breakpoint-xl)) {
  /* ... */
}
```

### JavaScript Config Files

- No longer detected automatically
- Use `@config` directive to load explicitly

**Example:**
```css
@config "../../tailwind.config.js";
```

**Unsupported Options:**
- `corePlugins`
- `safelist` (use `@source inline()` instead)
- `separator`

### Theme Values in JavaScript

- `resolveConfig()` function removed
- Use CSS variables directly (better bundle size)

**Motion Library Example:**
```jsx
<motion.div animate={{ backgroundColor: "var(--color-blue-500)" }} />
```

**Get Computed Value:**
```javascript
let styles = getComputedStyle(document.documentElement);
let shadow = styles.getPropertyValue("--shadow-xl");
```

### Vue/Svelte/CSS Modules

- Separate stylesheets don't have access to theme variables
- Use `@reference` to import without duplicating CSS

**Vue Example:**
```vue
<template>
  <h1>Hello world!</h1>
</template>
<style>
  @reference "../../app.css";
  h1 {
    @apply text-2xl font-bold text-red-500;
  }
</style>
```

**Alternative (Better Performance):**
```vue
<style>
  h1 {
    color: var(--text-red-500);
  }
</style>
```

### Disabling Core Plugins

- `corePlugins` option no longer supported
- No alternative in v4

## Compatibility and Migration

- **Important!** Review all changes carefully
- Use upgrade tool when possible
- Test thoroughly after migration
- Consider preserving v3 behavior with custom CSS if needed

## Unsupported in v4

### CSS Preprocessors

**Important!** Tailwind CSS v4.0 is not designed to be used with CSS preprocessors like Sass, Less, or Stylus

**Rationale:**
- Think of Tailwind CSS itself as your preprocessor
- You shouldn't use Tailwind with Sass for the same reason you wouldn't use Sass with Stylus
- Not possible to use preprocessors for stylesheets or `<style>` blocks in Vue, Svelte, Astro, etc.

### Other Unsupported Features

- `corePlugins` option (no alternative)
- `resolveConfig()` function (use CSS variables or `getComputedStyle()`)
- Automatic JavaScript config detection (use `@config` directive)