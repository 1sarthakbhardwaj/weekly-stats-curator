# 🔍 Google Search Console API Setup Guide (FREE - 15 minutes)

Google Search Console API is **completely free** and gives you search performance data for your website!

## Prerequisites

- You must have a verified website in Google Search Console
- Admin access to the website
- If you don't have GSC set up yet, visit [search.google.com/search-console](https://search.google.com/search-console) first

## Step 1: Create Google Cloud Project (3 minutes)

**If you already created a project for YouTube, skip to Step 2!**

1. Go to [Google Cloud Console](https://console.developers.google.com/)
2. Sign in with your Google account
3. Click **"Select a project"** dropdown at the top
4. Click **"NEW PROJECT"** (or use existing project)
5. Enter project name: `social-media-stats`
6. Click **"CREATE"**

## Step 2: Enable Search Console API (2 minutes)

1. In the left sidebar, click **"APIs & Services"** > **"Library"**
2. Search for: `Google Search Console API`
3. Click on **"Google Search Console API"**
4. Click the blue **"ENABLE"** button
5. Wait for it to enable (~5 seconds)

## Step 3: Create Service Account (5 minutes)

Service accounts are used for server-to-server authentication.

1. Click **"APIs & Services"** > **"Credentials"**
2. Click **"+ CREATE CREDENTIALS"**
3. Select **"Service account"**
4. Fill in details:
   - **Service account name**: `gsc-stats-reader`
   - **Service account ID**: (auto-filled)
   - **Description**: "Read Google Search Console stats"
5. Click **"CREATE AND CONTINUE"**
6. **Role**: Select **"Service Account User"** 
7. Click **"CONTINUE"**
8. Click **"DONE"**

## Step 4: Create Service Account Key (2 minutes)

1. Find your new service account in the list
2. Click on the **email address** (looks like `gsc-stats-reader@...`)
3. Go to the **"KEYS"** tab
4. Click **"ADD KEY"** > **"Create new key"**
5. Select **"JSON"**
6. Click **"CREATE"**
7. A JSON file will be downloaded to your computer
8. **Save this file securely!** (e.g., `gsc-credentials.json`)

## Step 5: Grant Service Account Access to Search Console (3 minutes)

1. Open the downloaded JSON file
2. Find the `"client_email"` field (looks like: `gsc-stats-reader@...iam.gserviceaccount.com`)
3. **COPY this email address**

4. Go to [Google Search Console](https://search.google.com/search-console)
5. Select your property (website)
6. Click **"Settings"** (gear icon) in the left sidebar
7. Click **"Users and permissions"**
8. Click **"ADD USER"**
9. Paste the service account email
10. Permission level: Select **"Full"** (or "Restricted" if you only want read access)
11. Click **"ADD"**

## Step 6: Move Credentials File & Update .env (2 minutes)

### Option A: Move file to project directory (Recommended)

```bash
# Move the downloaded file to your project
mv ~/Downloads/your-project-xxxxx-xxxxxx.json /Users/sarthak/Documents/Labellerr/gsc-credentials.json
```

### Option B: Keep it in a secure location

```bash
# Move to a secure location
mv ~/Downloads/your-project-xxxxx-xxxxxx.json ~/.credentials/gsc-credentials.json
```

### Update .env file:

```bash
# Google Search Console Configuration
GSC_CREDENTIALS_FILE=/Users/sarthak/Documents/Labellerr/gsc-credentials.json
GSC_PROPERTY_URL=https://labellerr.com/
```

**Important**: Use the **exact URL** as shown in Search Console:
- If GSC shows `https://labellerr.com`, use `https://labellerr.com/`
- If GSC shows `sc-domain:labellerr.com`, use `sc-domain:labellerr.com`

## Step 7: Test It! (30 seconds)

```bash
# Stop the server (Ctrl+C if running)
python stats.py
```

Open http://localhost:5050 and you should see Google Search Console stats!

---

## What Stats You'll Get

With GSC API, you'll see:
- ✅ Total clicks from Google Search
- ✅ Total impressions (how many times your site appeared)
- ✅ Click-through rate (CTR %)
- ✅ US-specific clicks
- ✅ Search queries (optional - can be added)

---

## Property URL Formats

Google Search Console has different property types:

| Property Type | Example | Use in .env |
|---------------|---------|-------------|
| URL Prefix | https://labellerr.com | `https://labellerr.com/` |
| Domain Property | labellerr.com | `sc-domain:labellerr.com` |

**How to check**: Go to Search Console, look at the property selector dropdown - use the exact format shown there.

---

## Security Notes

🔐 **Important**: The JSON credentials file contains sensitive information!

1. **Never commit to Git** (already in `.gitignore`)
2. Store in a secure location
3. Don't share the file
4. If compromised, delete the key in Google Cloud Console and create a new one

---

## Troubleshooting

### "No such file or directory"
- Check the file path in `.env` is correct
- Use absolute path: `/Users/sarthak/Documents/Labellerr/gsc-credentials.json`
- Verify file exists: `ls -la gsc-credentials.json`

### "Permission denied"
- Make sure you added the service account email to Search Console
- Check you selected "Full" or "Restricted" permission
- Wait 5 minutes for permissions to propagate

### "Property not found"
- Verify the property URL matches exactly (with or without trailing `/`)
- Check the property format (`https://` vs `sc-domain:`)
- Ensure the property is verified in Search Console

### "403 Forbidden"
- Service account not added to Search Console users
- Re-add the service account email with proper permissions

---

## Cost

**100% FREE!**
- No limits on API calls
- No quotas
- No charges

---

## Example Data You'll See

```
Google Search Console Stats:
- Total Clicks: 15,234
- Impressions: 456,789
- CTR: 3.34%
- US Clicks: 8,123
```

---

## Done! ✅

Once configured, your Google Search Console stats will automatically appear in the dashboard!

---

## Quick Reference

**Files you need:**
- `gsc-credentials.json` (service account key)

**Environment variables:**
```bash
GSC_CREDENTIALS_FILE=/path/to/gsc-credentials.json
GSC_PROPERTY_URL=https://your-domain.com/
```

**Service account email format:**
```
your-project-name@your-project-id.iam.gserviceaccount.com
```

This email needs to be added as a user in Google Search Console!

