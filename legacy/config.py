import os

GITHUB_TOKEN   = os.getenv("GITHUB_TOKEN")
GITHUB_REPO    = os.getenv("GITHUB_REPO", "fbrianzy/database-fenomena")
GITHUB_BRANCH  = os.getenv("GITHUB_BRANCH", "main")
GITHUB_DATA_DIR= os.getenv("GITHUB_DATA_DIR", "data")
ADMIN_SECRET   = os.getenv("ADMIN_SECRET", "admin")
assert GITHUB_TOKEN, "GITHUB_TOKEN is required"
