PY_TRACT_VERSION=$(cat tract_python/__init__.py|grep 'TRACT_VERSION'|awk '{print $3}')
CARGO_TRACT_VERSION=$(cat Cargo.toml|grep 'tract-nnef'|awk '{print $3}')

if [ "$PY_TRACT_VERSION" = "$CARGO_TRACT_VERSION" ]; then
    echo "Tract version in sync: "$PY_TRACT_VERSION
    exit 0
else
    echo "Tract version between python lib and Cargo toml are inconsistent"
    exit 1
fi
