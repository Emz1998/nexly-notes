# Tailwind v4 - Detecting Classes in Source Files

## Overview

**How Tailwind Works:**
- Scans your project for utility classes
- Generates CSS based on classes you've actually used
- Keeps CSS as small as possible
- Enables features like arbitrary values

## How Classes Are Detected

**Important!** Tailwind treats all source files as plain text and doesn't parse your files as code

**Detection Method:**
- Looks for tokens that could be classes based on expected characters in class names
- Tries to generate CSS for all tokens
- Throws away tokens that don't map to known utility classes

**Example:**

```jsx
export function Button({ color, children }) {
  const colors = {
    black: "bg-black text-white",
    blue: "bg-blue-500 text-white",
    white: "bg-white text-black",
  };
  return (
    <button className={`${colors[color]} rounded-full px-2 py-1.5 font-sans text-sm/6 font-medium shadow`}>
      {children}
    </button>
  );
}
```

## Dynamic Class Names

**Important!** Tailwind has no way of understanding string concatenation or interpolation

### Don't Construct Class Names Dynamically

**Bad Example:**

```html
<div class="text-{{ error ? 'red' : 'green' }}-600"></div>
```

*The strings `text-red-600` and `text-green-600` do not exist, so Tailwind will not generate those classes*

### Always Use Complete Class Names

**Good Example:**

```html
<div class="{{ error ? 'text-red-600' : 'text-green-600' }}"></div>
```

### Don't Use Props to Build Class Names Dynamically

**Bad Example:**

```jsx
function Button({ color, children }) {
  return <button className={`bg-${color}-600 hover:bg-${color}-500 ...`}>{children}</button>;
}
```

### Always Map Props to Static Class Names

**Good Example:**

```jsx
function Button({ color, children }) {
  const colorVariants = {
    blue: "bg-blue-600 hover:bg-blue-500",
    red: "bg-red-600 hover:bg-red-500",
  };
  return <button className={`${colorVariants[color]} ...`}>{children}</button>;
}
```

**Additional Benefits:**
- Map different prop values to different color shades
- Example with multiple variants:

```jsx
function Button({ color, children }) {
  const colorVariants = {
    blue: "bg-blue-600 hover:bg-blue-500 text-white",
    red: "bg-red-500 hover:bg-red-400 text-white",
    yellow: "bg-yellow-300 hover:bg-yellow-400 text-black",
  };
  return <button className={`${colorVariants[color]} ...`}>{children}</button>;
}
```

**Important!** As long as you always use complete class names in your code, Tailwind will generate all of your CSS perfectly every time

## Which Files Are Scanned

**Tailwind scans every file in your project except:**
- Files in `.gitignore`
- Files in `node_modules` directory
- Binary files (images, videos, zip files)
- CSS files
- Common package manager lock files

*If you need to scan files that Tailwind ignores by default, you can explicitly register those sources*

## Source Configuration

### Explicitly Registering Sources

**Use `@source` to register source paths relative to the stylesheet:**

```css
@import "tailwindcss";
@source "../node_modules/@acmecorp/ui-lib";
```

*Especially useful for scanning external libraries built with Tailwind, since dependencies are usually in `.gitignore`*

### Setting Your Base Path

**Use `source()` function to set base path explicitly:**

```css
@import "tailwindcss" source("../src");
```

*Useful for monorepos where build commands run from the root instead of each project's root*

### Ignoring Specific Paths

**Use `@source not` to ignore specific paths:**

```css
@import "tailwindcss";
@source not "../src/components/legacy";
```

*Useful for large directories that don't use Tailwind classes (legacy components or third-party libraries)*

### Disabling Automatic Detection

**Use `source(none)` to disable automatic source detection:**

```css
@import "tailwindcss" source(none);
@source "../admin";
@source "../shared";
```

*Useful for projects with multiple Tailwind stylesheets where each should only include the classes it needs*

## Safelisting

### Safelisting Specific Utilities

**Use `@source inline()` to force generation of specific class names:**

```css
@import "tailwindcss";
@source inline("underline");
```

**Generated CSS:**

```css
.underline {
  text-decoration-line: underline;
}
```

### Safelisting Variants

**Add variants using `{hover:,focus:,}` syntax:**

```css
@import "tailwindcss";
@source inline("{hover:,focus:,}underline");
```

**Generated CSS:**

```css
.underline {
  text-decoration-line: underline;
}
@media (hover: hover) {
  .hover\:underline:hover {
    text-decoration-line: underline;
  }
}
@media (focus: focus) {
  .focus\:underline:focus {
    text-decoration-line: underline;
  }
}
```

### Safelisting with Ranges

**Use brace expansion to generate multiple classes at once:**

```css
@import "tailwindcss";
@source inline("{hover:,}bg-red-{50,{100..900..100},950}");
```

**Generated CSS:**

```css
.bg-red-50 {
  background-color: var(--color-red-50);
}
.bg-red-100 {
  background-color: var(--color-red-100);
}
.bg-red-200 {
  background-color: var(--color-red-200);
}
/* ... */
.bg-red-800 {
  background-color: var(--color-red-800);
}
.bg-red-900 {
  background-color: var(--color-red-900);
}
.bg-red-950 {
  background-color: var(--color-red-950);
}
@media (hover: hover) {
  .hover\:bg-red-50:hover {
    background-color: var(--color-red-50);
  }
  /* ... */
  .hover\:bg-red-950:hover {
    background-color: var(--color-red-950);
  }
}
```

*Generates red background colors from 100 to 900 in increments of 100, plus first and last shades (50 and 950), with hover variants*

### Explicitly Excluding Classes

**Use `@source not inline()` to prevent specific classes from being generated:**

```css
@import "tailwindcss";
@source not inline("{hover:,focus:,}bg-red-{50,{100..900..100},950}");
```

*Explicitly excludes red background utilities and their hover and focus variants from being generated*