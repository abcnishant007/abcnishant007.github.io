---
layout: single
title: "Software"
permalink: /software/
author_profile: true
---

My open-source projects often come from practical research workflow friction: if a repetitive task slows me down, I try to turn the fix into a reusable tool.

<section class="software-activity-card">
  <div class="software-activity-copy">
    <p class="software-activity-eyebrow">GitHub activity</p>
    <h2>Recent contribution graph</h2>
    <p class="software-activity-summary" id="github-contrib-summary">Loading latest activity from GitHub.</p>
  </div>
  <div class="software-activity-graph-wrap">
    <div class="software-activity-months" id="github-contrib-months" aria-hidden="true"></div>
    <div class="software-activity-grid" id="github-contrib-graph" aria-label="GitHub contribution graph"></div>
  </div>
  <noscript>
    <p><a href="https://github.com/abcnishant007">View GitHub activity on GitHub</a></p>
  </noscript>
</section>

<style>
  .software-activity-card {
    margin: 1.5rem 0 2rem;
    padding: 1.25rem 1.25rem 1.4rem;
    border: 1px solid #d7e3d4;
    border-radius: 16px;
    background:
      radial-gradient(circle at top right, rgba(67, 160, 71, 0.12), transparent 28%),
      linear-gradient(180deg, #fbfdf9 0%, #f4f8f2 100%);
  }

  .software-activity-eyebrow {
    margin: 0;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #2f6f3e;
  }

  .software-activity-card h2 {
    margin: 0.2rem 0 0.3rem;
    font-size: 1.3rem;
  }

  .software-activity-summary {
    margin: 0 0 1rem;
    color: #4d5b50;
  }

  .software-activity-graph-wrap {
    overflow-x: auto;
    padding-bottom: 0.2rem;
  }

  .software-activity-months {
    display: grid;
    grid-template-columns: repeat(53, 11px);
    column-gap: 3px;
    margin: 0 0 0.35rem 16px;
    min-width: max-content;
    font-size: 0.68rem;
    color: #6c776e;
  }

  .software-activity-grid {
    display: grid;
    grid-template-columns: 14px repeat(53, 11px);
    grid-template-rows: repeat(7, 11px);
    gap: 3px;
    align-items: center;
    min-width: max-content;
  }

  .software-activity-day-label {
    font-size: 0.68rem;
    color: #6c776e;
    text-align: right;
    padding-right: 0.15rem;
  }

  .software-activity-day-label.is-empty {
    visibility: hidden;
  }

  .software-activity-cell {
    width: 11px;
    height: 11px;
    border-radius: 2px;
    background: #ebedf0;
  }

  @media (max-width: 640px) {
    .software-activity-card {
      padding: 1rem 0.9rem 1.15rem;
    }
  }
</style>

<script>
  (function () {
    const username = "abcnishant007";
    const endpoint = "{{ '/assets/data/github-contributions.json' | relative_url }}";
    const graph = document.getElementById("github-contrib-graph");
    const months = document.getElementById("github-contrib-months");
    const summary = document.getElementById("github-contrib-summary");

    if (!graph || !months || !summary) return;

    const dayLabels = ["", "Mon", "", "Wed", "", "Fri", ""];
    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

    function isoDate(date) {
      return date.toISOString().slice(0, 10);
    }

    function startOfWeek(date) {
      const clone = new Date(date);
      clone.setDate(clone.getDate() - clone.getDay());
      return clone;
    }

    function buildGrid(contributions) {
      const byDate = new Map(contributions.map((item) => [item.date, item]));
      const today = new Date();
      today.setHours(0, 0, 0, 0);

      const end = new Date(today);
      const start = startOfWeek(new Date(today));
      start.setDate(start.getDate() - (52 * 7));

      const weeks = [];
      let cursor = new Date(start);
      while (cursor <= end) {
        const week = [];
        for (let i = 0; i < 7; i += 1) {
          const key = isoDate(cursor);
          week.push(byDate.get(key) || { date: key, count: 0, color: "#ebedf0" });
          cursor.setDate(cursor.getDate() + 1);
        }
        weeks.push(week);
      }

      return weeks;
    }

    function renderMonths(weeks) {
      months.innerHTML = "";
      let previousMonth = null;

      weeks.forEach((week) => {
        const monthLabel = document.createElement("span");
        const firstDay = new Date(week[0].date + "T00:00:00");
        const month = firstDay.getMonth();
        monthLabel.textContent = month !== previousMonth ? monthNames[month] : "";
        previousMonth = month;
        months.appendChild(monthLabel);
      });
    }

    function renderGraph(weeks) {
      graph.innerHTML = "";

      dayLabels.forEach((label) => {
        const day = document.createElement("div");
        day.className = "software-activity-day-label" + (label ? "" : " is-empty");
        day.textContent = label;
        graph.appendChild(day);
      });

      for (let row = 0; row < 7; row += 1) {
        weeks.forEach((week) => {
          const item = week[row];
          const cell = document.createElement("div");
          const readableDate = new Date(item.date + "T00:00:00").toLocaleDateString(undefined, {
            year: "numeric",
            month: "short",
            day: "numeric"
          });
          const hasVisibleActivity = (item.color || "#ebedf0").toLowerCase() !== "#ebedf0";
          const tooltip = item.count > 0
            ? item.count + " contributions on " + readableDate
            : hasVisibleActivity
              ? "GitHub activity on " + readableDate
              : "No recorded contributions on " + readableDate;
          cell.className = "software-activity-cell";
          cell.style.backgroundColor = item.color || "#ebedf0";
          cell.title = tooltip;
          graph.appendChild(cell);
        });
      }
    }

    fetch(endpoint)
      .then((response) => {
        if (!response.ok) throw new Error("Failed to fetch contributions");
        return response.json();
      })
      .then((data) => {
        const contributions = Array.isArray(data.contributions) ? data.contributions : [];
        if (!contributions.length) throw new Error("No contributions returned");

        const weeks = buildGrid(contributions);
        const thisYear = data.summary && data.summary.year ? data.summary.year : String(new Date().getFullYear());
        const total = data.summary && typeof data.summary.total === "number"
          ? data.summary.total
          : contributions.reduce((sum, item) => sum + item.count, 0);

        summary.textContent = total + " contributions so far in " + thisYear + ".";
        renderMonths(weeks);
        renderGraph(weeks);
      })
      .catch(() => {
        summary.innerHTML = 'Contribution graph will appear after the weekly data refresh. <a href="https://github.com/' + username + '">View activity on GitHub</a>.';
      });
  })();
</script>

Selected projects
======
* [**smartprint**](https://github.com/abcnishant007/smartprint): lightweight Python debugging utility for readable variable-name/value printing.  
  PyPI: [smartprint](https://pypi.org/project/smartprint/) (46.5K+ downloads).
* [**meaningful-pdf-names**](https://pypi.org/project/meaningful-pdf-names/): offline-friendly CLI that renames messy PDF files into compact, searchable, keyword-rich filenames using text extracted from the first pages. Supports single files, folders, dry runs, and an optional local summarizer.  
  PyPI: [meaningful-pdf-names](https://pypi.org/project/meaningful-pdf-names/) (3.4K+ downloads). Also on piwheels: [meaningful-pdf-names](https://www.piwheels.org/project/meaningful-pdf-names/).
* [**LitSearch**](https://github.com/abcnishant007/LitSearch): Flask-based PDF search and paragraph-ranking app for faster literature review.
* [**cleanlatex**](https://cleanlatex.neocities.org): browser utility for cleaning LaTeX and BibTeX files.

Open-source contributions
======
* [trackintel](https://github.com/mie-lab/trackintel)
* [simmobility-prod](https://github.com/smart-fm/simmobility-prod)
* [Matplotlib](https://github.com/matplotlib/matplotlib)

Language and tooling
======
I mainly work in Python for modelling, data workflows, and research software. I also use C/C++, MATLAB, SQL, and shell scripting.

Community
======
* Stack Overflow profile: [lifezbeautiful](https://stackoverflow.com/users/3896008/lifezbeautiful)
* GitHub profile: [abcnishant007](https://github.com/abcnishant007)
