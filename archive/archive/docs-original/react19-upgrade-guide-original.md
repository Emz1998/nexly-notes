================
CODE SNIPPETS
================
TITLE: Execute React 19 migration codemods
DESCRIPTION: This command runs the `codemod` tool with the React 19 migration recipe, which automatically updates code to many new APIs and patterns introduced in React 19. It streamlines the upgrade process by applying common code transformations.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: bash
CODE:
```
npx codemod@latest react/19/migration-recipe
```

--------------------------------

TITLE: Run Codemod to Migrate 'ReactDOM.render' to React 19
DESCRIPTION: Execute this 'npx' command to automatically migrate `ReactDOM.render` calls to the `ReactDOM.createRoot` API, preparing your React application for React 19.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: bash
CODE:
```
npx codemod@latest react/19/replace-reactdom-render
```

--------------------------------

TITLE: Install React 19 TypeScript type definitions
DESCRIPTION: These commands install the exact version 19 of TypeScript type definitions for React and React DOM. This is an essential step for TypeScript projects to ensure proper type checking and compatibility when upgrading to React 19, available for both npm and Yarn.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: bash
CODE:
```
npm install --save-exact @types/react@^19.0.0 @types/react-dom@^19.0.0
```

LANGUAGE: bash
CODE:
```
yarn add --exact @types/react@^19.0.0 @types/react-dom@^19.0.0
```

--------------------------------

TITLE: Run Codemod to Migrate React 'act' Import to React 19
DESCRIPTION: This 'npx' command executes a codemod to automatically update `ReactDOMTestUtils.act` calls to `React.act` and adjust import paths, simplifying the migration process to React 19.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: bash
CODE:
```
npx codemod@latest react/19/replace-act-import
```

--------------------------------

TITLE: Migrate from react-test-renderer/shallow to react-shallow-renderer
DESCRIPTION: This snippet provides instructions for migrating from `react-test-renderer/shallow` to directly using `react-shallow-renderer` by installing it as a dependency and updating import statements. `react-test-renderer/shallow` is being removed in React 19.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: shell
CODE:
```
npm install react-shallow-renderer --save-dev
```

LANGUAGE: diff
CODE:
```
- import ShallowRenderer from 'react-test-renderer/shallow';  
+ import ShallowRenderer from 'react-shallow-renderer';
```

--------------------------------

TITLE: Migrate 'ReactDOM.hydrate' to 'ReactDOM.hydrateRoot' in React 19
DESCRIPTION: React 19 removes `ReactDOM.hydrate`. This snippet shows the migration path to `ReactDOM.hydrateRoot` for server-rendered applications, ensuring proper hydration of your React components.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: javascript
CODE:
```
// Before  
import {hydrate} from 'react-dom';  
hydrate(<App />, document.getElementById('root'));
```

LANGUAGE: javascript
CODE:
```
// After  
import {hydrateRoot} from 'react-dom/client';  
hydrateRoot(document.getElementById('root'), <App />);
```

--------------------------------

TITLE: Migrate 'ReactDOM.findDOMNode' to React DOM Refs
DESCRIPTION: `ReactDOM.findDOMNode` is removed due to its performance issues and fragility. This example shows how to replace `findDOMNode` functionality with `useRef` and direct DOM manipulation via `ref.current` for more robust and performant code.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: javascript
CODE:
```
// Before  
import {findDOMNode} from 'react-dom';  

function AutoselectingInput() {  
  useEffect(() => {  
    const input = findDOMNode(this);  
    input.select()  
  }, []);  

  return <input defaultValue="Hello" />;  
}
```

LANGUAGE: javascript
CODE:
```
// After  
function AutoselectingInput() {  
  const ref = useRef(null);  
  useEffect(() => {  
    ref.current.select();  
  }, []);  

  return <input ref={ref} defaultValue="Hello" />  
}
```

--------------------------------

TITLE: Codemod for React string refs to ref callbacks migration
DESCRIPTION: Use this `npx codemod` command to automatically migrate string refs in your React project to ref callbacks. This assists in updating to the recommended ref management approach.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: shell
CODE:
```
npx codemod@latest react/19/replace-string-ref
```

--------------------------------

TITLE: Install React 19 and React DOM core libraries
DESCRIPTION: These commands install the latest React 19 and React DOM packages with exact version matching. They are the primary steps for updating your application's core React dependencies to version 19, available for both npm and Yarn users.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: bash
CODE:
```
npm install --save-exact react@^19.0.0 react-dom@^19.0.0
```

LANGUAGE: bash
CODE:
```
yarn add --exact react@^19.0.0 react-dom@^19.0.0
```

--------------------------------

TITLE: Codemod for React PropTypes to TypeScript migration
DESCRIPTION: Use this `npx codemod` command to automatically migrate `propTypes` in your React project to TypeScript. This helps in transitioning from deprecated `propTypes` to a type-checking solution.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: shell
CODE:
```
npx codemod@latest react/prop-types-typescript
```

--------------------------------

TITLE: Migrate `element.props` TypeScript Access with Codemod
DESCRIPTION: This command provides an additional `npx types-react-codemod` option, `react-element-default-any-props`, specifically for migrating TypeScript files that have unsound access patterns to `element.props` in React 19. It targets a specified path to your React TypeScript files.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: shell
CODE:
```
npx types-react-codemod@latest react-element-default-any-props ./path-to-your-react-ts-files
```

--------------------------------

