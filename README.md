# prop-test-ts-clj

Property-based testing for tree-sitter-clojure

## Status

Early stage.

## Setup

```
# clone this repository
git clone https://github.com/sogaiu/prop-test-ts-clj
cd prop-test-ts-clj

# prepare tree-sitter-clojure
mkdir vendor
cd vendor
git clone https://github.com/sogaiu/tree-sitter-clojure
cd tree-sitter-clojure
npm install
npx tree-sitter generate
npx node-gyp configure
npx node-gyp rebuild
cd ../..

# install hypothesis, py-tree-sitter, etc.
# N.B. before doing the following, please consider using pyenv, virtualenv, etc.
pip install -r requirements.txt
```

## Run Tests

```
python prop-test-ts-clj.py
```

## Acknowledgments

* DRMacIver and hypothesis maintainers and contributors
* gfredericks and test.check maintainers and contributors
* py-tree-sitter maintainers and contributors
* pyrmont - discussion
