set -e

rm -rf node_modules
rm -rf dist
yarn install
yarn build
python -m build
python3 -m twine upload dist/*