TITLE: Migrate React.createFactory usage to JSX
DESCRIPTION: This snippet illustrates how to replace `React.createFactory` calls with standard JSX syntax. `createFactory` was common before JSX but is now deprecated and being removed in React 19.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: javascript
CODE:
```
// Before  

import { createFactory } from 'react';  

  

const button = createFactory('button');
```

LANGUAGE: javascript
CODE:
```
// After  

const button = <button />;
```

--------------------------------

TITLE: Migrate React class components from string refs to ref callbacks
DESCRIPTION: This snippet shows how to update React class components from using deprecated string refs to the recommended ref callback pattern. String refs are being removed in React 19 for simplicity and improved understanding.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: javascript
CODE:
```
// Before  

class MyComponent extends React.Component {  

  componentDidMount() {  

    this.refs.input.focus();  

  }  

  

  render() {  

    return <input ref='input' />;

  }  

}
```

LANGUAGE: javascript
CODE:
```
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

--------------------------------

TITLE: Install React 18 using npm or Yarn
DESCRIPTION: These commands demonstrate how to install the latest versions of React and ReactDOM using either the npm or Yarn package manager. This is the initial step for upgrading your project to React 18.

SOURCE: https://react.dev/blog/2022/03/08/react-18-upgrade-guide

LANGUAGE: shell
CODE:
```
npm install react react-dom
```

LANGUAGE: shell
CODE:
```
yarn add react react-dom
```

--------------------------------

TITLE: Migrate 'unmountComponentAtNode' to 'root.unmount()' in React 19
DESCRIPTION: `ReactDOM.unmountComponentAtNode` is removed in React 19. This example demonstrates how to switch to using the `root.unmount()` method provided by `createRoot` or `hydrateRoot` for unmounting components.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: javascript
CODE:
```
// Before  
unmountComponentAtNode(document.getElementById('root'));
```

LANGUAGE: javascript
CODE:
```
// After  
root.unmount();
```

--------------------------------

TITLE: Migrate 'ReactDOM.render' to 'ReactDOM.createRoot' in React 19
DESCRIPTION: `ReactDOM.render` is removed in React 19. This example demonstrates how to refactor your application's entry point to use `ReactDOM.createRoot` for rendering, which offers improved performance and concurrent features.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: javascript
CODE:
```
// Before  
import {render} from 'react-dom';  
render(<App />, document.getElementById('root'));
```

LANGUAGE: javascript
CODE:
```
// After  
import {createRoot} from 'react-dom/client';  
const root = createRoot(document.getElementById('root'));  
root.render(<App />);
```

--------------------------------

TITLE: Load React 19 via ESM CDN in HTML
DESCRIPTION: This snippet demonstrates how to load React 19 and ReactDOMClient directly in an HTML document using an ESM-based CDN like esm.sh. React 19 no longer provides UMD builds, requiring this modern approach for script-tag-based loading.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: html
CODE:
```
<script type="module">
  import React from "https://esm.sh/react@19/?dev"
  import ReactDOMClient from "https://esm.sh/react-dom@19/client?dev"
  ...
</script>
```

--------------------------------

TITLE: Require Argument for `useRef` and `createContext` (TypeScript)
DESCRIPTION: React 19 updates `useRef` and `createContext` to require an argument, simplifying their type signatures and making them behave more consistently. This change ensures explicit initialization. The `react-19` codemod preset `refobject-defaults` helps migrate.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: typescript
CODE:
```
// @ts-expect-error: Expected 1 argument but saw none  
useRef();  
// Passes  
useRef(undefined);  
// @ts-expect-error: Expected 1 argument but saw none  
createContext();  
// Passes  
createContext(undefined);
```

--------------------------------

TITLE: Migrate React 'act' Import from 'react-dom/test-utils' to 'react'
DESCRIPTION: React 19 moves the 'act' utility from 'react-dom/test-utils' to the 'react' package. This snippet demonstrates how to update your import statements to correctly use 'act' directly from the 'react' package.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: javascript
CODE:
```
// Before
import {act} from 'react-dom/test-utils';
```

LANGUAGE: javascript
CODE:
```
// After
import {act} from 'react';
```

--------------------------------

TITLE: Migrate React 19 TypeScript Types with Codemod Preset
DESCRIPTION: This command shows how to use the `npx types-react-codemod` utility with the `preset-19` option to automatically migrate most breaking TypeScript type changes introduced in React 19. It should be run in the root of your application's directory.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: shell
CODE:
```
npx types-react-codemod@latest preset-19 ./path-to-app
```

--------------------------------

TITLE: Explicit `useReducer` State and Action Types (TypeScript)
DESCRIPTION: For edge cases where type inference might not be sufficient, `useReducer` now accepts explicit `State` and `Action` types as generic arguments. The `Action` type should be provided in a tuple `[Action]`. This allows precise typing when needed.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: typescript
CODE:
```
- useReducer<React.Reducer<State, Action>>(reducer)  
+ useReducer<State, [Action]>(reducer)
```

--------------------------------

TITLE: Update React Client Unmount API: Migrate from unmountComponentAtNode to root.unmount
DESCRIPTION: With the introduction of the new root API in React 18, the method for unmounting a component has changed. This code demonstrates how to update your existing calls from `unmountComponentAtNode` to the new `root.unmount` method.

SOURCE: https://react.dev/blog/2022/03/08/react-18-upgrade-guide

LANGUAGE: javascript
CODE:
```
// Before  
unmountComponentAtNode(container);  
  
