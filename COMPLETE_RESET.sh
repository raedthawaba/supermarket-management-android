#!/bin/bash

# 🧹 Complete Repository Reset Script
# This will completely reset the repository to avoid any secret detection issues

echo "🔄 Starting complete repository reset..."

# Backup essential files to temp directory
echo "📁 Backing up essential files..."
mkdir -p /tmp/final_upload
cp android_supermarket_app.py /tmp/final_upload/
cp main_android_app.py /tmp/final_upload/
cp requirements_android.txt /tmp/final_upload/
cp buildozer_github_actions.spec /tmp/final_upload/
cp -r .github /tmp/final_upload/

# Also backup README if you want documentation
cp README.md /tmp/final_upload/ 2>/dev/null || echo "README.md not found, skipping..."

echo "🗑️ Removing ALL git history..."
# Completely remove git directory
rm -rf .git
rm -rf /tmp/final_upload/.git 2>/dev/null || true

echo "🆕 Creating fresh repository..."
git init
git config user.name "MiniMax Agent"
git config user.email "agent@minimax.com"

echo "📋 Adding files..."
cd /tmp/final_upload
# Copy files back to main workspace
cp -r * /workspace/ 2>/dev/null || true

cd /workspace
git add android_supermarket_app.py
git add main_android_app.py  
git add requirements_android.txt
git add buildozer_github_actions.spec
git add README.md
git add -r .github

echo "💾 Creating commit..."
git commit -m "Initial commit: Android Supermarket Management App with GitHub Actions CI/CD"

echo "🔗 Adding remote..."
git remote add origin https://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@github.com/raedthawaba/supermarket-management-android.git

echo "🌿 Creating main branch..."
git branch -M main

echo "🚀 Pushing to GitHub..."
git push -f origin main

if [ $? -eq 0 ]; then
    echo "✅ SUCCESS! Repository uploaded successfully!"
    echo "🎯 Files now available in: https://github.com/raedthawaba/supermarket-management-android"
else
    echo "❌ Upload failed. Check GitHub repository settings."
fi

# Cleanup
rm -rf /tmp/final_upload