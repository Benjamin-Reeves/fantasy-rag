from news_articles.ingestion import NewsArticleIngestion


def main() -> None:
    urls = [
  "https://www.espn.com/fantasy/football/story/_/page/FFPreseasonRank24/fantasy-football-rankings-2024-draft-ppr-non-ppr",
  "https://www.espn.com/fantasy/football/story/_/id/44786976/fantasy-football-rankings-2025-draft-ppr",
  "https://www.espn.com/fantasy/football/story/_/id/39247161/fantasy-football-rankings-2024-ppr",
  "https://www.espn.com/fantasy/football/story/_/id/36304365/fantasy-football-rankings-2023-ppr-non-ppr",
  "https://www.espn.com/fantasy/football/story/_/id/36135778/fantasy-football-ppr-rankings-2023-quarterback-running-back-wide-receiver-tight-end-top-200",
  "https://www.espn.com/fantasy/football/story/_/page/23ffdraftkit/2023-fantasy-football-draft-rankings-cheat-sheets-sleepers",
  "https://www.espn.com/fantasy/football/story/_/page/23ffcheatsheet/2023-fantasy-football-rankings-cheat-sheet-depth-charts-ppr",
  "https://www.espn.com/fantasy/football/story/_/page/FFCheatSheetCent24-39970898/2024-fantasy-football-rankings-cheat-sheet-depth-charts-ppr",
  "https://www.espn.com/fantasy/football/story/_/id/39386014/fantasy-football-rankings-2024-ppr-top-200",
  "https://www.espn.com/fantasy/football/story/_/id/40196245/2024-fantasy-football-rankings-ppr-field-yates-qb-rb-wr-te",
  "https://www.espn.com/fantasy/football/story/_/id/37683451/2023-fantasy-football-rankings-ppr-field-yates-qb-rb-wr-te",
  "https://www.espn.com/fantasy/football/story/_/id/39273386/fantasy-football-superflex-rankings-2024-qb-rb-wr-te",
  "https://www.espn.com/fantasy/football/story/_/page/23ffhighslows/nfl-fantasy-football-2024-rankings-2023-awards",
  "https://www.espn.com/fantasy/football/story/_/page/imagined070720/updated-fantasy-football-draft-sleepers-busts-breakouts-2020",
  "https://www.espn.com/fantasy/football/story/_/id/32045379/fantasy-football-breakouts-sleepers-individual-defensive-players-idp-watch",
  "https://www.pff.com/news/fantasy-football-rankings-2025-ppr",
  "https://www.pff.com/news/fantasy-football-rankings-2025-standard-leagues",
  "https://www.pff.com/news/fantasy-football-rankings-2024",
  "https://www.pff.com/news/fantasy-football-rankings-2024-standard-top-400",
  "https://www.pff.com/news/fantasy-football-rankings-2024-week-1",
  "https://www.pff.com/news/fantasy-football-rankings-2024-combined-offense-and-idp-rankings-and-strategy",
  "https://www.pff.com/news/fantasy-football-rankings-2023-top-250",
  "https://www.pff.com/fantasy/articles",
  "https://www.cbssports.com/fantasy/football/news/fantasy-football-rankings-2025-sleepers-breakouts-and-busts-by-computer-that-forecasted-strouds-tough-year/",
  "https://www.cbssports.com/fantasy/football/news/fantasy-football-rankings-2025-sleepers-breakouts-and-busts-by-computer-that-forecasted-strouds-down-year/",
  "https://www.cbssports.com/fantasy/football/news/fantasy-football-rankings-2025-sleepers-breakouts-and-busts-by-model-that-predicted-strouds-down-year/",
  "https://www.cbssports.com/fantasy/football/news/fantasy-football-2022-rankings-draft-prep-qb-wr-rb-te-picks-cheat-sheets-adp-tiers-by-analytical-model/",
  "https://www.cbssports.com/fantasy/football/news/fantasy-football-rankings-top-24-for-2022-with-player-outlooks-plus-top-150-overall/",
  "https://www.cbssports.com/fantasy/football/news/fantasy-football-today-heres-your-first-look-at-the-2022-rankings/",
  "https://cbssports.com/fantasy/football/news/fantasy-football-rankings-2022-sleepers-breakouts-busts-from-strong-model-that-nailed-taylors-huge-season",
  "https://www.cbssports.com/fantasy/football/rankings/ppr/top200/",
  "https://www.fantasypros.com/2023/08/fantasy-football-draft-values-busts-sleepers-afc-east-2023/",
  "https://www.fantasypros.com/2023/08/fantasy-football-draft-values-busts-sleepers-afc-north-2023/",
  "https://www.fantasypros.com/2023/08/fantasy-football-draft-values-busts-sleepers-afc-west-2023/",
  "https://www.fantasypros.com/2023/08/fantasy-football-draft-values-busts-sleepers-nfc-east-2023/",
  "https://www.fantasypros.com/2023/08/fantasy-football-draft-values-busts-sleepers-nfc-north-2023/",
  "https://www.fantasypros.com/2023/08/fantasy-football-draft-values-busts-sleepers-nfc-south-2023/",
  "https://www.fantasypros.com/2023/08/fantasy-football-draft-values-busts-sleepers-nfc-west-2023/",
  "https://www.fantasypros.com/2023/08/5-fantasy-football-draft-sleepers/",
  "https://www.fantasypros.com/2023/08/fantasy-football-draft-sleepers-experts-target/",
  "https://www.fantasypros.com/2023/09/experts-favorite-fantasy-football-sleepers-2023/",
  "https://www.fantasypros.com/nfl/rankings/consensus-cheatsheets.php",
  "https://www.rotowire.com/football/article/draft-strategy-slots-10-12-83975",
  "https://www.rotowire.com/football/article/draft-strategy-32-fades-one-from-each-team-84356",
  "https://www.rotowire.com/football/article/rotowire-roundtable-2024-top-150-fantasy-rankings-final-update-84649",
  "https://www.rotowire.com/football/article/the-fantasy-year-in-review-2023s-biggest-draft-values-79052",
  "https://www.rotowire.com/football/draft-kit.php",
  "https://www.rotowire.com/football/advice/",
  "https://www.4for4.com/2020/preseason/99-fantasy-football-stats",
  "https://www.4for4.com/2020/preseason/4-fantasy-football-trends-apply-2020",
  "https://www.footballguys.com/articles",
  "https://www.dynastynerds.com/"
]
    ingestion = NewsArticleIngestion()
    result = ingestion.ingest_urls(urls=urls)
    print(result)


if __name__ == "__main__":
    main()
