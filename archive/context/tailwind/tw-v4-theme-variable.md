# Tailwind CSS v4 Theme Variables

**Using utility classes as an API for your design tokens**

## Overview

- Tailwind is a framework for building custom designs requiring different typography, colors, shadows, breakpoints
- Low-level design decisions are called **design tokens**, stored as **theme variables** in Tailwind projects

### What are Theme Variables?

- Special CSS variables defined using `@theme` directive
- Influence which utility classes exist in your project
- Example: Adding a new color

```css
@import "tailwindcss";
@theme {
  --color-mint-500: oklch(0.72 0.11 178);
}
```

**Usage:**

```html
<div class="bg-mint-500">
  <!-- Uses the custom color -->
</div>
```

- Tailwind generates regular CSS variables for use in arbitrary values or inline styles

```html
<div style="background-color: var(--color-mint-500)">
  <!-- Direct CSS variable usage -->
</div>
```

### Why @theme instead of :root?

- Theme variables aren't just CSS variables—they instruct Tailwind to create new utility classes
- Special syntax makes defining theme variables explicit
- Must be defined top-level, not nested under selectors or media queries
- **Use `@theme`** when design token should map to utility class
- **Use `:root`** for regular CSS variables without corresponding utility classes

## Relationship to Utility Classes

- Static utilities (`flex`, `object-cover`) are always the same
- Dynamic utilities are driven by theme variables

**Example with fonts:**

```css
@theme {
  --font-sans: ui-sans-serif, system-ui, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
  --font-serif: ui-serif, Georgia, Cambria, "Times New Roman", Times, serif;
  --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
}
```

- `font-sans`, `font-serif`, `font-mono` utilities exist because of these theme variables
- Adding `--font-poppins` creates `font-poppins` utility

```css
@import "tailwindcss";
@theme {
  --font-poppins: Poppins, sans-serif;
}
```

```html
<h1 class="font-poppins">This headline will use Poppins.</h1>
```

- Name theme variables whatever you want within namespaces
- Corresponding utility with same name becomes available

## Relationship to Variants

- Some theme variables define variants instead of utilities
- Example: `--breakpoint-*` namespace determines responsive breakpoint variants

```css
@import "tailwindcss";
@theme {
  --breakpoint-3xl: 120rem;
}
```

```html
<div class="3xl:grid-cols-6 grid grid-cols-2 md:grid-cols-4">
  <!-- Triggers at 120rem viewport -->
</div>
```

## Theme Variable Namespaces

- Theme variables are defined in namespaces
- Each namespace corresponds to one or more utility class or variant APIs
- Defining new theme variables makes new corresponding utilities/variants available

**Namespace to Utility Mapping:**

- `--color-*` - Color utilities like `bg-red-500`, `text-sky-300`
- `--font-*` - Font family utilities like `font-sans`
- `--text-*` - Font size utilities like `text-xl`
- `--font-weight-*` - Font weight utilities like `font-bold`
- `--tracking-*` - Letter spacing utilities like `tracking-wide`
- `--leading-*` - Line height utilities like `leading-tight`
- `--breakpoint-*` - Responsive breakpoint variants like `sm:*`
- `--container-*` - Container query variants like `@sm:*` and size utilities like `max-w-md`
- `--spacing-*` - Spacing and sizing utilities like `px-4`, `max-h-16`
- `--radius-*` - Border radius utilities like `rounded-sm`
- `--shadow-*` - Box shadow utilities like `shadow-md`
- `--inset-shadow-*` - Inset box shadow utilities like `inset-shadow-xs`
- `--drop-shadow-*` - Drop shadow filter utilities like `drop-shadow-md`
- `--blur-*` - Blur filter utilities like `blur-md`
- `--perspective-*` - Perspective utilities like `perspective-near`
- `--aspect-*` - Aspect ratio utilities like `aspect-video`
- `--ease-*` - Transition timing function utilities like `ease-out`
- `--animate-*` - Animation utilities like `animate-spin`

## Default Theme Variables

- Importing `tailwindcss` includes default theme variables

**What you're importing:**

```css
@layer theme, base, components, utilities;
@import "./theme.css" layer(theme);
@import "./preflight.css" layer(base);
@import "./utilities.css" layer(base);
```

- `theme.css` includes default color palette, type scale, shadows, fonts
- Utilities like `bg-red-200`, `font-serif`, `shadow-sm` exist because they're driven by default theme
- Not hardcoded like `flex-col` or `pointer-events-none`

## Customizing Your Theme

- Default theme variables are general purpose but just a starting point
- Common to customize colors, fonts, shadows

### Extending the Default Theme

```css
@import "tailwindcss";
@theme {
  --font-script: Great Vibes, cursive;
}
```

- Makes `font-script` utility available like default `font-sans` or `font-mono`

```html
<p class="font-script">This will use the Great Vibes font family.</p>
```

### Overriding the Default Theme

**Single variable override:**

```css
@import "tailwindcss";
@theme {
  --breakpoint-sm: 30rem;
}
```

- `sm:*` variant now triggers at `30rem` instead of default `40rem`

**Complete namespace override:**

