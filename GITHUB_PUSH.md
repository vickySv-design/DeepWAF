# Push DeepWAF to GitHub

## Quick Commands to Push to Your Repository

Open Command Prompt or Terminal in the `Advanced-WAF-WAFinity-main` folder and run these commands:

```bash
# Step 1: Initialize Git repository
git init

# Step 2: Add all files
git add .

# Step 3: Commit files
git commit -m "DeepWAF: Character-Level CNN Web Application Firewall - Final Year Project"

# Step 4: Add your GitHub repository as remote
git remote add origin https://github.com/vickySv-design/DeepWAF.git

# Step 5: Rename branch to main (if needed)
git branch -M main

# Step 6: Push to GitHub
git push -u origin main
```

---

## If You Get Authentication Error:

### Option 1: Use Personal Access Token (Recommended)

1. Go to GitHub: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: "DeepWAF Push"
4. Select scopes: Check "repo" (full control)
5. Click "Generate token"
6. **COPY THE TOKEN** (you won't see it again!)

7. When pushing, use:
```bash
git push -u origin main
```
- Username: `vickySv-design`
- Password: `paste_your_token_here`

### Option 2: Use GitHub Desktop (Easiest)

1. Download GitHub Desktop: https://desktop.github.com/
2. Install and login with your GitHub account
3. Click "Add" → "Add existing repository"
4. Select `Advanced-WAF-WAFinity-main` folder
5. Click "Publish repository"
6. Repository name: `DeepWAF`
7. Click "Publish repository"

---

## If Repository Already Exists on GitHub:

If you already created the repository on GitHub, run:

```bash
git init
git add .
git commit -m "Initial commit - DeepWAF Final Year Project"
git remote add origin https://github.com/vickySv-design/DeepWAF.git
git branch -M main
git push -u origin main --force
```

---

## Verify Push Success:

After pushing, visit: https://github.com/vickySv-design/DeepWAF

You should see all your files there!

---

## Common Issues:

### Issue 1: "fatal: remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/vickySv-design/DeepWAF.git
git push -u origin main
```

### Issue 2: "Updates were rejected"
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Issue 3: "Permission denied"
- Use Personal Access Token instead of password
- Or use GitHub Desktop

---

## After Successful Push:

Your repository will be live at:
**https://github.com/vickySv-design/DeepWAF**

Then you can deploy to Render! 🚀