// After  
root.unmount();
```

--------------------------------

TITLE: Update React Client Root API: Migrate from render to createRoot
DESCRIPTION: React 18 introduces a new root API, `createRoot`, which provides better ergonomics and enables concurrent features. This snippet shows how to replace the deprecated `ReactDOM.render` with the new `createRoot` API for client-side application rendering.

SOURCE: https://react.dev/blog/2022/03/08/react-18-upgrade-guide

LANGUAGE: javascript
CODE:
```
// Before  
import { render } from 'react-dom';  
const container = document.getElementById('app');  
render(<App tab="home" />, container);  
  
// After  
import { createRoot } from 'react-dom/client';  
const container = document.getElementById('app');  
const root = createRoot(container); // createRoot(container!) if you use TypeScript  
root.render(<App tab="home" />);
```

--------------------------------

TITLE: Migrate React Module Pattern Factories to standard function components
DESCRIPTION: This snippet demonstrates how to convert React components written as module pattern factories to standard function components. Module pattern factories are being removed in React 19 as they were rarely used.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: javascript
CODE:
```
// Before  

function FactoryComponent() {  

  return { render() { return <div />; } }  

}
```

LANGUAGE: javascript
CODE:
```
// After  

function FactoryComponent() {  

  return <div />;

}
```

--------------------------------

TITLE: Mutable `useRef` Current Property (TypeScript)
DESCRIPTION: With React 19, `useRef` always returns a mutable `RefObject`. This resolves the issue where `ref.current` was read-only if initialized with `null`, allowing direct assignment to `ref.current` without type errors. The `MutableRef` type is now deprecated.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: typescript
CODE:
```
const ref = useRef<number>(null);  
  
// Cannot assign to 'current' because it is a read-only property  
ref.current = 1;
```

--------------------------------

TITLE: Migrate React class components from Legacy Context to new Context API
DESCRIPTION: This snippet illustrates the migration from the deprecated Legacy Context API (`contextTypes`, `getChildContext`) in React class components to the modern Context API (`React.createContext`, `contextType`). Legacy Context is being removed in React 19 due to subtle bugs.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: javascript
CODE:
```
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
```

LANGUAGE: javascript
CODE:
```
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

--------------------------------

TITLE: Migrate React function components from PropTypes and defaultProps to TypeScript/ES6
DESCRIPTION: This snippet demonstrates how to migrate React function components that use `propTypes` and `defaultProps` to a modern approach using TypeScript interfaces and ES6 default parameters. The `propTypes` and `defaultProps` APIs are being removed for function components in React 19.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: javascript
CODE:
```
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
```

LANGUAGE: typescript
CODE:
```
// After  

interface Props {  

  text?: string;  

}  

function Heading({text = 'Hello, world!'}: Props) {  

  return <h1>{text}</h1>;  

}
```

--------------------------------

TITLE: New `RefObject` Type Definition for `useRef` (TypeScript)
DESCRIPTION: React 19 introduces a unified `RefObject<T>` type returned by `useRef`, deprecating `MutableRef`. This interface defines the `current` property which holds the mutable reference value. Overloads exist for `useRef<T>(null)` and `useRef(undefined)` to ease migration.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: typescript
CODE:
```
interface RefObject<T> {  
  current: T  
}  
  
declare function useRef<T>: RefObject<T>
```

--------------------------------

TITLE: Annotate External Reducer Parameters for `useReducer` (TypeScript)
DESCRIPTION: If a reducer function is defined outside the `useReducer` call, its parameters should be explicitly annotated with their respective types (`state: State`, `action: Action`). This ensures correct type inference when the reducer is passed to `useReducer`.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: typescript
CODE:
```
const reducer = (state: State, action: Action) => state;
```

--------------------------------

TITLE: Default `ReactElement` Props Type Changed to `unknown` (TypeScript)
DESCRIPTION: In React 19, the default type for `ReactElement`'s `props` has changed from `any` to `unknown` if no type argument is provided. This requires explicit handling of `unknown` when accessing props, improving type safety. The `react-element-default-any-props` codemod addresses this.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: typescript
CODE:
```
type Example = ReactElement["props"];  
//   ^? Before, was 'any', now 'unknown'
```

--------------------------------

TITLE: Handle React 18 Render Callbacks using useEffect
DESCRIPTION: React 18 removes the callback parameter from the `render` function as it could lead to unexpected results with Suspense. This example illustrates how to achieve similar post-render functionality by utilizing the `useEffect` hook within a component.

SOURCE: https://react.dev/blog/2022/03/08/react-18-upgrade-guide

LANGUAGE: javascript
CODE:
```
// Before  
const container = document.getElementById('app');  
render(<App tab="home" />, container, () => {  
  console.log('rendered');  
});  
  
// After  
function AppWithCallbackAfterRender() {  
  useEffect(() => {  
    console.log('rendered');  
  });  
  
  return <App tab="home" />  
}  
  
const container = document.getElementById('app');  
const root = createRoot(container);  
root.render(<AppWithCallbackAfterRender />);
```

--------------------------------

TITLE: Improved `useReducer` Type Inference (TypeScript)
DESCRIPTION: React 19's `useReducer` now has improved type inference, making it best practice to omit explicit type arguments and rely on contextual typing. This reduces boilerplate and simplifies its usage, though it's a breaking change from previous explicit full reducer type parameters.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: typescript
CODE:
```
- useReducer<React.Reducer<State, Action>>(reducer)  
+ useReducer(reducer)
```

--------------------------------

