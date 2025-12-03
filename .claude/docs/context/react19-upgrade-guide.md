# React 19 Upgrade Guide

## Automated Migration

**Execute React 19 migration codemods**
Runs codemod tool with React 19 migration recipe, automatically updating code to new APIs and patterns
```bash
npx codemod@latest react/19/migration-recipe
```

**Migrate ReactDOM.render to createRoot**
```bash
npx codemod@latest react/19/replace-reactdom-render
```

**Migrate act import**
```bash
npx codemod@latest react/19/replace-act-import
```

**Migrate string refs to ref callbacks**
```bash
npx codemod@latest react/19/replace-string-ref
```

**Migrate PropTypes to TypeScript**
```bash
npx codemod@latest react/prop-types-typescript
```

**Migrate element.props TypeScript access**
```bash
npx types-react-codemod@latest react-element-default-any-props ./path-to-your-react-ts-files
```

**Migrate React 19 TypeScript types**
```bash
npx types-react-codemod@latest preset-19 ./path-to-app
```

## Installation

**Install React 19 core libraries**
```bash
npm install --save-exact react@^19.0.0 react-dom@^19.0.0
yarn add --exact react@^19.0.0 react-dom@^19.0.0
```

**Install TypeScript type definitions**
```bash
npm install --save-exact @types/react@^19.0.0 @types/react-dom@^19.0.0
yarn add --exact @types/react@^19.0.0 @types/react-dom@^19.0.0
```

**Install React 18**
```bash
npm install react react-dom
yarn add react react-dom
```

## API Migrations

**ReactDOM.render → createRoot**
```javascript
// Before
import {render} from 'react-dom';
render(<App />, document.getElementById('root'));

// After
import {createRoot} from 'react-dom/client';
const root = createRoot(document.getElementById('root'));
root.render(<App />);
```

**ReactDOM.hydrate → hydrateRoot**
```javascript
// Before
import {hydrate} from 'react-dom';
hydrate(<App />, document.getElementById('root'));

// After
import {hydrateRoot} from 'react-dom/client';
hydrateRoot(document.getElementById('root'), <App />);
```

**unmountComponentAtNode → root.unmount()**
```javascript
// Before
unmountComponentAtNode(document.getElementById('root'));

// After
root.unmount();
```

**ReactDOM.findDOMNode → useRef**
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

**React.createFactory → JSX**
```javascript
// Before
import { createFactory } from 'react';
const button = createFactory('button');

// After
const button = <button />;
```

**String refs → ref callbacks**
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

**Module pattern factories → function components**
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

**Legacy Context → new Context API**
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

**PropTypes and defaultProps → TypeScript/ES6**
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

## Testing

**Migrate react-test-renderer/shallow**
```bash
npm install react-shallow-renderer --save-dev
```
```diff
- import ShallowRenderer from 'react-test-renderer/shallow';
+ import ShallowRenderer from 'react-shallow-renderer';
```

**Migrate act import**
```javascript
// Before
import {act} from 'react-dom/test-utils';

// After
import {act} from 'react';
```

**Replace renderIntoDocument with @testing-library/react**
```javascript
// Before
import {renderIntoDocument} from 'react-dom/test-utils';
renderIntoDocument(<Component />);

// After
import {render} from '@testing-library/react';
render(<Component />);
```

**Configure testing environment for act() warnings**
```javascript
// In your test setup file
globalThis.IS_REACT_ACT_ENVIRONMENT = true;
```

## TypeScript Changes

**useRef and createContext require arguments**
```typescript
// @ts-expect-error: Expected 1 argument but saw none
useRef();
// Passes
useRef(undefined);
// @ts-expect-error: Expected 1 argument but saw none
createContext();
// Passes
createContext(undefined);
```

**Mutable useRef current property**
```typescript
const ref = useRef<number>(null);
// Cannot assign to 'current' because it is a read-only property
ref.current = 1;
```

**New RefObject type**
```typescript
interface RefObject<T> {
  current: T
}
declare function useRef<T>: RefObject<T>
```

**Improved useReducer type inference**
```typescript
// Before
- useReducer<React.Reducer<State, Action>>(reducer)
// After
+ useReducer(reducer)

// Annotate external reducer
const reducer = (state: State, action: Action) => state;

// Annotate inline reducer
- useReducer<React.Reducer<State, Action>>((state, action) => state)
+ useReducer((state: State, action: Action) => state)

// Explicit types (edge cases)
- useReducer<React.Reducer<State, Action>>(reducer)
+ useReducer<State, [Action]>(reducer)
```

**ReactElement props type changed to unknown**
```typescript
type Example = ReactElement["props"];
//   ^? Before, was 'any', now 'unknown'

type Example2 = ReactElement<{ id: string }>["props"];
//   ^? { id: string }
```

**Augment JSX namespace in declare module**
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

**Define children prop in interfaces**
```typescript
interface MyButtonProps {
  color: string;
  children?: React.ReactNode;
}
```

## React 18 Features

**Update root API**
```javascript
// Before
import { render } from 'react-dom';
const container = document.getElementById('app');
render(<App tab="home" />, container);

// After
import { createRoot } from 'react-dom/client';
const container = document.getElementById('app');
const root = createRoot(container); // createRoot(container!) if TypeScript
root.render(<App tab="home" />);
```

