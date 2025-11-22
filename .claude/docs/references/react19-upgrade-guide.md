# React 19 Upgrade Guide

*April 25, 2024 by Ricky Hanlon*

**Important!** Upgrade to React 18.3 first before upgrading to React 19 to identify issues early.

## Overview

- React 19 includes breaking changes but most apps should not be affected
- React 18.3 includes warnings for deprecated APIs needed for React 19
- This guide covers installation, codemods, breaking changes, deprecations, notable changes, TypeScript changes, and changelog

**Upgrade Steps:**
1. Install React 19
2. Run codemods
3. Address breaking changes
4. Review deprecations
5. Check notable changes
6. Update TypeScript types
7. Review changelog

## Installing

**Important!** New JSX Transform is required for React 19.

**JSX Transform Requirements:**
- React 19 requires the new JSX transform introduced in 2020
- Enables `ref` as a prop and JSX performance improvements
- Most environments already have this enabled
- Without it, you'll see a warning about outdated JSX transform

**NPM Installation:**
```bash
npm install --save-exact react@^19.0.0 react-dom@^19.0.0
npm install --save-exact @types/react@^19.0.0 @types/react-dom@^19.0.0
```

**Yarn Installation:**
```bash
yarn add --exact react@^19.0.0 react-dom@^19.0.0
yarn add --exact @types/react@^19.0.0 @types/react-dom@^19.0.0
```

## Codemods

**Run All React 19 Codemods:**
```bash
npx codemod@latest react/19/migration-recipe
```

**Included Codemods:**
- `replace-reactdom-render` - Updates ReactDOM.render to createRoot
- `replace-string-ref` - Converts string refs to ref callbacks
- `replace-act-import` - Moves act import from react-dom/test-utils to react
- `replace-use-form-state` - Updates form state hooks
- `prop-types-typescript` - Migrates PropTypes to TypeScript

*Note: TypeScript changes require separate codemods (see TypeScript section)*

**Why Use Codemods:**
- Faster than manual migration
- Handles complex code patterns
- Better TypeScript support
- Maintained by codemod.com team

## Breaking Changes

### Error Handling Changes

**New Error Behavior:**
- Errors in render are no longer re-thrown
- Reduces duplicate error logs in DEV mode

**Error Reporting:**
- **Uncaught Errors:** Reported to `window.reportError`
- **Caught Errors:** Reported to `console.error`

**Custom Error Handling:**
```javascript
const root = createRoot(container, {
  onUncaughtError: (error, errorInfo) => {
    // Log error report
  },
  onCaughtError: (error, errorInfo) => {
    // Log error report
  }
});
```

*Important: Update error handling if production error reporting relies on re-thrown errors*

### Removed: propTypes and defaultProps for Functions

**Deprecated Since:** April 2017 (v15.5.0)

**Changes:**
- `propTypes` removed from React package (silently ignored if used)
- `defaultProps` removed from function components
- Use ES6 default parameters instead
- Class components still support `defaultProps`

**Migration Example:**
```javascript
// Before
import PropTypes from 'prop-types';

function Heading({text}) {
  return <h1>{text}</h1>;
}
Heading.propTypes = {
  text: PropTypes.string,
};
Heading.defaultProps = {
  text: 'Hello, world!',
};

// After
interface Props {
  text?: string;
}
function Heading({text = 'Hello, world!'}: Props) {
  return <h1>{text}</h1>;
}
```

**Codemod:**
```bash
npx codemod@latest react/prop-types-typescript
```
### Removed: Legacy Context (contextTypes and getChildContext)

**Deprecated Since:** October 2018 (v16.6.0)

**Why Removed:**
- Only available in class components
- Replaced with `contextType` due to subtle bugs
- Makes React smaller and faster

