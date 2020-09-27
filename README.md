# prop-test-ts-clj

Property-based testing for tree-sitter-clojure

## Status

Early stage.

## Setup

```
git clone https://github.com/sogaiu/prop-test-ts-clj
cd prop-test-ts-clj
mkdir vendor
cd vendor
git clone https://github.com/sogaiu/tree-sitter-clojure
cd tree-sitter-clojure
npm install
npx tree-sitter generate
npx node-gyp configure
npx node-gyp rebuild
cd ../..
# before doing the following, please consider using pyenv, virtualenv, etc.
pip install -r requirements.txt
```

## Run Tests

```
python prop-test-ts-clj.py
```