**Update hydration API**
```javascript
// Before
import { hydrate } from 'react-dom';
const container = document.getElementById('app');
hydrate(<App tab="home" />, container);

// After
import { hydrateRoot } from 'react-dom/client';
const container = document.getElementById('app');
const root = hydrateRoot(container, <App tab="home" />);
// Unlike createRoot, no separate root.render() call needed
```

**Update unmount API**
```javascript
// Before
unmountComponentAtNode(container);

// After
root.unmount();
```

**Handle render callbacks with useEffect**
```javascript
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

**Automatic batching**
```javascript
// React 18: all updates batched
function handleClick() {
  setCount(c => c + 1);
  setFlag(f => !f);
  // React will only re-render once at the end (batching!)
}
setTimeout(() => {
  setCount(c => c + 1);
  setFlag(f => !f);
  // React will only re-render once at the end (batching!)
}, 1000);

// React 17: only React events batched
function handleClick() {
  setCount(c => c + 1);
  setFlag(f => !f);
  // React will only re-render once at the end (batching!)
}
setTimeout(() => {
  setCount(c => c + 1);
  setFlag(f => !f);
  // React will render twice, once for each state update (no batching)
}, 1000);
```

**Opt-out of automatic batching with flushSync**
```javascript
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

## React 19 Specific

**Load via ESM CDN**
```html
<script type="module">
  import React from "https://esm.sh/react@19/?dev"
  import ReactDOMClient from "https://esm.sh/react-dom@19/client?dev"
  ...
</script>
```

**Custom error handling**
```javascript
const root = createRoot(container, {
  onUncaughtError: (error, errorInfo) => {
    // ... log error report
  },
  onCaughtError: (error, errorInfo) => {
    // ... log error report
  }
});
```

## React Compiler

**Install compiler**
```bash
npm install -D babel-plugin-react-compiler@rc
yarn add -D babel-plugin-react-compiler@rc
pnpm install -D babel-plugin-react-compiler@rc
```

**Install ESLint plugin**
```bash
npm install -D eslint-plugin-react-hooks@rc
```

**Configure in Babel**
```javascript
module.exports = {
  plugins: [
    'babel-plugin-react-compiler', // must run first!
    // ... other plugins
  ],
  // ... other config
};
```

**Configure in Vite with vite-plugin-react**
```javascript
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

**Configure in Vite with vite-plugin-babel**
```bash
npm install -D vite-plugin-babel
```
```javascript
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

**Configure with React Router and Vite**
```javascript
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

**Compiler configuration**
```javascript
// Valid configuration
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

**Recommended production config**
```javascript
{
  panicThreshold: 'none'
}
```

**Opt out component from compiler**
```javascript
function ProblematicComponent() {
  "use no memo";
  // Component code here
}
```

**Verify compiler output**
```javascript
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

**Install exact version**
```bash
npm install --save-dev --save-exact babel-plugin-react-compiler@rc
pnpm add --save-dev --save-exact babel-plugin-react-compiler@rc
yarn add --dev --exact babel-plugin-react-compiler@rc
```

## React Basics Reference

**Import useState**
```javascript
import { useState } from 'react';
```

**Create functional component**
```javascript
function MyButton() {
  return (
    <button>I'm a button</button>
  );
}
```

**Nest components**
```javascript
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

**Use fragments**
```javascript
function AboutPage() {
  return (
    <>
      <h1>About</h1>
      <p>Hello there.<br />How do you do?</p>
    </>
  );
}
```

**Embed variables in JSX**
```javascript
return (
  <h1>
    {user.name}
  </h1>
);
```

**Set dynamic attributes**
```javascript
return (
  <img
    className="avatar"
    src={user.imageUrl}
  />
);
```

**Conditional rendering - if/else**
```javascript
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

**Conditional rendering - ternary**
```javascript
<div>
  {isLoggedIn ? (
    <AdminPanel />
  ) : (
    <LoginForm />
  )}
</div>
```

**Conditional rendering - logical AND**
```javascript
<div>
  {isLoggedIn && <AdminPanel />}
</div>
```

**Render lists**
```javascript
const products = [
  { title: 'Cabbage', id: 1 },
  { title: 'Garlic', id: 2 },
  { title: 'Apple', id: 3 },
];

const listItems = products.map(product =>
  <li key={product.id}>
    {product.title}
  </li>
);

return (
  <ul>{listItems}</ul>
);
```

**Render lists with conditional styling**
```javascript
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

**Handle click events**
```javascript
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

**Declare state**
```javascript
function MyButton() {
  const [count, setCount] = useState(0);
  // ...
}
```

**Update and display state**
```javascript
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

**Lift state up**
```javascript
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

**Flatten data structures for easier updates**
```javascript
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
    // ...
  }
};
```

**List item updates**
```html
<!-- Before -->
<li>Alexa: 7 tasks left</li>
<li>Ben: 5 tasks left</li>

<!-- After -->
<li>Ben: 9 tasks left</li>
<li>Claudia: 8 tasks left</li>
<li>Alexa: 5 tasks left</li>
```

**Progressive enhancement with useActionState**
```jsx
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