**Migration Example:**
```javascript
// Before
import PropTypes from 'prop-types';

class Parent extends React.Component {
  static childContextTypes = {
    foo: PropTypes.string.isRequired,
  };

  getChildContext() {
    return { foo: 'bar' };
  }

  render() {
    return <Child />;
  }
}

class Child extends React.Component {
  static contextTypes = {
    foo: PropTypes.string.isRequired,
  };

  render() {
    return <div>{this.context.foo}</div>;
  }
}

// After
const FooContext = React.createContext();

class Parent extends React.Component {
  render() {
    return (
      <FooContext value='bar'>
        <Child />
      </FooContext>
    );
  }
}

class Child extends React.Component {
  static contextType = FooContext;

  render() {
    return <div>{this.context}</div>;
  }
}
```
### Removed: String Refs

**Deprecated Since:** March 2018 (v16.3.0)

**Why Removed:**
- Multiple downsides compared to ref callbacks
- Makes React simpler and easier to understand

**Migration Example:**
```javascript
// Before
class MyComponent extends React.Component {
  componentDidMount() {
    this.refs.input.focus();
  }

  render() {
    return <input ref='input' />;
  }
}

// After
class MyComponent extends React.Component {
  componentDidMount() {
    this.input.focus();
  }

  render() {
    return <input ref={input => this.input = input} />;
  }
}
```

**Codemod:**
```bash
npx codemod@latest react/19/replace-string-ref
```
### Removed: Module Pattern Factories

**Deprecated Since:** August 2019 (v16.9.0)

**Why Removed:**
- Rarely used pattern
- Makes React larger and slower than necessary

**Migration Example:**
```javascript
// Before
function FactoryComponent() {
  return { render() { return <div />; } }
}

// After
function FactoryComponent() {
  return <div />;
}
```
### Removed: React.createFactory

**Deprecated Since:** February 2020 (v16.13.0)

**Why Removed:**
- Common before JSX support
- Rarely used today
- Can be replaced with JSX

**Migration Example:**
```javascript
// Before
import { createFactory } from 'react';
const button = createFactory('button');

// After
const button = <button />;
```
### Removed: react-test-renderer/shallow

**Migration Steps:**
```bash
npm install react-shallow-renderer --save-dev
```

```javascript
- import ShallowRenderer from 'react-test-renderer/shallow';
+ import ShallowRenderer from 'react-shallow-renderer';
```

**Important!** Consider migrating away from shallow rendering:
- Depends on React internals
- Can block future upgrades
- Recommended alternatives: `@testing-library/react` or `@testing-library/react-native`

### Removed: react-dom/test-utils

**act Migration:**
```javascript
- import {act} from 'react-dom/test-utils'
+ import {act} from 'react';
```

**All Other test-utils Functions Removed:**
- Were uncommon and made it too easy to depend on low-level implementation details
- Will error when called in React 19
- Exports will be removed in future versions

**Codemod:**
```bash
npx codemod@latest react/19/replace-act-import
```
### Removed: ReactDOM.render

**Deprecated Since:** March 2022 (v18.0.0)

**Migration Example:**
```javascript
// Before
import {render} from 'react-dom';
render(<App />, document.getElementById('root'));

// After
import {createRoot} from 'react-dom/client';
const root = createRoot(document.getElementById('root'));
root.render(<App />);
```

**Codemod:**
```bash
npx codemod@latest react/19/replace-reactdom-render
```
### Removed: ReactDOM.hydrate

**Deprecated Since:** March 2022 (v18.0.0)

**Migration Example:**
```javascript
// Before
import {hydrate} from 'react-dom';
hydrate(<App />, document.getElementById('root'));

// After
import {hydrateRoot} from 'react-dom/client';
hydrateRoot(document.getElementById('root'), <App />);
```

**Codemod:**
```bash
npx codemod@latest react/19/replace-reactdom-render
```
### Removed: unmountComponentAtNode

**Deprecated Since:** March 2022 (v18.0.0)

**Migration Example:**
```javascript
// Before
unmountComponentAtNode(document.getElementById('root'));

// After
root.unmount();
```

