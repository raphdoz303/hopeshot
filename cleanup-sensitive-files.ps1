Write-Host "Checking for sensitive files that should be ignored..." -ForegroundColor Yellow

# List of sensitive file patterns to check and remove
$sensitiveFiles = @(
    ".env",
    "backend/.env", 
    ".env.local",
    ".env.development.local",
    ".env.test.local", 
    ".env.production.local"
)

# Check what's currently tracked that shouldn't be
Write-Host "Checking currently tracked files..." -ForegroundColor Cyan

$foundSensitiveFiles = @()

foreach ($pattern in $sensitiveFiles) {
    try {
        $trackedFiles = git ls-files $pattern 2>$null
        if ($trackedFiles) {
            $foundSensitiveFiles += $trackedFiles
            Write-Host "Found tracked sensitive file: $trackedFiles" -ForegroundColor Red
        }
    }
    catch {
        # Ignore errors for patterns that don't match anything
    }
}

if ($foundSensitiveFiles.Count -eq 0) {
    Write-Host "No sensitive files found in Git tracking!" -ForegroundColor Green
    exit 0
}

# Show found files
Write-Host "Found $($foundSensitiveFiles.Count) sensitive file(s) in Git tracking:" -ForegroundColor Red
foreach ($file in $foundSensitiveFiles) {
    Write-Host "  - $file" -ForegroundColor Yellow
}

$confirmation = Read-Host "Do you want to remove these from Git tracking? (y/N)"

if ($confirmation -eq 'y' -or $confirmation -eq 'Y') {
    
    Write-Host "Removing sensitive files from Git tracking..." -ForegroundColor Yellow
    
    # Remove each file from Git tracking
    foreach ($file in $foundSensitiveFiles) {
        Write-Host "Removing: $file" -ForegroundColor Cyan
        git rm --cached $file
    }
    
    # Commit the changes
    Write-Host "Committing removal..." -ForegroundColor Yellow
    git commit -m "Remove sensitive files from Git tracking"
    
    # Show status
    Write-Host "Current Git status:" -ForegroundColor Cyan
    git status --short
    
    Write-Host "Sensitive files removed from Git tracking!" -ForegroundColor Green
    Write-Host "Run 'git push' to update GitHub" -ForegroundColor Yellow
    
    # Optional: Remove from history
    $historyCleanup = Read-Host "Do you want to remove these files from Git history too? This rewrites history! (y/N)"
    
    if ($historyCleanup -eq 'y' -or $historyCleanup -eq 'Y') {
        Write-Host "This may take a while..." -ForegroundColor Yellow
        
        foreach ($file in $foundSensitiveFiles) {
            Write-Host "Removing $file from history..." -ForegroundColor Cyan
            git filter-branch --force --index-filter "git rm --cached --ignore-unmatch $file" --prune-empty --tag-name-filter cat -- --all
        }
        
        Write-Host "Run 'git push origin --force --all' to update GitHub with cleaned history" -ForegroundColor Yellow
        Write-Host "WARNING: This rewrites Git history. Coordinate with team members!" -ForegroundColor Red
    }
    
} else {
    Write-Host "Aborted. Files remain in Git tracking." -ForegroundColor Red
    Write-Host "Remember to change any exposed API keys!" -ForegroundColor Yellow
}

Write-Host "Security Reminder:" -ForegroundColor Magenta
Write-Host "1. Change all exposed API keys immediately" -ForegroundColor White
Write-Host "2. Update your local files with new keys" -ForegroundColor White
Write-Host "3. Test your application with new credentials" -ForegroundColor White