import sqlite3
from typing import Dict, List, Tuple


class HighscoreDatabase:

    def __init__(self, db_path: str = "Database/platformer_scores.db"):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self) -> None:
        conn = self._get_connection()
        c = conn.cursor()

        try:
            c.execute("SELECT time_seconds FROM highscores LIMIT 1")
        except sqlite3.OperationalError:
            c.execute("DROP TABLE IF EXISTS highscores")
            print("Gammel database oppdaget. Oppdaterer tabell...")

        c.execute(
            """
            CREATE TABLE IF NOT EXISTS highscores
            (username TEXT, world INTEGER, time_seconds REAL)
            """
        )

        conn.commit()
        conn.close()

    def save_highscore(self, username: str, world: int, time_seconds: float) -> None:
        username = "".join(char for char in username if char.isalpha()).upper()
        if not username:
            return

        conn = self._get_connection()
        c = conn.cursor()

        c.execute(
            "SELECT time_seconds FROM highscores WHERE username = ? AND world = ?",
            (username, world),
        )
        row = c.fetchone()

        if row is None:
            c.execute(
                "INSERT INTO highscores VALUES (?, ?, ?)",
                (username, world, time_seconds),
            )
            print(
                f"Saved New Highscore -> Name: {username}, World: {world}, "
                f"Time: {time_seconds:.2f} Sec"
            )
        elif time_seconds < row[0]:
            c.execute(
                "UPDATE highscores SET time_seconds = ? WHERE username = ? AND world = ?",
                (time_seconds, username, world),
            )
            print(
                f"Updated Highscore -> Name: {username}, World: {world}, "
                f"Time: {time_seconds:.2f} Sec"
            )
        else:
            print(
                f"Time not fast enough -> Name: {username}, World: {world}, "
                f"Time: {time_seconds:.2f} Sec (Best: {row[0]:.2f})"
            )

        conn.commit()
        conn.close()

    def debug_print_scores(self) -> None:
        conn = self._get_connection()
        c = conn.cursor()

        print("\n====== LEADERBOARDS ======")
        for w in range(1, 6):
            c.execute(
                "SELECT * FROM highscores WHERE world = ? ORDER BY time_seconds ASC",
                (w,),
            )
            rows = c.fetchall()
            world_name = "TUTORIAL" if w == 4 else f"WORLD {w}"
            print(f"\n--- {world_name} ---")
            if not rows:
                print("No scores yet.")
            else:
                for rank, row in enumerate(rows, 1):
                    print(f"{rank}. {row[0]} - {row[2]:.2f}s")
        print("\n==========================")
        conn.close()

    def get_top_scores(self) -> Dict[int, List[Tuple[str, int, float]]]:
        conn = self._get_connection()
        c = conn.cursor()
        scores: Dict[int, List[Tuple[str, int, float]]] = {}
        for w in range(1, 6):
            c.execute(
                "SELECT * FROM highscores WHERE world = ? ORDER BY time_seconds ASC LIMIT 3",
                (w,),
            )
            rows = c.fetchall()
            scores[w] = rows
        conn.close()
        return scores

    def get_all_scores(self) -> Dict[int, List[Tuple[str, int, float]]]:
        conn = self._get_connection()
        c = conn.cursor()
        scores: Dict[int, List[Tuple[str, int, float]]] = {}
        for w in range(1, 6):
            c.execute(
                "SELECT * FROM highscores WHERE world = ? ORDER BY time_seconds ASC",
                (w,),
            )
            rows = c.fetchall()
            scores[w] = rows
        conn.close()
        return scores

