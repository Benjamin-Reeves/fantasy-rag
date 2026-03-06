from news_articles.ingestion import NewsArticleIngestion


def main() -> None:
    urls = [
  "https://www.thefantasyfootballers.com/articles/three-fantasy-football-rbs-you-can-trust-in-2019/",
  "https://www.thefantasyfootballers.com/articles/32-shamelessly-bold-predictions-for-the-2019-fantasy-football-season/",
  "https://www.thefantasyfootballers.com/articles/auction-draft-strategy-2019-fantasy-football-budget-builder/",
  "https://www.thefantasyfootballers.com/articles/fantasy-football-auction-the-2019-all-value-team/",
  "https://www.thefantasyfootballers.com/articles/week-4-waiver-wire-fantasy-football/",
  "https://www.thefantasyfootballers.com/articles/fantasy-footballers-podcast-recap-the-truth-about-tight-ends-in-2019/",
  "https://www.thefantasyfootballers.com/articles/the-fantasy-footballers-top-10-rb-rankings-recap/",
  "https://www.thefantasyfootballers.com/articles/2020-post-nfl-draft-rb-depth-chart-fantasy-football/",
  "https://www.thefantasyfootballers.com/articles/jason-moores-tiered-rookie-rb-rankings-for-the-2020-nfl-draft/",
  "https://www.thefantasyfootballers.com/articles/evaluating-the-2018-wr-draft-class-fantasy-football/",
  "https://www.thefantasyfootballers.com/articles/three-ppr-running-backs-to-roster-in-2020-fantasy-football/",
  "https://www.thefantasyfootballers.com/articles/the-best-fantasy-football-players-of-the-past-decade/",
  "https://www.thefantasyfootballers.com/articles/25-qb-statistics-from-2020-fantasy-football/",
  "https://www.thefantasyfootballers.com/articles/reviewing-the-2020-rookie-qb-class-fantasy-football/",
  "https://www.thefantasyfootballers.com/articles/nfl-coaching-changes-for-2021-what-it-means-for-fantasy/",
  "https://www.thefantasyfootballers.com/articles/2021-awards-futures-with-borg-betz-fantasy-football/",
  "https://www.thefantasyfootballers.com/articles/how-to-spot-a-fantasy-football-league-winner-tes/",
  "https://www.thefantasyfootballers.com/articles/the-fantasy-football-historian-teams-and-trends/",
  "https://www.thefantasyfootballers.com/articles/dynasty-report-an-early-look-at-three-2022-prospects-fantasy-football/",
  "https://www.thefantasyfootballers.com/articles/the-breakouts-busts-in-every-dynasty-rookie-draft-since-2015-fantasy-football/",
  "https://www.thefantasyfootballers.com/analysis/three-true-deep-sleepers-for-2022-fantasy-football/",
  "https://www.thefantasyfootballers.com/analysis/aiming-your-darts-late-round-fantasy-football-draft-strategy/",
  "https://www.thefantasyfootballers.com/analysis/anticipating-the-breakout-wide-receiver-trends-breakout-candidates-fantasy-football/",
  "https://www.thefantasyfootballers.com/draft-kit/fantasy-football-analyze-your-draft-with-the-ultimate-draft-kit/",
  "https://www.thefantasyfootballers.com/analysis/the-fantasy-footballers-wr-rankings-countdown-20-11/",
  "https://www.thefantasyfootballers.com/analysis/championship-defining-statistics-from-the-2022-season-fantasy-football/",
  "https://www.thefantasyfootballers.com/analysis/the-truth-about-top-10-qbs-in-2023-fantasy-football/",
  "https://www.thefantasyfootballers.com/analysis/targets-per-route-run-report-2023-season-preview-fantasy-football/",
  "https://www.thefantasyfootballers.com/analysis/mike-s-ultimate-value-hitsquad-for-2023-fantasy-football/",
  "https://www.thefantasyfootballers.com/analysis/ultimate-draft-kit-review-the-2023-udk-fantasy-football/",
  "https://www.thefantasyfootballers.com/analysis/waiver-wire-pickups-week-2-fantasy-football/",
  "https://www.thefantasyfootballers.com/dynasty/dynasty-report-an-early-look-at-the-2024-running-back-class-fantasy-football/",
  "https://www.thefantasyfootballers.com/dynasty/dynasty-report-an-early-look-at-the-2024-wide-receiver-class-fantasy-football/",
  "https://www.thefantasyfootballers.com/analysis/the-fantasy-footballers-sleeper-picks-for-2024/",
  "https://www.thefantasyfootballers.com/analysis/players-who-pop-the-best-late-round-draft-values-fantasy-football/",
  "https://www.thefantasyfootballers.com/analysis/the-fantasy-footballers-early-rb-rankings-20-11/",
  "https://www.thefantasyfootballers.com/analysis/1000-fantasy-facts-scheme-stats-get-ready-for-2024-fantasy-football/",
  "https://www.thefantasyfootballers.com/dynasty/dynasty-range-of-outcomes-2024-running-back-class/",
  "https://www.thefantasyfootballers.com/dynasty/dynasty-range-of-outcomes-2024-wide-receiver-class/",
  "https://www.thefantasyfootballers.com/dynasty/dynasty-report-an-early-look-at-the-2025-running-back-class-fantasy-football/",
  "https://www.thefantasyfootballers.com/dynasty/2024-dynasty-ultimatums-5-wrs-entering-make-or-break-fantasy-seasons/",
  "https://www.thefantasyfootballers.com/dynasty/dynasty-rookie-draft-tips-tricks-for-2024/",
  "https://www.thefantasyfootballers.com/dynasty/dynasty-report-an-early-look-at-the-2025-running-back-class-fantasy-football/",
  "https://www.thefantasyfootballers.com/analysis/2025-nfl-draft-nfc-winners-losers-fantasy-football/",
  "https://www.thefantasyfootballers.com/analysis/2025-rb-rankings-10-1-fantasy-football/",
  "https://www.thefantasyfootballers.com/best-ball/draftkings-best-ball-sleepers-for-2025-fantasy-football/",
  "https://www.thefantasyfootballers.com/udk/udk-toolbox-strength-of-schedule-report-fantasy-football/",
  "https://www.thefantasyfootballers.com/analysis/fantasy-football-101-waiver-wire-strategies/",
  "https://www.thefantasyfootballers.com/articles/when-should-you-hit-the-waiver-wire-fantasy-football/",
  "https://www.thefantasyfootballers.com/fantasy-football-draft-kit-footclan/",
]
    ingestion = NewsArticleIngestion()
    result = ingestion.ingest_urls(urls=urls)
    print(result)


if __name__ == "__main__":
    main()
