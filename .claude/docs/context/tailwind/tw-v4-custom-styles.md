# Adding Custom Styles

Best practices for adding your own custom styles in Tailwind projects.

## Overview

- Tailwind is designed to be extensible and customizable
- This guide covers:
  - Customizing design tokens
  - Breaking out of constraints when necessary
  - Adding custom CSS
  - Extending the framework with plugins

## Customizing Your Theme

**To change color palette, spacing scale, typography scale, or breakpoints:**

- Add customizations using the `@theme` directive in your CSS:

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
  /* ... */
}
```

*Learn more about customizing your theme in the theme variables documentation*

## Using Arbitrary Values

**When to use:**
- When you need to break out of design token constraints for pixel-perfect positioning
- Example: `top: 117px` for precise background image placement

**Square bracket notation:**

```html
<div class="top-[117px]">
  <!-- ... -->
</div>
```

**Benefits:**
- Like inline styles but can combine with interactive modifiers like `hover`
- Can combine with responsive modifiers like `lg:`

```html
<div class="top-[117px] lg:top-[344px]">
  <!-- ... -->
</div>
```

**Works for everything in the framework:**
- Background colors
- Font sizes
- Pseudo-element content
- More

```html
<div class="bg-[#bada55] text-[22px] before:content-['Festivus']">
  <!-- ... -->
</div>
```

**CSS variables as arbitrary values:**

- Use custom property syntax:

```html
<div class="fill-(--my-brand-color) ...">
  <!-- ... -->
</div>
```

- This is shorthand for `fill-(--my-brand-color)` that adds the `var()` function automatically

### Arbitrary Properties

**For CSS properties Tailwind doesn't include out of the box:**

- Use square bracket notation to write completely arbitrary CSS:

```html
<div class="mask-type-luminance">
  <!-- ... -->
</div>
```

**Benefits:**
- Like inline styles but can use modifiers:

```html
<div class="mask-type-luminance hover:mask-type-alpha">
  <!-- ... -->
</div>
```

**Useful for CSS variables that need to change under different conditions:**

```html
<div class="[--scroll-offset:56px] lg:[--scroll-offset:44px]">
  <!-- ... -->
