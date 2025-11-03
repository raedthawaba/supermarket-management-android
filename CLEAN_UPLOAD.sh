#!/bin/bash

# Clean repository upload script
# This script removes all commit history to avoid token issues

echo "🧹 Cleaning repository and starting fresh..."

# Backup essential files
mkdir -p /tmp/clean_files
cp android_supermarket_app.py /tmp/clean_files/
cp main_android_app.py /tmp/clean_files/
cp requirements_android.txt /tmp/clean_files/
cp buildozer_github_actions.spec /tmp/clean_files/
cp -r .github /tmp/clean_files/

# Remove all git history
rm -rf .git

# Reinitialize clean repository
git init
echo "Please enter your name and email for git config:"
read -p "Your Name: " USER_NAME
read -p "Your Email: " USER_EMAIL

git config user.name "$USER_NAME"
git config user.email "$USER_EMAIL"

# Copy files back
cp /tmp/clean_files/* .
cp -r /tmp/clean_files/.github .

# Add and commit
git add .
git commit -m "Initial commit: Clean Android supermarket app"

# Add remote and push
git remote add origin https://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@github.com/raedthawaba/supermarket-management-android.git
git branch -M main
git push -f origin main

echo "✅ Clean upload completed!"