TITLE: Implement custom error handling for React 19 root
DESCRIPTION: This JavaScript code demonstrates how to provide custom error handling functions when creating a React root using `createRoot`. It allows developers to define specific logic for logging or reporting both uncaught and caught errors in React 19, improving error reporting granularity.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: javascript
CODE:
```
const root = createRoot(container, {  
  onUncaughtError: (error, errorInfo) => {  
    // ... log error report  
  },  
  onCaughtError: (error, errorInfo) => {  
    // ... log error report  
  }  
});
```

--------------------------------

TITLE: Explicit `ReactElement` Props Type (TypeScript)
DESCRIPTION: When a type argument is passed to `ReactElement`, its `props` type is correctly inferred. This example demonstrates how `ReactElement<{ id: string }>` correctly sets the `props` type to `{ id: string }`. This behavior is unchanged.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: typescript
CODE:
```
type Example2 = ReactElement<{ id: string }>["props"];  
//   ^? { id: string }
```

--------------------------------

TITLE: Update React Client Hydration API: Migrate from hydrate to hydrateRoot
DESCRIPTION: For applications using server-side rendering (SSR) with hydration, React 18 introduces `hydrateRoot`. This snippet shows the necessary change from the older `ReactDOM.hydrate` function to the new `hydrateRoot` API for hydrating server-rendered HTML.

SOURCE: https://react.dev/blog/2022/03/08/react-18-upgrade-guide

LANGUAGE: javascript
CODE:
```
// Before  
import { hydrate } from 'react-dom';  
const container = document.getElementById('app');  
hydrate(<App tab="home" />, container);  
  
// After  
import { hydrateRoot } from 'react-dom/client';  
const container = document.getElementById('app');  
const root = hydrateRoot(container, <App tab="home" />);  
// Unlike with createRoot, you don't need a separate root.render() call here.
```

--------------------------------

TITLE: Annotate Inline Reducer Parameters for `useReducer` (TypeScript)
DESCRIPTION: When defining the reducer function inline with `useReducer`, the new best practice is to annotate the function parameters directly with their types (`state: State`, `action: Action`). This provides clear type information without needing to pass type arguments to `useReducer` itself.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: typescript
CODE:
```
- useReducer<React.Reducer<State, Action>>((state, action) => state)  
+ useReducer((state: State, action: Action) => state)
```

--------------------------------

TITLE: Augmenting JSX Namespace within `declare module` (TypeScript)
DESCRIPTION: React 19 moves the global `JSX` namespace into `React.JSX` to prevent global type pollution. To augment the `JSX` namespace, such as adding custom intrinsic elements, you must now wrap the augmentation within a `declare module "react"` block. The specific module specifier depends on your `tsconfig.json`'s `jsx` setting.

SOURCE: https://react.dev/blog/2024/04/25/react-19-upgrade-guide

LANGUAGE: typescript
CODE:
```
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

--------------------------------

TITLE: Configure React Testing Environment for `act()` Warnings
DESCRIPTION: To resolve `act()` warnings when updating tests to use `createRoot` in React 18, set `globalThis.IS_REACT_ACT_ENVIRONMENT` to `true` in your test setup file. This flag informs React that it is running in a unit test-like environment, enabling helpful warnings if an update is not wrapped with `act`.

SOURCE: https://react.dev/blog/2022/03/08/react-18-upgrade-guide

LANGUAGE: javascript
CODE:
```
// In your test setup file
globalThis.IS_REACT_ACT_ENVIRONMENT = true;
```

--------------------------------

TITLE: Opt-out of React 18 Automatic Batching with flushSync
DESCRIPTION: To opt-out of React 18's automatic batching for specific state updates, you can use the `flushSync` function imported from 'react-dom'. This example demonstrates how `flushSync` forces React to immediately re-render and update the DOM after each wrapped state update, rather than batching them.

SOURCE: https://react.dev/blog/2022/03/08/react-18-upgrade-guide

LANGUAGE: javascript
CODE:
```
import { flushSync } from 'react-dom';  
  
function handleClick() {  
  flushSync(() => {  
    setCounter(c => c + 1);  
  });  
  // React has updated the DOM by now  
  flushSync(() => {  
    setFlag(f => !f);  
  });  
  // React has updated the DOM by now  
}
```

--------------------------------

TITLE: Install React Compiler as a Development Dependency
DESCRIPTION: Installs the `babel-plugin-react-compiler` as a development dependency using npm, yarn, or pnpm. The `@rc` tag is used to get the latest release candidate version of the compiler plugin.

SOURCE: https://react.dev/learn/react-compiler/installation

LANGUAGE: bash
CODE:
```
npm install -D babel-plugin-react-compiler@rc
```

LANGUAGE: bash
CODE:
```
yarn add -D babel-plugin-react-compiler@rc
```

LANGUAGE: bash
CODE:
```
pnpm install -D babel-plugin-react-compiler@rc
```

--------------------------------

TITLE: Define children Prop in React TypeScript Interface
DESCRIPTION: In React 18, TypeScript definitions require explicit listing of the 'children' prop in component interfaces. This example shows how to define a prop type, including an optional 'children' prop of type 'React.ReactNode', ensuring safer type checking for components.

SOURCE: https://react.dev/blog/2022/03/08/react-18-upgrade-guide

LANGUAGE: typescript
CODE:
```
interface MyButtonProps {  
  color: string;  
  children?: React.ReactNode;  
}
```

--------------------------------

TITLE: Demonstrate React 18 Automatic Batching
DESCRIPTION: This example illustrates the new automatic batching behavior in React 18 when using `createRoot`. It shows that regardless of their origin (e.g., event handlers, `setTimeout`, promises), all state updates are automatically batched into a single re-render, improving performance by reducing unnecessary renders.

SOURCE: https://react.dev/blog/2022/03/08/react-18-upgrade-guide

LANGUAGE: javascript
CODE:
```
// After React 18 updates inside of timeouts, promises,  
// native event handlers or any other event are batched.  
  
