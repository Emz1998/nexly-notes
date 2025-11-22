# Tailwind CSS v4 Functions and Directives

**Reference for custom functions and directives that Tailwind exposes to your CSS**

## Directives

**Custom Tailwind-specific at-rules for special functionality in Tailwind CSS projects**

### @import

- Inline imports CSS files including Tailwind itself

```css
@import "tailwindcss";
```

### @theme

- Defines project's custom design tokens: fonts, colors, breakpoints

```css
@theme {
  --font-display: "Satoshi", "sans-serif";
  --breakpoint-3xl: 120rem;
  --color-avocado-100: oklch(0.99 0 0);
  --color-avocado-200: oklch(0.98 0.04 113.22);
  --color-avocado-300: oklch(0.94 0.11 115.03);
  --color-avocado-400: oklch(0.92 0.19 114.08);
  --color-avocado-500: oklch(0.84 0.18 117.33);
  --color-avocado-600: oklch(0.53 0.12 118.34);
  --ease-fluid: cubic-bezier(0.3, 0, 0, 1);
  --ease-snappy: cubic-bezier(0.2, 0, 0, 1);
}
```

*Learn more: theme variables documentation*

### @source

- Explicitly specifies source files not picked up by automatic content detection

```css
@source "../node_modules/@my-company/ui-lib";
```

*Learn more: detecting classes in source files documentation*

### @utility

- Adds custom utilities that work with variants like `hover`, `focus`, `lg`

```css
@utility tab-4 {
  tab-size: 4;
}
```

*Learn more: adding custom utilities documentation*

### @variant

- Applies Tailwind variants to styles in CSS

```css
.my-element {
  background: white;
  @variant dark {
    background: black;
  }
}
```

*Learn more: using variants documentation*

### @custom-variant

- Adds custom variants to project

```css
@custom-variant theme-midnight (&:where([data-theme="midnight"] *));
```

- Enables utilities like `theme-midnight:bg-black` and `theme-midnight:text-white`

*Learn more: adding custom variants documentation*

### @apply

- Inlines existing utility classes into custom CSS
- Useful for overriding third-party library styles while using design tokens and HTML syntax

```css
.select2-dropdown {
  @apply rounded-b-lg shadow-md;
}
.select2-search {
  @apply rounded border border-gray-300;
}
.select2-results__group {
  @apply text-lg font-bold text-gray-900;
}
```

### @reference

- Imports theme variables, custom utilities, and variants without duplicating CSS in output
- Required for using `@apply` or `@variant` in Vue/Svelte `<style>` blocks or CSS modules

**With custom stylesheet:**

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

**With default theme:**

```vue
<template>
  <h1>Hello world!</h1>
</template>
<style>
  @reference "tailwindcss";
  h1 {
    @apply text-2xl font-bold text-red-500;
  }
</style>
```

## Functions

**Build-time functions for working with colors and spacing**

### --alpha()

- Adjusts color opacity

**Input:**
```css
.my-element {
  color: --alpha(var(--color-lime-300) / 50%);
}
```

**Compiled:**
```css
.my-element {
  color: color-mix(in oklab, var(--color-lime-300) 50%, transparent);
}
```

### --spacing()

- Generates spacing values based on theme

**Input:**
```css
.my-element {
  margin: --spacing(4);
}
```

**Compiled:**
```css
.my-element {
  margin: calc(var(--spacing) * 4);
}
```

**Useful in arbitrary values with `calc()`:**

```html
<div class="py-[calc(--spacing(4)-1px)]">
  <!-- ... -->
</div>
```

## Compatibility

**Directives and functions for Tailwind CSS v3.x compatibility**

**Important!** `@config` and `@plugin` directives work alongside `@theme`, `@utility`, and other CSS-driven features for incremental migration. CSS definitions merge where possible and take precedence over configs, presets, and plugins.

### @config

- Loads legacy JavaScript-based configuration file

```css
@config "../../tailwind.config.js";
```

**Important!** Not supported in v4.0:
- `corePlugins` option
- `safelist` option
- `separator` option

*To safelist utilities in v4, use `@source inline()`*

### @plugin

- Loads legacy JavaScript-based plugin
- Accepts package name or local path

```css
@plugin "@tailwindcss/typography";
```

### theme()

- Accesses Tailwind theme values using dot notation

```css
.my-element {
  margin: theme(spacing.12);
}
```

**Important!** This function is deprecated. Use CSS theme variables instead.