**Codemod:**
```bash
npx codemod@latest react/19/replace-reactdom-render
```
### Removed: ReactDOM.findDOMNode

**Deprecated Since:** October 2018 (v16.6.0)

**Why Removed:**
- Legacy escape hatch
- Slow to execute
- Fragile to refactoring
- Only returned first child
- Broke abstraction levels

**Migration Example:**
```javascript
// Before
import {findDOMNode} from 'react-dom';

function AutoselectingInput() {
  useEffect(() => {
    const input = findDOMNode(this);
    input.select()
  }, []);

  return <input defaultValue="Hello" />;
}

// After
function AutoselectingInput() {
  const ref = useRef(null);
  useEffect(() => {
    ref.current.select();
  }, []);

  return <input ref={ref} defaultValue="Hello" />
}
```
## New Deprecations

### Deprecated: element.ref

**Changes:**
- `ref` is now a regular prop in React 19
- `element.ref` deprecated in favor of `element.props.ref`
- Accessing `element.ref` will trigger warning
- Will be removed from JSX Element type in future release

### Deprecated: react-test-renderer

**Why Deprecated:**
- Implements own renderer environment that doesn't match user environments
- Promotes testing implementation details
- Relies on introspection of React internals
- Better alternatives now available

**Current Behavior in React 19:**
- Logs deprecation warning
- Switched to concurrent rendering

**Recommended Migration:**
- Use `@testing-library/react` for web
- Use `@testing-library/react-native` for native
- Modern, well-supported testing experience

## Notable Changes

### StrictMode Changes

**Improvements:**
- `useMemo` and `useCallback` reuse memoized results from first render during second render in double-rendering
- Components already Strict Mode compatible should see no behavior difference
- Designed to surface bugs during development before production

**Example Behavior:**
- Strict Mode double-invokes ref callback functions on initial mount
- Simulates mounted component replacement by Suspense fallback

### Suspense Improvements

**Previous Behavior:**
- Component suspends → suspended siblings rendered → fallback committed

**New Behavior in React 19:**
- Component suspends → fallback immediately committed → suspended siblings rendered

**Benefits:**
- Suspense fallbacks display faster
- Still pre-warms lazy requests in suspended tree
- Better user experience with faster visual feedback

### UMD Builds Removed

**Why Removed:**
- Modern alternatives available for loading modules in HTML
- Reduces complexity of testing and release process

**Alternative - Use ESM-based CDN:**
```html
<script type="module">
  import React from "https://esm.sh/react@19/?dev"
  import ReactDOMClient from "https://esm.sh/react-dom@19/client?dev"
  ...
</script>
```

*Recommended CDN: esm.sh*
### Libraries Depending on React Internals

**Important!** Changes to React internals may impact libraries using internal APIs.

**Internal API Renaming:**
- `SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED` renamed to
- `_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE`

**Recommendations:**
- Remove any code depending on React internals
- Follow official React guidelines
- Not listed as breaking changes per Versioning Policy
- Future versions will more aggressively block internal API access

## TypeScript Changes

### Removed Deprecated TypeScript Types

**Types Cleanup:**
- Removed types based on removed APIs
- Some types moved to more relevant packages
- Others no longer needed

**Migration Codemod:**
```bash
npx types-react-codemod@latest preset-19 ./path-to-app
```

**Additional Codemod for element.props:**
```bash
npx types-react-codemod@latest react-element-default-any-props ./path-to-your-react-ts-files
```

### Ref Cleanup Requirements

**Included in:** `react-19` codemod preset as `no-implicit-ref-callback-return`

**Change:**
- Ref cleanup functions introduced
- Returning anything from ref callback now rejected by TypeScript
- Stop using implicit returns

**Migration Example:**
```javascript
- <div ref={current => (instance = current)} />
+ <div ref={current => {instance = current}} />
```

*Why: TypeScript can't distinguish between cleanup function and instance return*

### useRef Requires Argument

