class ChunkingStats:
    def chunk_stat(self, stat: dict, chunk_size: int) -> str:
        """
        Convert a player's weekly stats into a readable text chunk.

        This is the TEXT that will be:
        1. Stored in the database
        2. Retrieved and shown to the LLM (for answering)
        """

        if stat["position"] not in ["QB", "RB", "WR", "TE"]:
            return None

        chunk = f"""
        {stat['player_display_name']} - {stat['position']} ({stat['team']})
        Week {stat['week']}, {stat['season']} Season

        Fantasy Performance:
        - PPR Points: {stat['fantasy_points_ppr']:.1f}
        - Standard Points: {stat['fantasy_points']:.1f}

        Game Stats:
        """

        # Add position-specific stats
        if stat["position"] == "QB":
            chunk += f"""Passing: {stat['completions']}/{stat['attempts']} comp, {stat['passing_yards']} yards, {stat['passing_tds']} TDs, {stat['passing_interceptions']} INTs
            Rushing: {stat['carries']} carries, {stat['rushing_yards']} yards, {stat['rushing_tds']} TDs
            Sacks Taken: {stat['sacks_suffered']}, fumbles lost: {stat['receiving_fumbles_lost'] + stat['rushing_fumbles_lost']}"""

        elif stat["position"] == "RB":
            chunk += f"""Rushing: {stat['carries']} carries, {stat['rushing_yards']} yards, {stat['rushing_tds']} TDs
            Receiving: {stat['receptions']} receptions, {stat['receiving_yards']} yards, {stat['receiving_tds']} TDs
            Targets: {stat['targets']}, fumbles lost: {stat['receiving_fumbles_lost'] + stat['rushing_fumbles_lost']}"""

        elif stat["position"] in ["WR", "TE"]:
            chunk += f"""Receiving: {stat['receptions']} receptions, {stat['receiving_yards']} yards, {stat['receiving_tds']} TDs
            Targets: {stat['targets']}
            Rushing: {stat['carries']} carries, {stat['rushing_yards']} yards, {stat['rushing_tds']} TDs, fumbles lost: {stat['receiving_fumbles_lost'] + stat['rushing_fumbles_lost']}"""

        return chunk.strip()