</div>
```

### Arbitrary Variants

**What they are:**
- Like arbitrary values but for on-the-fly selector modification
- Similar to built-in pseudo-class variants like `hover:{utility}` or responsive variants like `md:{utility}`
- Uses square bracket notation directly in HTML

**Example:**

```html
<ul role="list">
  {#each items as item}
  <li class="lg:nth-[-n+3]:hover:underline">{item}</li>
  {/each}
</ul>
```

*Learn more in the arbitrary variants documentation*

### Handling Whitespace

**When arbitrary value needs a space:**
- Use underscore `_` instead
- Tailwind automatically converts it to space at build-time:

```html
<div class="grid grid-cols-[1fr_500px_2fr]">
  <!-- ... -->
</div>
```

**When underscores are common but spaces are invalid:**
- Tailwind preserves the underscore instead of converting to space
- Example in URLs:

```html
<div class="bg-[url('/what_a_rush.png')]">
  <!-- ... -->
</div>
```

**When you need an underscore but it's ambiguous:**
- Escape the underscore with backslash
- Tailwind won't convert it to space:

```html
<div class="before:content-['hello\_world']">
  <!-- ... -->
</div>
```

**For JSX where backslash is stripped:**
- Use `String.raw()` so backslash isn't treated as JavaScript escape character:

```jsx
<div className={String.raw`before:content-['hello\_world']`}>
  <!-- ... -->
</div>
```

### Resolving Ambiguities

**The problem:**
- Many utilities share common namespace but map to different CSS properties
- Example: `text-lg` and `text-black` both share `text-` namespace
  - One is for `font-size`
  - Other is for `color`

**How Tailwind handles it:**
- Generally handles ambiguity automatically based on value passed in:

```html
<!-- Will generate a font-size utility -->
<div class="text-[22px]">...</div>
<!-- Will generate a color utility -->
<div class="text-[#bada55]">...</div>
```

**When it's truly ambiguous (like CSS variables):**

```html
<div class="text-(--my-var)">...</div>
```

**Solution - hint the underlying type:**
- Add CSS data type before the value:

```html
<!-- Will generate a font-size utility -->
<div class="text-(length:--my-var)">...</div>
<!-- Will generate a color utility -->
<div class="text-(--my-var)">...</div>
```

## Using Custom CSS

**Basic approach:**
- Nothing stops you from writing plain CSS when needed:

```css
@import "tailwindcss";
.my-custom-style {
  /* ... */
}
```

### Adding Base Styles

**For page defaults (text color, background color, font family):**
- Easiest option: add classes to `html` or `body` elements:

```html
<!doctype html>
<html lang="en" class="bg-gray-100 font-serif text-gray-900">
  <!-- ... -->
</html>
```

**Benefits:**
- Keeps base styling decisions in markup alongside other styles
- Avoids hiding them in separate file

**For custom default base styles for specific HTML elements:**
- Use `@layer` directive to add to Tailwind's base layer:

```css
@layer base {
  h1 {
    font-size: var(--text-2xl);
  }
  h2 {
    font-size: var(--text-xl);
  }
}
```

### Adding Component Classes

**When to use:**
- For complicated classes you want to add to your project
- That you'd still like to override with utility classes

**Traditional examples:**
- `card`, `btn`, `badge`

**Example:**

```css
@layer components {
  .card {
    background-color: var(--color-white);
    border-radius: var(--radius-lg);
    padding: --spacing(6);
    box-shadow: var(--shadow-xl);
  }
}
```

**Benefits:**
- Can still use utility classes to override when necessary:

```html
<!-- Will look like a card, but with square corners -->
<div class="card rounded-none">
  <!-- ... -->
</div>
```

**Note:**
- Using Tailwind you probably don't need these types of classes as often as you think
- *Read our guide on managing duplication for our recommendations*

**Also good for third-party component styles:**

```css
@layer components {
  .select2-dropdown {
    /* ... */
  }
}
```

### Using Variants

**Apply Tailwind variant within custom CSS:**
- Use `@variant` directive:

```css
/* app.css */
.my-element {
  background: white;
  @variant dark {
    background: black;
  }
}
```

**Compiled output:**

```css
.my-element {
  background: white;
  @media (prefers-color-scheme: dark) {
    background: black;
  }
}
```

**For multiple variants at the same time:**
- Use nesting:

```css
/* app.css */
.my-element {
  background: white;
  @variant dark {
    @variant hover {
      background: black;
    }
  }
}
```

**Compiled output:**

```css
.my-element {
  background: white;
  @media (prefers-color-scheme: dark) {
    &:hover {
      @media (hover: hover) {
        background: black;
      }
    }
  }
}
```

## Adding Custom Utilities

### Simple Utilities

**When to use:**
- For CSS features you'd like to use that Tailwind doesn't include out of the box

**Use `@utility` directive:**

```css
@utility content-auto {
  content-visibility: auto;
}
```

**Usage in HTML:**

```html
<div class="content-auto">
  <!-- ... -->
</div>
```

**Works with variants:**

```html
<div class="hover:content-auto">
  <!-- ... -->
</div>
```

**Note:**
- Custom utilities are automatically inserted into the utilities layer along with built-in utilities

### Complex Utilities

**For utilities more complex than single class name:**
- Use nesting to define the utility:

```css
@utility scrollbar-hidden {
  &::-webkit-scrollbar {
    display: none;
  }
}
```

### Functional Utilities

**Register functional utilities that accept an argument:**

```css
@utility tab-* {
  tab-size: --value(--tab-size-*);
}
```

**Note:**
- The special `--value()` function is used to resolve the utility value

#### Matching Theme Values

**Use `--value(--theme-key-*)` syntax:**
- Resolves utility value against set of theme keys:

```css
@theme {
  --tab-size-2: 2;
  --tab-size-4: 4;
  --tab-size-github: 8;
}
@utility tab-* {
  tab-size: --value(--tab-size-*);
}
```

**Matches utilities like:**
- `tab-2`
- `tab-4`
- `tab-github`

#### Bare Values

**To resolve value as bare value:**
- Use `--value({type})` syntax
- `{type}` is the data type you want to validate the bare value as:

```css
@utility tab-* {
  tab-size: --value(integer);
}
```

**Matches utilities like:**
- `tab-1`
- `tab-76`

**Available bare value data types:**
- `number`
- `integer`
- `ratio`
- `percentage`

#### Literal Values

**To support literal values:**
- Use `--value('literal')` syntax (notice the quotes):

```css
@utility tab-* {
  tab-size: --value("inherit", "initial", "unset");
}
```

**Matches utilities like:**
- `tab-inherit`
- `tab-initial`
- `tab-unset`

#### Arbitrary Values

**To support arbitrary values:**
- Use `--value([{type}])` syntax (notice the square brackets)
- Tells Tailwind which types are supported as arbitrary value:

```css
@utility tab-* {
  tab-size: --value([integer]);
}
```

**Matches utilities like:**
- `tab-[1]`
- `tab-[76]`

**Available arbitrary value data types:**
- `absolute-size`, `angle`, `bg-size`, `color`, `family-name`, `generic-name`, `image`, `integer`, `length`, `line-width`, `number`, `percentage`, `position`, `ratio`, `relative-size`, `url`, `vector`, `*`

#### Supporting Theme, Bare, and Arbitrary Values Together

**All three forms of `--value()` can be used within a rule:**
- Use multiple declarations
- Declarations that fail to resolve will be omitted in output:

```css
@theme {
  --tab-size-github: 8;
}
@utility tab-* {
  tab-size: --value([integer]);
  tab-size: --value(integer);
  tab-size: --value(--tab-size-*);
}
```

**Makes it possible to treat value differently in each case:**
- Example: translating bare integer to percentage:

```css
@utility opacity-* {
  opacity: --value([percentage]);
  opacity: calc(--value(integer) * 1%);
  opacity: --value(--opacity-*);
}
```

**Alternative approach - multiple arguments:**
- `--value()` function can take multiple arguments
- Resolves them left to right if you don't need to treat return value differently:

```css
@theme {
  --tab-size-github: 8;
}
@utility tab-* {
  tab-size: --value(--tab-size-*, integer, [integer]);
}
@utility opacity-* {
  opacity: calc(--value(integer) * 1%);
  opacity: --value(--opacity-*, [percentage]);
}
```

#### Negative Values

**To support negative values:**
- Register separate positive and negative utilities into separate declarations:

```css
@utility inset-* {
  inset: --spacing(--value(integer));
  inset: --value([percentage], [length]);
}
@utility -inset-* {
  inset: --spacing(--value(integer) * -1);
  inset: calc(--value([percentage], [length]) * -1);
}
```

#### Modifiers

**Handled using `--modifier()` function:**
- Works exactly like `--value()` function
- Operates on modifier if present:

```css
@utility text-* {
  font-size: --value(--text-*, [length]);
  line-height: --modifier(--leading-*, [length], [*]);
}
```

**Note:**
- If modifier isn't present, any declaration depending on modifier is not included in output

#### Fractions

**To handle fractions:**
- Rely on CSS ratio data type
- If used with `--value()`, it's a signal to Tailwind to treat value and modifier as single value:

```css
@utility aspect-* {
  aspect-ratio: --value(--aspect-ratio-*, ratio, [ratio]);
}
```

**Matches utilities like:**
- `aspect-square`
- `aspect-3/4`
- `aspect-7/9`

## Adding Custom Variants

**Add custom variants using `@custom-variant` directive:**

```css
@custom-variant theme-midnight {
  &:where([data-theme="midnight"] *) {
    @slot;
  }
}
```

**Usage in HTML:**

```html
<html data-theme="midnight">
  <button class="theme-midnight:bg-black ..."></button>
</html>
```

**Shorthand syntax when nesting isn't required:**

```css
@custom-variant theme-midnight (&:where([data-theme="midnight"] *));
```

**When custom variant has multiple rules:**
- Nest them within each other:

```css
@custom-variant any-hover {
  @media (any-hover: hover) {
    &:hover {
      @slot;
    }
  }
}
```
