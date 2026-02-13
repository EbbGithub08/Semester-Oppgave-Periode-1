import sqlite3
from typing import Dict, List, Tuple


class HighscoreDatabase:

    def __init__(self, db_path: str = "Database/platformer_scores.db"):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self) -> None:
        with self._get_connection() as conn:
            c = conn.cursor()

            c.execute(
                """
                CREATE TABLE IF NOT EXISTS highscores (
                    username TEXT,
                    world INTEGER,
                    time_seconds REAL,
                    coins INTEGER,
                    perfect_run INTEGER,
                    score_version INTEGER DEFAULT 0
                )
                """
            )

            c.execute("PRAGMA table_info(highscores)")
            columns = [info[1] for info in c.fetchall()]
            if 'coins' not in columns:
                c.execute("ALTER TABLE highscores ADD COLUMN coins INTEGER DEFAULT 0")
            if 'perfect_run' not in columns:
                c.execute("ALTER TABLE highscores ADD COLUMN perfect_run INTEGER DEFAULT 0")
            if 'score_version' not in columns:
                c.execute("ALTER TABLE highscores ADD COLUMN score_version INTEGER DEFAULT 0")

            c.execute("DELETE FROM highscores WHERE LENGTH(username) > 9")

    def save_highscore(self, username: str, world: int, time_seconds: float, coins: int, perfect_run: bool) -> None:
        username = "".join(char for char in username if char.isalpha()).upper()[:9]
        if not username:
            return

        p_run_int = 1 if perfect_run else 0

        with self._get_connection() as conn:
            c = conn.cursor()
            c.execute(
                "SELECT time_seconds FROM highscores WHERE username = ? AND world = ? AND perfect_run = ?",
                (username, world, p_run_int),
            )
            row = c.fetchone()

            if row is None:
                c.execute(
                    "INSERT INTO highscores (username, world, time_seconds, coins, perfect_run, score_version) VALUES (?, ?, ?, ?, ?, 1)",
                    (username, world, time_seconds, coins, p_run_int),
                )
                print(f"Lagret ny highscore for {username}: {time_seconds:.2f}s (Perfect: {perfect_run})")
            elif time_seconds < row[0]:
                c.execute(
                    "UPDATE highscores SET time_seconds = ?, coins = ?, score_version = 1 WHERE username = ? AND world = ? AND perfect_run = ?",
                    (time_seconds, coins, username, world, p_run_int),
                )
                print(f"Oppdaterte highscore for {username}: {time_seconds:.2f}s (Gammel: {row[0]:.2f}s, Perfect: {perfect_run})")
            else:
                print(f"Tiden var ikke rask nok for {username}: {time_seconds:.2f}s (Best: {row[0]:.2f}s, Perfect: {perfect_run})")

    def debug_print_scores(self) -> None:
        print("\n====== LEADERBOARDS (DEBUG) ======")
        with self._get_connection() as conn:
            c = conn.cursor()
            for w in range(1, 6):
                c.execute("SELECT * FROM highscores WHERE world = ? ORDER BY time_seconds ASC", (w,))
                rows = c.fetchall()
                
                world_name = f"WORLD {w}"
                if w == 4: world_name = "TUTORIAL"
                if w == 5: world_name = "DEMON WORLD"
                
                print(f"\n--- {world_name} ---")
                if not rows:
                    print("Ingen scores enda.")
                else:
                    for rank, row in enumerate(rows, 1):
                        username = row[0]
                        time_s = row[2]
                        coins = row[3] if len(row) > 3 else 0
                        perfect = row[4] if len(row) > 4 else 0
                        perfect_str = " (PERFECT)" if perfect else ""
                        print(f"{rank}. {username} - {time_s:.2f}s - Coins: {coins}{perfect_str}")
        print("\n================================")

    def _get_scores_by_world(self, limit_per_world: int = None) -> Dict[int, List[Tuple]]:
        scores: Dict[int, List[Tuple]] = {}
        query = "SELECT * FROM highscores WHERE world = ? ORDER BY time_seconds ASC"
        if limit_per_world:
            query += f" LIMIT {limit_per_world}"

        with self._get_connection() as conn:
            c = conn.cursor()
            for w in range(1, 6):
                c.execute(query, (w,))
                scores[w] = c.fetchall()
        return scores

    def get_top_scores(self) -> Dict[int, List[Tuple]]:
        return self._get_scores_by_world(limit_per_world=3)

    def get_all_scores(self) -> Dict[int, List[Tuple]]:
        return self._get_scores_by_world()