function handleClick() {  
  setCount(c => c + 1);  
  setFlag(f => !f);  
  // React will only re-render once at the end (that's batching!)  
}  
  
setTimeout(() => {  
  setCount(c => c + 1);  
  setFlag(f => !f);  
  // React will only re-render once at the end (that's batching!)  
}, 1000);
```

--------------------------------

TITLE: Migrate `act` Import from `react-dom/test-utils` to `react`
DESCRIPTION: This snippet demonstrates updating the import source for the `act` function. The `act` utility, crucial for testing React components that involve state updates, has been moved directly into the `react` package to centralize its availability. This change simplifies imports and aligns with current React testing recommendations.

SOURCE: https://react.dev/warnings/react-dom-test-utils

LANGUAGE: javascript
CODE:
```
import {act} from 'react-dom/test-utils';
```

LANGUAGE: javascript
CODE:
```
import {act} from 'react';
```

--------------------------------

TITLE: Illustrate React 17 Batching Behavior
DESCRIPTION: This JavaScript code demonstrates the batching behavior in React versions prior to React 18. It shows that while state updates within a React event handler are batched into a single re-render, updates initiated outside of React's event system (e.g., within `setTimeout`) are not batched, leading to multiple renders.

SOURCE: https://react.dev/blog/2022/03/08/react-18-upgrade-guide

LANGUAGE: javascript
CODE:
```
// Before React 18 only React events were batched  
  
function handleClick() {  
  setCount(c => c + 1);  
  setFlag(f => !f);  
  // React will only re-render once at the end (that's batching!)  
}  
  
setTimeout(() => {  
  setCount(c => c + 1);  
  setFlag(f => !f);  
  // React will render twice, once for each state update (no batching)  
}, 1000);
```

--------------------------------

TITLE: Install Vite Plugin Babel for Compiler Integration
DESCRIPTION: Installs `vite-plugin-babel` as a development dependency. This plugin provides a way to apply Babel configurations separately within a Vite project, enabling flexible integration of `babel-plugin-react-compiler`.

SOURCE: https://react.dev/learn/react-compiler/installation

LANGUAGE: bash
CODE:
```
npm install -D vite-plugin-babel
```

--------------------------------

TITLE: Verify React Compiler Output in JavaScript
DESCRIPTION: This JavaScript code snippet demonstrates the kind of automatic memoization logic that the React Compiler inserts into your build output. It shows how the compiler uses a runtime function (`_c`) and a memo cache sentinel to optimize component rendering, ensuring that expensive calculations or renderings are only performed when necessary.

SOURCE: https://react.dev/learn/react-compiler/installation

LANGUAGE: javascript
CODE:
```
import { c as _c } from "react/compiler-runtime";  

export default function MyApp() {  

  const $ = _c(1);  

  let t0;  

  if ($[0] === Symbol.for("react.memo_cache_sentinel")) {  

    t0 = <div>Hello World</div>;  

    $[0] = t0;  

  } else {  

    t0 = $[0];  

  }  

  return t0;  

}
```

--------------------------------

TITLE: Install ESLint Plugin for React Compiler Integration
DESCRIPTION: Installs `eslint-plugin-react-hooks` as a development dependency, specifically the release candidate (`@rc`) version. This plugin includes a rule that identifies code segments that the React Compiler cannot optimize, helping developers understand potential optimization limitations.

SOURCE: https://react.dev/learn/react-compiler/installation

LANGUAGE: bash
CODE:
```
npm install -D eslint-plugin-react-hooks@rc
```

--------------------------------

TITLE: Configure React Compiler in Babel
DESCRIPTION: Adds `babel-plugin-react-compiler` to the `plugins` array in your `babel.config.js` file. It is crucial for the React Compiler plugin to be listed first in the Babel plugin pipeline to ensure it processes the original source code before other transformations.

SOURCE: https://react.dev/learn/react-compiler/installation

LANGUAGE: javascript
CODE:
```
module.exports = {  
  plugins: [  
    'babel-plugin-react-compiler', // must run first!  
    // ... other plugins  
  ],  
  // ... other config  
};
```

--------------------------------

TITLE: Replace `ReactDOMTestUtils.renderIntoDocument` with `@testing-library/react` `render`
DESCRIPTION: This snippet illustrates the migration from `renderIntoDocument` to `render` provided by `@testing-library/react`. `render` offers a more robust and user-centric approach to rendering components in tests, focusing on accessibility and querying the DOM as a user would. It provides additional utilities for interacting with the rendered component.

SOURCE: https://react.dev/warnings/react-dom-test-utils

LANGUAGE: javascript
CODE:
```
import {renderIntoDocument} from 'react-dom/test-utils';

renderIntoDocument(<Component />);
```

LANGUAGE: javascript
CODE:
```
import {render} from '@testing-library/react';

render(<Component />);
```

--------------------------------

TITLE: Render Lists of Items using Array map() in React
DESCRIPTION: This snippet demonstrates how to use the `map()` function to transform an array of data (`products`) into an array of JSX `<li>` elements. Each `<li>` is assigned a unique `key` attribute, which is crucial for React's reconciliation process.

SOURCE: https://react.dev/learn

LANGUAGE: javascript
CODE:
```
const listItems = products.map(product =>
  <li key={product.id}>
    {product.title}
  </li>
);


