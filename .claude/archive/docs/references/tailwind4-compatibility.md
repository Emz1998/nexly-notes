# Tailwind CSS v4.0 Compatibility Guide

## Browser Support

**Minimum Browser Versions:**
1. Chrome 111 (March 2023)
2. Safari 16.4 (March 2023)
3. Firefox 128 (July 2024)

**Important!** Tailwind includes support for bleeding-edge platform features like:
- `field-sizing: content`
- `@starting-style`
- `text-wrap: balance`

**Recommendations:**
- Check browser compatibility before using modern features
- Use [Can I Use](https://caniuse.com) database for feature support verification

## Preprocessor Compatibility

### Why Not Preprocessors?

**Key Points:**
- Tailwind CSS v4.0 is a full-featured CSS build tool
- **Not designed to work with Sass, Less, or Stylus**
- Tailwind itself acts as a preprocessor

### Built-in Preprocessor Features

1. **Import Handling**
   - Automatically bundles CSS files with `@import`
   - No separate preprocessing tool required

   ```css
   @import "tailwindcss";
   @import "./typography.css";
   ```

2. **Native CSS Variables**
   - Modern browsers support CSS variables natively
   - Tailwind relies heavily on CSS variables

   ```css
   .typography {
     font-size: var(--text-base);
     color: var(--color-gray-700);
   }
   ```

3. **CSS Nesting**
   - Uses Lightning CSS for nested CSS processing
   - Automatically flattens nested CSS for browser compatibility

   ```css
   .typography {
     p { font-size: var(--text-base); }
     img { border-radius: var(--radius-lg); }
   }
   ```

4. **Color and Math Functions**
   - Recommends using predefined color palettes
   - Supports modern CSS features like `color-mix()`
   - Native browser support for `min()`, `max()`, and `round()` functions

## CSS Modules Compatibility

### Compatibility Status
- Compatible with CSS modules
- **Not recommended to use together if avoidable**

### Challenges with CSS Modules
1. **Scoping is Less Relevant**
   - Tailwind utility classes are inherently scoped
   - No unexpected side effects

2. **Performance Concerns**
   - Build tools process each CSS module separately
   - Increases build time and complexity

### Recommended Approaches

1. **Styling with Utility Classes**
   ```html
   <button class="bg-indigo-500 hover:bg-indigo-600">
     Button Text
   </button>
   ```

2. **Using CSS Variables**
   ```css
   button {
     background: var(--color-blue-500);
   }
   ```

## Framework-Specific Considerations

### Vue, Svelte, and Astro

**Recommendations:**
- Avoid `<style>` blocks in components
- Style directly with utility classes
- If using `<style>` blocks, import global styles as reference

**Example:**
```vue
<template>
  <button><slot /></button>
</template>
<style scoped>
  @reference "../app.css";
  button {
    @apply bg-blue-500;
  }
</style>
```

**Important!** Prioritize utility classes and CSS variables over `@apply`.