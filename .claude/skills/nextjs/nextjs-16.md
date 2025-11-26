# Next.js 16 (Beta)

The early release of Next.js 16 (Beta) is now available, signaling major architectural changes focused on raw performance, refined caching strategies, and tight integration with the latest React features. The most significant changes include Turbopack becoming the default bundler and the React Compiler moving to stable integration.

## Key Highlights in Next.js 16 Beta

- Turbopack (Stable): Now the default bundler, offering 2–5x faster production builds and up to 10x faster Fast Refresh.
- React Compiler Support (Stable): Built-in support for automatic component memoization.
- Enhanced Routing: Faster navigations with layout deduplication and incremental prefetching.
- Improved Caching APIs: New updateTag() for read-your-writes semantics and updated revalidateTag() with required cacheLife profiles.
- React 19.2: Includes new features like View Transitions and useEffectEvent().
- Turbopack File System Caching (Beta): Even faster start-up and compile times on large apps.

## Developer Experience and Configuration

### Turbopack Enhancements

Turbopack has reached stable status for both development and production builds and is now the default bundler for all new Next.js projects.

**Performance Gains** — developers can expect significant speed improvements right away, with no configuration required:

- 2−5× faster production builds.
- Up to 10× faster Fast Refresh.

**Opting Out** — For existing apps with custom webpack setups, you can continue using webpack by explicitly running:

```
next dev --webpack
next build --webpack
```

### Turbopack File System Caching (Beta)

Next.js 16 introduces filesystem caching in development mode to speed up subsequent runs, especially in large projects. This feature stores compiler artifacts on disk between restarts, leading to significantly faster compile times.

To enable filesystem caching, configure your next.config.ts:

```
// next.config.ts
const nextConfig = {
  experimental: {
    turbopackFileSystemCacheForDev: true,
  },
};

export default nextConfig;
```

### React Compiler Support (Stable)

Built-in support for the React Compiler is now stable following its 1.0 release. The compiler automatically memoizes components, effectively reducing unnecessary re-renders without requiring manual code changes.

The reactCompiler configuration option has been promoted to stable, but is not enabled by default. To use it, you must:

1. Install the latest compiler plugin: `npm install babel-plugin-react-compiler@latest`
2. Enable the option in your next.config.ts:

```
// next.config.ts
const nextConfig = {
  reactCompiler: true,
};

export default nextConfig;
```

Note: Enabling the compiler may slightly increase initial compile times, as it relies on Babel.

## New APIs and Project Setup

### Simplified create-next-app

The boilerplate for new projects has been redesigned for a streamlined setup flow with modern defaults:

- Includes the App Router by default.
- Uses a TypeScript-first configuration.
- Integrates Tailwind CSS.
- Includes ESLint.

### Build Adapters API (Alpha)

The Build Adapters API allows deployment platforms and custom build integrations to modify the build process. You can create custom adapters that hook into the build to change configurations or process the final output.

To integrate a custom adapter, specify its path in your next.config.js:

```
// next.config.js
const nextConfig = {
  experimental: {
    adapterPath: require.resolve('./my-adapter.js'),
  },
};

module.exports = nextConfig;
```

## Mandatory Changes and Deprecations

### Enhanced Routing and Navigation

The routing and navigation system has been completely overhauled to make page transitions faster and leaner, requiring no code changes in existing apps.

**Layout Deduplication**: Reduces network transfer size by downloading shared layouts only once when prefetching multiple URLs (e.g., downloading a layout once for 50 product links instead of 50 times).

**Incremental Prefetching**: The prefetch cache is smarter, only fetching parts of the page not already in the cache instead of entire pages. It intelligently cancels requests when links leave the viewport and re-prefetches upon data invalidation.

This trade-off may result in more individual prefetch requests but leads to a much lower total network transfer size overall.

### Partial Pre-Rendering (PPR) and Cache Components

The experimental Partial Pre-Rendering (PPR) flag and configuration options have been removed. PPR functionality is now being integrated into Cache Components.

**Migration**: To opt into the new PPR model in Next.js 16, use the experimental.cacheComponents configuration option.

**Warning**: If your application heavily relies on the old experimental.ppr = true configuration, it is recommended to stay on your current Next.js Canary version until a dedicated migration guide for Cache Components is released.

### Improved Caching APIs

Next.js 16 refines its caching APIs to give developers more explicit control over cache invalidation and revalidation behavior.

#### 1. revalidateTag() (Updated)

This function now requires a cacheLife profile as a second argument to enable Stale-While-Revalidate (SWR) behavior. It is designed for invalidating content that can tolerate eventual consistency, immediately serving cached data while a revalidation request runs in the background.

