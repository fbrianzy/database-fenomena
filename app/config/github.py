import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GH_OWNER  = os.getenv("GITHUB_OWNER",  "fbrianzy")
GH_REPO   = os.getenv("GITHUB_REPO",   "database-fenomena")
GH_BRANCH = os.getenv("GITHUB_BRANCH", "main")