return (
  <ul>{listItems}</ul>
);
```

--------------------------------

TITLE: Define Product Data Array for List Rendering in React
DESCRIPTION: This code defines a simple array of product objects, each with a `title` and a unique `id`. This array serves as the data source for rendering lists of items in a React component.

SOURCE: https://react.dev/learn

LANGUAGE: javascript
CODE:
```
const products = [
  { title: 'Cabbage', id: 1 },
  { title: 'Garlic', id: 2 },
  { title: 'Apple', id: 3 },
];
```

--------------------------------

TITLE: Configure React Compiler with React Router and Vite
DESCRIPTION: Integrates `babel-plugin-react-compiler` into a React Router project using Vite. This setup leverages `vite-plugin-babel` to apply the compiler plugin, with optional TypeScript presets and a custom `ReactCompilerConfig`.

SOURCE: https://react.dev/learn/react-compiler/installation

LANGUAGE: javascript
CODE:
```
// vite.config.js  
import { defineConfig } from "vite";  
import babel from "vite-plugin-babel";  
import { reactRouter } from "@react-router/dev/vite";  
  
const ReactCompilerConfig = { /* ... */ };  
  
export default defineConfig({  
  plugins: [  
    reactRouter(),  
    babel({  
      filter: /\.[jt]sx?$/,  
      babelConfig: {  
        presets: ["@babel/preset-typescript"], // if you use TypeScript  
        plugins: [  
          ["babel-plugin-react-compiler", ReactCompilerConfig],  
        ],  
      },  
    }),  
  ],  
});
```

--------------------------------

TITLE: Implement Progressive Enhancement with React useActionState Permalink
DESCRIPTION: This example illustrates how to enable progressive enhancement using `useActionState` by providing a permalink as the third argument. If the form is submitted before the JavaScript bundle loads, React will redirect to the specified URL, ensuring basic functionality even without JavaScript.

SOURCE: https://react.dev/reference/rsc/server-actions

LANGUAGE: jsx
CODE:
```
"use client";

import {updateName} from './actions';

function UpdateName() {
  const [, submitAction] = useActionState(updateName, null, `/name/update`);


  return (
    <form action={submitAction}>
      ...
    </form>
  );
}
```

--------------------------------

TITLE: Import useState Hook in React
DESCRIPTION: This line of code demonstrates the standard way to import the `useState` hook from the React library. The `useState` hook is essential for adding stateful logic to functional components.

SOURCE: https://react.dev/learn

LANGUAGE: javascript
CODE:
```
import { useState } from 'react';
```

--------------------------------

TITLE: Configure React Compiler in Vite with vite-plugin-babel
DESCRIPTION: Configures `babel-plugin-react-compiler` in Vite by using `vite-plugin-babel` in `vite.config.js`. This approach allows for a dedicated Babel configuration for the compiler plugin, separate from `@vitejs/plugin-react`'s internal Babel setup.

SOURCE: https://react.dev/learn/react-compiler/installation

LANGUAGE: javascript
CODE:
```
// vite.config.js  
import babel from 'vite-plugin-babel';  
import { defineConfig } from 'vite';  
import react from '@vitejs/plugin-react';  
  
export default defineConfig({  
  plugins: [  
    react(),  
    babel({  
      babelConfig: {  
        plugins: ['babel-plugin-react-compiler'],  
      },  
    }),  
  ],
});
```

--------------------------------

TITLE: Configure React Compiler in Vite with vite-plugin-react
DESCRIPTION: Integrates `babel-plugin-react-compiler` into a Vite project by passing it through the `babel` option of `@vitejs/plugin-react` within `vite.config.js`. This method is suitable for projects already utilizing `vite-plugin-react` for React support.

SOURCE: https://react.dev/learn/react-compiler/installation

LANGUAGE: javascript
CODE:
```
// vite.config.js  
import { defineConfig } from 'vite';  
import react from '@vitejs/plugin-react';  
  
export default defineConfig({  
  plugins: [  
    react({  
      babel: {  
        plugins: ['babel-plugin-react-compiler'],  
      },  
    }),  
  ],  
});
```

--------------------------------

TITLE: Complete Component for Styling and Rendering a List in React
DESCRIPTION: This full React component (`ShoppingList`) demonstrates creating and rendering a dynamic list with conditional styling. It maps over a `products` array, applying a magenta color to fruits and darkgreen to others, showcasing the use of `key` props and inline styles.

SOURCE: https://react.dev/learn

LANGUAGE: javascript
CODE:
```
const products = [
  { title: 'Cabbage', isFruit: false, id: 1 },
  { title: 'Garlic', isFruit: false, id: 2 },
  { title: 'Apple', isFruit: true, id: 3 },
];

export default function ShoppingList() {
  const listItems = products.map(product =>
    <li
      key={product.id}
      style={{
        color: product.isFruit ? 'magenta' : 'darkgreen'
      }}
    >
      {product.title}
    </li>
  );

  return (
    <ul>{listItems}</ul>
  );
}
```

--------------------------------

TITLE: Conditionally Render JSX with Logical AND (&&) in React
DESCRIPTION: This snippet illustrates using the logical `&&` operator for conditional rendering when an `else` branch is not required. If `isLoggedIn` is true, `AdminPanel` is rendered; otherwise, nothing is rendered.

SOURCE: https://react.dev/learn

LANGUAGE: javascript
CODE:
```
<div>
  {isLoggedIn && <AdminPanel />}
