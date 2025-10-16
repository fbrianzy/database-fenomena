
# DASHFENA — BPS Sidoarjo Phenomena Dashboard

Dashfena is an interactive web dashboard system designed to visualize
and summarize economic, social, and development phenomena curated by
the BPS (Statistics Office) of Sidoarjo, Indonesia.

Built using Flask (Python) and directly integrated with a GitHub repository
as the main data source (CSV-based). The system helps streamline analysis,
monitoring, and internal reporting through an intuitive web interface.

### Key objectives:
- Present real-world news phenomena in a structured, data-driven way.
- Enable efficient monitoring of economic trends across multiple sectors.
- Simplify internal reporting and publication processes via an admin panel.

## CORE FEATURES 

1. Real-Time GitHub Synchronization
   - Reads CSV files from the `database-fenomena` repository.
   - Automatically displays the latest synchronization timestamp.
2. Analytical Dashboard
   - Monthly and categorical trend visualization.
   - Growth and sentiment indicators compared to previous months.
3. Modern Admin Panel
   - CSV-based CRUD operations (create, update, delete entries).
   - Direct CSV upload and auto-refresh on dashboard update.
4. Responsive UI/UX
   - Built with Tailwind CSS 3 + Font Awesome 6.
   - Clean, mobile-first design with smooth animations (no “blink” effects).
5. Security & Stability
   - CSRF validation across host variations (127.0.0.1 / LAN IP).
   - Unique session management per domain.
   - Suspicious request logging and input sanitization.