```css
@import "tailwindcss";
@theme {
  --color-*: initial;
  --color-white: #fff;
  --color-purple: #3f3cbb;
  --color-midnight: #121063;
  --color-tahiti: #3ab7bf;
  --color-bermuda: #78dcca;
}
```

- Removes all default color utilities (like `bg-red-500`)
- Only custom values available (like `bg-midnight`)

### Using a Custom Theme

**Disable default theme completely:**

```css
@import "tailwindcss";
@theme {
  --*: initial;
  --spacing: 4px;
  --font-body: Inter, sans-serif;
  --color-lagoon: oklch(0.72 0.11 221.19);
  --color-coral: oklch(0.74 0.17 40.24);
  --color-driftwood: oklch(0.79 0.06 74.59);
  --color-tide: oklch(0.49 0.08 205.88);
  --color-dusk: oklch(0.82 0.15 72.09);
}
```

- No default theme variable utilities available
- Only custom theme variable utilities (like `font-body`, `text-dusk`)

## Defining Animation Keyframes

- Define `@keyframes` rules for `--animate-*` theme variables within `@theme`

```css
@import "tailwindcss";
@theme {
  --animate-fade-in-scale: fade-in-scale 0.3s ease-out;
  @keyframes fade-in-scale {
    0% {
      opacity: 0;
      transform: scale(0.95);
    }
    100% {
      opacity: 1;
      transform: scale(1);
    }
  }
}
```

*If you want custom `@keyframes` rules always included without `--animate-*` theme variable, define them outside `@theme`*

## Referencing Other Variables

**Use the `inline` option when referencing other variables:**

```css
@import "tailwindcss";
@theme inline {
  --font-sans: var(--font-inter);
}
```

- Utility class uses theme variable value instead of referencing the theme variable

```css
.font-sans {
  font-family: var(--font-inter);
}
```

**Important!** Without `inline`, utility classes might resolve to unexpected values due to CSS variable resolution order

**Example of the problem:**

```html
<div id="parent" style="--font-sans: var(--font-inter, sans-serif);">
  <div id="child" style="--font-inter: Inter; font-family: var(--font-sans);">
    This text will use the sans-serif font, not Inter.
  </div>
</div>
```

- `var(--font-sans)` resolves where `--font-sans` is defined (`#parent`)
- `--font-inter` has no value there since it's defined on `#child`

## Generating All CSS Variables

**By default:** Only used CSS variables are generated in final CSS output

**To always generate all CSS variables:**

```css
@import "tailwindcss";
@theme static {
  --color-primary: var(--color-red-500);
  --color-secondary: var(--color-blue-500);
}
```

## Sharing Across Projects

- Theme variables are defined in CSS
- Share by creating separate CSS file to import in each project

**Example shared theme:**

```css
/* ./packages/brand/theme.css */
@theme {
  --*: initial;
  --spacing: 4px;
  --font-body: Inter, sans-serif;
  --color-lagoon: oklch(0.72 0.11 221.19);
  --color-coral: oklch(0.74 0.17 40.24);
  --color-driftwood: oklch(0.79 0.06 74.59);
  --color-tide: oklch(0.49 0.08 205.88);
  --color-dusk: oklch(0.82 0.15 72.09);
}
```

**Import in other projects:**

```css
/* ./packages/admin/app.css */
@import "tailwindcss";
@import "../brand/theme.css";
```

- Put shared theme variables in own package in monorepo setups
- Can publish to NPM and import like any third-party CSS files

## Using Your Theme Variables

- All theme variables become regular CSS variables when compiled

```css
:root {
  --font-sans: ui-sans-serif, system-ui, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
  --font-serif: ui-serif, Georgia, Cambria, "Times New Roman", Times, serif;
  --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  --color-red-50: oklch(0.971 0.013 17.38);
  --color-red-100: oklch(0.936 0.032 17.717);
  --color-red-200: oklch(0.885 0.062 18.334);
  /* ... */
}
```

### With Custom CSS

```css
@import "tailwindcss";
@layer components {
  .typography {
    p {
      font-size: var(--text-base);
      color: var(--color-gray-700);
    }
    h1 {
      font-size: var(--text-2xl--line-height);
      font-weight: var(--font-weight-semibold);
      color: var(--color-gray-950);
    }
    h2 {
      font-size: var(--text-xl);
      font-weight: var(--font-weight-semibold);
      color: var(--color-gray-950);
    }
  }
}
```

*Useful when styling HTML you don't control, like Markdown content from database or API*

### With Arbitrary Values

```html
<div class="relative rounded-xl">
  <div class="absolute inset-px rounded-[calc(var(--radius-xl)-1px)]">
    <!-- ... -->
  </div>
  <!-- ... -->
</div>
```

- Subtracting `1px` from `--radius-xl` value on nested inset element for concentric border radius

### Referencing in JavaScript

**Direct usage with CSS variables:**

```jsx
<motion.div animate={{ backgroundColor: "var(--color-blue-500)" }} />
```

**Getting resolved value:**

```js
let styles = getComputedStyle(document.documentElement);
let shadow = styles.getPropertyValue("--shadow-xl");
```


