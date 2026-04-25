#!/bin/bash
# Auto-increment version tag

# Get latest tag
LATEST=$(git tag -l --sort=-version:refname | head -1)
echo "Latest tag: $LATEST"

# Extract version numbers
VERSION=${LATEST#v}
MAJOR=$(echo $VERSION | cut -d. -f1)
MINOR=$(echo $VERSION | cut -d. -f2)
PATCH=$(echo $VERSION | cut -d. -f3)

# Increment patch
NEW_PATCH=$((PATCH + 1))
NEW_TAG="v$MAJOR.$MINOR.$NEW_PATCH"

echo "Creating new tag: $NEW_TAG"
git tag $NEW_TAG
git push origin $NEW_TAG

if [ $? -eq 0 ]; then
    echo "✅ $NEW_TAG pushed successfully!"
else
    echo "❌ Failed to push $NEW_TAG"
fi