**Included in:** `react-19` codemod preset as `refobject-defaults`

**Changes:**
- `useRef` now requires an argument
- Simplifies type signature
- Behaves like `createContext`
- All refs are now mutable

**Examples:**
```typescript
// Error - no argument
useRef();

// Passes
useRef(undefined);

// Error - no argument
createContext();

// Passes
createContext(undefined);
```

**All Refs Now Mutable:**
```typescript
const ref = useRef<number>(null);
ref.current = 1; // Now works, previously read-only
```

**Type Changes:**
- `MutableRef` deprecated
- Single `RefObject` type returned by `useRef`

**Convenience Overloads:**
- `useRef<T>(null)` returns `RefObject<T | null>`
- `useRef(undefined)` returns `RefObject<T | undefined>`

### ReactElement TypeScript Type Changes

**Included in:** `react-element-default-any-props` codemod

**Change:**
- Props default to `unknown` instead of `any` for `ReactElement`

**With Type Argument (Unchanged):**
```typescript
type Example2 = ReactElement<{ id: string }>["props"];
//   ^? { id: string }
```

**Without Type Argument (Changed):**
```typescript
type Example = ReactElement["props"];
//   ^? Before: 'any', Now: 'unknown'
```

**When Needed:**
- Legacy code with unsound element props access
- Element introspection as escape hatch
- Make unsound access explicit with `any`

### JSX Namespace in TypeScript

**Included in:** `react-19` codemod preset as `scoped-jsx`

**Change:**
- Global JSX namespace removed
- Use `React.JSX` instead
- Prevents global type pollution
- Prevents conflicts between UI libraries

**Module Augmentation:**
```typescript
// global.d.ts
+ declare module "react" {
    namespace JSX {
      interface IntrinsicElements {
        "my-element": {
          myElementProps: string;
        };
      }
    }
+ }
```

**Module Specifier Based on JSX Runtime:**
- `"jsx": "react-jsx"` → `react/jsx-runtime`
- `"jsx": "react-jsxdev"` → `react/jsx-dev-runtime`
- `"jsx": "react"` or `"jsx": "preserve"` → `react`
### Better useReducer Typings

**Improvements:**
- Improved type inference (thanks to @mfp22)
- Breaking change in type parameters

**Best Practice (No Type Arguments):**
```typescript
- useReducer<React.Reducer<State, Action>>(reducer)
+ useReducer(reducer)
```

**Edge Cases (Explicit State and Action):**
```typescript
- useReducer<React.Reducer<State, Action>>(reducer)
+ useReducer<State, [Action]>(reducer)
```

**Inline Reducer (Annotate Parameters):**
```typescript
- useReducer<React.Reducer<State, Action>>((state, action) => state)
+ useReducer((state: State, action: Action) => state)
```

**External Reducer:**
```typescript
const reducer = (state: State, action: Action) => state;
```
## Changelog

### Other Breaking Changes

- **react-dom:** Error for javascript URLs in src and href (#26507)
- **react-dom:** Remove `errorInfo.digest` from `onRecoverableError` (#28222)
- **react-dom:** Remove `unstable_flushControlled` (#26397)
- **react-dom:** Remove `unstable_createEventHandle` (#28271)
- **react-dom:** Remove `unstable_renderSubtreeIntoContainer` (#28271)
- **react-dom:** Remove `unstable_runWithPriority` (#28271)
- **react-is:** Remove deprecated methods (#28224)

### Other Notable Changes

- **react:** Batch sync, default and continuous lanes (#25700)
- **react:** Don't prerender siblings of suspended component (#26380)
- **react:** Detect infinite update loops caused by render phase updates (#26625)
- **react-dom:** Transitions in popstate are now synchronous (#26025)
- **react-dom:** Remove layout effect warning during SSR (#26395)
- **react-dom:** Warn and don't set empty string for src/href (except anchor tags) (#28124)

*For full changelog, see official React 19 Changelog*