- `revalidateTag('tag', 'max')`: Recommended for most cases; enables SWR for long-lived content.
- `revalidateTag('tag', 'hours')`: Uses a built-in profile for hourly revalidation.
- `revalidateTag('tag', { revalidate: 3600 })`: Uses a custom inline object defining the revalidation time in seconds.

**Migration**: You must add the second cacheLife argument to all existing calls, or switch to updateTag() for interactive content. The single-argument form (revalidateTag('tag')) is now deprecated.

#### 2. updateTag() (New, Server Actions Only)

This new API provides read-your-writes semantics and is only available within Server Actions. It simultaneously expires and immediately refreshes cached data within the same request, ensuring the user sees their changes instantly upon form submission or settings update.

```
'use server';
import { updateTag } from 'next/cache';

export async function updateUserProfile(userId: string, profile: Profile) {
  // ...update logic...
  updateTag(`user-${userId}`); // Expire and refresh immediately
}
```

#### 3. refresh() (New, Server Actions Only)

This Server Actions-only API is for refreshing uncached data only — it does not affect the cache. It complements the client-side router.refresh() by allowing developers to refresh dynamic data (like notification counts or status indicators) displayed elsewhere on the page after a Server Action, keeping the cached page shell fast.

## React 19.2 and Canary Features

The App Router now uses the latest React Canary release, integrating features from the new React 19.2:

- View Transitions: Allows animating elements that update inside a Transition or navigation.
- useEffectEvent: Extracts non-reactive logic from Effects into reusable Effect Event functions.
- Activity: Renders "background activity" by hiding UI with display: none while maintaining state and cleaning up Effects.

## Breaking Changes and Other Updates

Next.js 16 introduces several breaking changes, version requirement bumps, removals of deprecated features, and changes to default behaviors that developers must address when migrating.

### Mandatory Version Updates

Next.js 16 requires developers to update their minimum supported software versions:

- Node.js: The minimum version is now 20.9.0 (LTS). Node.js 18 is no longer supported.
- TypeScript: The minimum version is now 5.1.0.
- Browsers: Minimum supported versions are Chrome 111+, Edge 111+, Firefox 111+, and Safari 16.4+.

### Breaking Changes and Removals

Several previously deprecated features have been permanently removed, and access to key APIs has changed:

#### API Access Must Be Asynchronous

Synchronous access to several Next.js data-fetching and cache APIs is now banned; you must use await:

- params, searchParams props access: `await params`, `await searchParams`.
- cookies(), headers(), draftMode() access: `await cookies()`, `await headers()`, `await draftMode()`.

#### Removed Features

- AMP Support (all APIs and configs): No replacement; the feature has been retired.
- next lint command: Use Biome or the ESLint CLI directly. (next build no longer runs linting.)
- Runtime Configs (serverRuntimeConfig, publicRuntimeConfig): Use environment variables (.env files) instead.
- Partial Pre-Rendering (PPR) Flags (experimental.ppr, export const experimental_ppr): PPR is evolving into the Cache Components model; opt-in using experimental.cacheComponents.
- scroll-behavior: smooth default: Must opt back in by adding data-scroll-behavior="smooth" to the HTML document.
- unstable_rootParams(): An alternative API is planned for a future minor release.

#### Changed Default Behaviors

Several defaults have been updated to align with modern performance and security standards:

**Behavior Changes**

- Default Bundler: Turbopack is now the default. Opt out with next build --webpack.
- Parallel Routes: All parallel route slots now require an explicit default.js file. Builds will fail if this file is missing.
- revalidateTag() Signature: The function now requires a cacheLife profile as the second argument to enable SWR behavior.

**Image Component Security and Caching**

The defaults for the next/image component have been tightened and optimized:

- images.minimumCacheTTL: 4 hours (14400s) (was 60s). Reduces revalidation cost for images missing cache-control headers.
- images.maximumRedirects: 3 redirects (was unlimited). Improves security; can be adjusted or set to 0 to disable.
- images.qualities: [75] (was [1..100]). Improves consistency; the quality prop is now coerced to the closest value in the configured array.
- Local IP Optimization: Blocked by default. New security restriction (images.dangerouslyAllowLocalIP must be set to true for private networks).
- images.imageSizes: Removed 16 from default sizes. Reduces the size of the generated srcset and API variations.

### Deprecations

These features are deprecated in Next.js 16 and will be removed in a future major version:

- middleware.ts filename: Developers should rename this file to proxy.ts to clarify its role in network boundary and routing.
- next/legacy/image component: Use next/image instead.
- images.domains config: Use images.remotePatterns instead for a more secure restriction of remote image sources.
- revalidateTag() single argument: Replace with revalidateTag(tag, profile) for SWR, or updateTag(tag) in Server Actions for read-your-writes.
