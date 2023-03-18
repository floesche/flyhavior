import sqlite3

class PostProcessor:

    def __init__(self, fnDB) -> None:
        self.db = sqlite3.connect(fnDB)


    def vacuum(self) -> None:
        self.db.execute("VACUUM")

    def fix_data(self) -> None:
        self.db.execute("""
            UPDATE condition 
            SET gain=-1.0 
            WHERE condition_type="CLOSED" AND gain IS NULL
        """)


    def alter_v_move(self) -> None:
        self.db.execute("""
            DROP VIEW IF EXISTS v_move 
        """)
        self.db.commit()

        self.db.execute("""
            CREATE VIEW IF NOT EXISTS
            v_move AS 
            SELECT 
                f.number AS fly_number, f.sex, f.strain, f.birth_after, f.birth_before, f.day_start, f.day_end, 
                b.number as ball_number,
                e.temperature, e.air, e.glue, e.start,
                c.repetition, c.stimulus_type, c.trial_number, c.trial_type, c.condition_number, c.condition_type, c.fps, c.bar_size, c.interval_size, c.gain, c.start_orientation, c.comment, c.fg_color, c.bg_color, c.left_right,
                c.contrast, c.brightness,
                ac.bar_deg, ac.interval_deg, ac.trial_speed, ac.trial_speed_deg, ac.direction,
                r.rendered, r.speed, r.angle, r.client_ts_ms, c.start_mask, c.end_mask,
                -- at.turn,
                t.*
            FROM fly f 
            LEFT JOIN experiment e on f.id = e.fly_id 
            LEFT JOIN ball b on e.ball_id=b.id
            LEFT JOIN condition c on c.experiment_id = e.id
            LEFT JOIN a_condition ac on ac.condition_id=c.id
            LEFT JOIN rotation r on r.condition_id = c.id
            LEFT JOIN fictrac t ON r.fictrac_id = t.id
            -- LEFT JOIN a_fictrac at on at.fictrac_id=t.id
        """)
        self.db.commit()

    def create_a_condition(self) -> None:

        self.db.execute("""DROP TABLE IF EXISTS a_condition""")

        self.db.execute("""
        CREATE TABLE IF NOT EXISTS
        a_condition(
            condition_id INTEGER UNIQUE,
            bar_deg REAL,
            interval_deg REAL,
            trial_speed REAL,
            trial_speed_deg REAL,
            direction TEXT CHECK(direction IN("CW","CCW")),
            FOREIGN KEY (condition_id) REFERENCES Condition(id) ON DELETE RESTRICT ON UPDATE RESTRICT
        )
        """)

        self.db.execute("""
            INSERT INTO a_condition (
                condition_id, 
                bar_deg,
                interval_deg
            ) SELECT 
                id, 
                bar_size*180/3.141592653589793115997963468544185161590576171875,
                interval_size*180/3.141592653589793115997963468544185161590576171875
            FROM condition
        """)

        self.db.execute("""
        UPDATE a_condition 
        SET trial_speed = cond.speed
        FROM (
            SELECT c1.id as id, c1.trial_type as trial_type, avg(speed) as speed 
            FROM condition c1 
            left join condition c2 on c1.trial_number=c2.trial_number and c1.experiment_id=c2.experiment_id and c2.condition_type="OPEN" 
            left join rotation r on c2.id=r.condition_id group by c1.id
        ) as cond
        where a_condition.condition_id = cond.id and cond.trial_type="OPEN"
        """)

        self.db.execute("""
        UPDATE a_condition 
        SET 
            trial_speed_deg = round(ac.trial_speed*180/3.141592653589793115997963468544185161590576171875 / bar_deg *100) / 100,
            direction = iif(ac.trial_speed>0, "CW", 
                            iif(ac.trial_speed<0, "CCW", NULL))
        FROM (
            SELECT condition_id, trial_speed
            from a_condition
        ) as ac
        where ac.condition_id=a_condition.condition_id
        """)

        self.db.commit()


    def create_a_fictrac(self) -> None:

        self.db.execute("""DROP TABLE IF EXISTS a_fictrac""")

        # self.db.execute("""
        # CREATE TABLE IF NOT EXISTS
        # a_fictrac(
        #     fictrac_id INTEGER UNIQUE,
        #     turn REAL,
        #     FOREIGN KEY (fictrac_id) REFERENCES fictrac(id) ON DELETE RESTRICT ON UPDATE RESTRICT
        # )
        # """)

        # self.db.execute("""
        # INSERT INTO a_fictrac (
        #     fictrac_id,
        #     turn
        # ) SELECT 
        #     fi.id as fid,
        #     ((fi.hdiff+fi.pi) - cast((fi.hdiff+fi.pi)/(2*fi.pi) AS INT)*(2*fi.pi))-fi.pi as trn
            
        # FROM (
        #     SELECT 
        #         id, 
        #         lag(animal_lab_heading) OVER (order by id) - animal_lab_heading hdiff, 
        #         3.141592653589793115997963468544185161590576171875 as pi 
        #         FROM fictrac
        # ) as fi
        # """)