</div>
```

--------------------------------

TITLE: React: Complete Application with Lifted State (App.js)
DESCRIPTION: This comprehensive React code snippet combines `MyApp` and `MyButton` to illustrate the full 'lifting state up' pattern. `MyApp` manages the shared `count` state and `handleClick` function, passing them down as props. `MyButton` consumes these props, resulting in a synchronized counter across multiple buttons.

SOURCE: https://react.dev/learn

LANGUAGE: javascript
CODE:
```
import { useState } from 'react';

export default function MyApp() {
  const [count, setCount] = useState(0);

  function handleClick() {
    setCount(count + 1);
  }

  return (
    <div>
      <h1>Counters that update together</h1>
      <MyButton count={count} onClick={handleClick} />
      <MyButton count={count} onClick={handleClick} />
    </div>
  );
}

function MyButton({ count, onClick }) {
  return (
    <button onClick={onClick}>
      Clicked {count} times
    </button>
  );
}
```

--------------------------------

TITLE: Correct React Compiler Configuration for Troubleshooting (ESLint)
DESCRIPTION: This example provides a corrected and valid configuration for `babel-plugin-react-compiler`, demonstrating proper option usage for `compilationMode` and `panicThreshold`. It guides users in rectifying common troubleshooting issues by showing a functional setup.

SOURCE: https://react.dev/reference/eslint-plugin-react-hooks/lints/config

LANGUAGE: javascript
CODE:
```
// ✅ Better: Valid configuration  
module.exports = {  
  plugins: [  
    ['babel-plugin-react-compiler', {  
      compilationMode: 'all', // or 'infer'  
      panicThreshold: 'none', // or 'critical_errors', 'all_errors'  
      // Only use documented options  
    }]  
  ]  
};
```

--------------------------------

TITLE: Update and Display State in React Component
DESCRIPTION: This React component demonstrates how to update a state variable (`count`) in response to an event and display its current value. Clicking the button increments the `count` using `setCount(count + 1)`, causing the component to re-render with the new value.

SOURCE: https://react.dev/learn

LANGUAGE: javascript
CODE:
```
function MyButton() {
  const [count, setCount] = useState(0);


  function handleClick() {
    setCount(count + 1);
  }


  return (
    <button onClick={handleClick}>
      Clicked {count} times
    </button>
  );
}
```

--------------------------------

TITLE: Opt Out React Component from Compiler Optimization in JavaScript
DESCRIPTION: This JavaScript snippet illustrates how to temporarily opt out a specific React component from being optimized by the React Compiler. By including the "use no memo" directive at the top of a component's function body, you instruct the compiler to skip optimization for that component, which can be useful for troubleshooting issues arising from compilation.

SOURCE: https://react.dev/learn/react-compiler/installation

LANGUAGE: javascript
CODE:
```
function ProblematicComponent() {  

  "use no memo";  

  // Component code here  

}
```

--------------------------------

TITLE: Declare State Variable with useState in React
DESCRIPTION: This snippet shows how to declare a state variable (`count`) and its corresponding setter function (`setCount`) using the `useState` hook. The initial value for `count` is set to `0`.

SOURCE: https://react.dev/learn

LANGUAGE: javascript
CODE:
```
function MyButton() {
  const [count, setCount] = useState(0);
  // ...
```

--------------------------------

TITLE: Set dynamic attributes in React JSX using JavaScript variables
DESCRIPTION: This JavaScript code demonstrates how to set dynamic attribute values in JSX, such as `src`, by using curly braces `{}` to reference JavaScript variables like `user.imageUrl`. This enables components to render images or other elements with variable properties.

SOURCE: https://react.dev/learn

LANGUAGE: javascript
CODE:
```
return (
  <img
    className="avatar"
    src={user.imageUrl}
  />
);
```

--------------------------------

TITLE: Conditionally Render JSX with if/else in React
DESCRIPTION: This snippet demonstrates how to conditionally render different JSX components based on a boolean condition (`isLoggedIn`) using a standard JavaScript `if...else` statement. It assigns the appropriate component to a variable which is then rendered.

SOURCE: https://react.dev/learn

LANGUAGE: javascript
CODE:
```
let content;

if (isLoggedIn) {
  content = <AdminPanel />;
} else {
  content = <LoginForm />;
}

return (
  <div>
    {content}
  </div>
);
```

--------------------------------

TITLE: Create a simple React functional component in JavaScript
DESCRIPTION: This JavaScript code defines a basic functional React component named `MyButton`. It returns JSX markup, specifically a button element, demonstrating the fundamental structure of a reusable UI piece in React.

SOURCE: https://react.dev/learn

LANGUAGE: javascript
CODE:
```
function MyButton() {
  return (
    <button>I'm a button</button>
  );
}
```

--------------------------------

TITLE: Conditionally Render JSX with Ternary Operator in React
DESCRIPTION: This example shows how to use the JavaScript ternary operator (`condition ? true_value : false_value`) for more compact conditional rendering directly within JSX. It renders `AdminPanel` if `isLoggedIn` is true, otherwise `LoginForm`.

SOURCE: https://react.dev/learn

LANGUAGE: javascript
CODE:
```
<div>
  {isLoggedIn ? (
    <AdminPanel />
  ) : (
    <LoginForm />
  )}
</div>
```

--------------------------------

TITLE: Return multiple JSX elements using a Fragment in React
DESCRIPTION: This JavaScript snippet demonstrates how to return multiple top-level JSX elements from a React component by wrapping them in an empty `<>...</>` fragment. This technique satisfies JSX's requirement that a component must return a single root element without adding unnecessary DOM nodes like a `<div>`.

SOURCE: https://react.dev/learn

LANGUAGE: javascript
CODE:
```
function AboutPage() {
  return (
    <>
      <h1>About</h1>
      <p>Hello there.<br />How do you do?</p>
    </>
  );
}
```

--------------------------------

TITLE: React: Parent Component Passing Shared State and Handler as Props
DESCRIPTION: This `MyApp` component demonstrates how to pass shared state (`count`) and an event handler (`handleClick`) down to child `MyButton` components as props. This is the 'lifting state up' pattern, where the parent manages the state and provides it to children for synchronized updates.

SOURCE: https://react.dev/learn

LANGUAGE: javascript
CODE:
```
export default function MyApp() {  
  const [count, setCount] = useState(0);  
  
  function handleClick() {  
    setCount(count + 1);  
  }  
  
  return (  
    <div>  
      <h1>Counters that update together</h1>  
      <MyButton count={count} onClick={handleClick} />  
      <MyButton count={count} onClick={handleClick} />  
    </div>  
  );  
}
```

--------------------------------

TITLE: Flatten Travel Plan Data Structure for Easier Updates (JavaScript)
DESCRIPTION: This JavaScript snippet demonstrates a restructured, flattened format for the `initialTravelPlan` data. Instead of deeply nested `childPlaces` arrays, each place now stores an array of `childIds`, and the overall plan becomes a map from IDs to place objects. This approach simplifies state updates by reducing the need to copy entire parent chains for deep modifications, making it easier to manage complex UIs.

SOURCE: https://react.dev/learn/choosing-the-state-structure

LANGUAGE: javascript
CODE:
```
export const initialTravelPlan = {
  0: {
    id: 0,
    title: '(Root)',
    childIds: [1, 42, 46]
  },
  1: {
    id: 1,
    title: 'Earth',
    childIds: [2, 10, 19, 26, 34]
  },
  2: {
    id: 2,
    title: 'Africa',
```

--------------------------------

TITLE: Embed JavaScript variables in React JSX for data display
DESCRIPTION: This JavaScript example illustrates how to display dynamic data in React by embedding a JavaScript variable, `user.name`, directly into JSX using curly braces `{}`. This allows components to render data from their state or props.

SOURCE: https://react.dev/learn

LANGUAGE: javascript
CODE:
```
return (
  <h1>
    {user.name}
  </h1>
);
```

--------------------------------

TITLE: Install React Compiler RC (Babel plugin)
DESCRIPTION: Instructions to install the React Compiler Release Candidate as a Babel plugin using npm, pnpm, or yarn. This package enables the compiler for build-time optimization, compatible with React 17 and up.

SOURCE: https://react.dev/blog/2025/04/21/react-compiler-rc

LANGUAGE: npm
CODE:
```
npm install --save-dev --save-exact babel-plugin-react-compiler@rc
```

LANGUAGE: pnpm
CODE:
```
pnpm add --save-dev --save-exact babel-plugin-react-compiler@rc
```

LANGUAGE: yarn
CODE:
```
yarn add --dev --exact babel-plugin-react-compiler@rc
```

--------------------------------

TITLE: Recommended Production Configuration for React Compiler `panicThreshold`
DESCRIPTION: This snippet demonstrates the recommended configuration for `panicThreshold` in production environments, explicitly setting its value to `'none'`. This ensures build stability, allowing the React Compiler to skip unoptimizable components without causing build failures, and maximizing component optimization.

SOURCE: https://react.dev/reference/react-compiler/panicThreshold

LANGUAGE: javascript
CODE:
```
{  
  panicThreshold: 'none'  
}
```

--------------------------------

TITLE: Illustrate React List Item Updates (HTML/JSX)
DESCRIPTION: These HTML/JSX snippets demonstrate a list of items before and after an update. This scenario highlights how list content can change by reordering, adding new items, and modifying existing ones, emphasizing the need for unique `key` props in React to manage component identity during such transformations.

SOURCE: https://react.dev/learn/tutorial-tic-tac-toe

LANGUAGE: html
CODE:
```
<li>Alexa: 7 tasks left</li>  

<li>Ben: 5 tasks left</li>
```

LANGUAGE: html
CODE:
```
<li>Ben: 9 tasks left</li>  

<li>Claudia: 8 tasks left</li>  

<li>Alexa: 5 tasks left</li>
```

--------------------------------

TITLE: Complete example of creating and nesting React components in JavaScript
DESCRIPTION: This consolidated JavaScript code provides a full example of both defining a reusable `MyButton` component and then nesting it within an `MyApp` component. It illustrates the complete pattern for structuring simple React applications with multiple components in a single file.

SOURCE: https://react.dev/learn

LANGUAGE: javascript
CODE:
```
function MyButton() {
  return (
    <button>
      I'm a button
    </button>
  );
}

export default function MyApp() {
  return (
    <div>
      <h1>Welcome to my app</h1>
      <MyButton />
    </div>
  );
}
```

--------------------------------

TITLE: Handle Click Events in React Components
DESCRIPTION: This example shows how to define an event handler function (`handleClick`) within a React component (`MyButton`) and attach it to a button's `onClick` prop. The handler triggers an alert when the button is clicked, demonstrating basic event response.

SOURCE: https://react.dev/learn

LANGUAGE: javascript
CODE:
```
function MyButton() {
  function handleClick() {
    alert('You clicked me!');
  }


  return (
    <button onClick={handleClick}>
      Click me
    </button>
  );
}
```