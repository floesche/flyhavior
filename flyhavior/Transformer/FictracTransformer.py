import pandas as pd

from Entities.BaseModel import db

class FictracTransformer():

    def __init__(self, datfile, experiment):
        self.datfile = datfile
        self.experiment = experiment


    def run(self):

        df = pd.read_csv(self.datfile,\
            names=["frame_counter", \
            "d_cam_x", "d_cam_y", "d_cam_z",\
            "err",\
            "d_lab_x", "d_lab_y", "d_lab_z",\
            "cam_x", "cam_y", "cam_z",\
            "lab_x", "lab_y", "lab_z",\
            "integrated_lab_x", "integrated_lab_y",\
            "animal_lab_heading",\
            "animal_lab_movement",\
            "animal_speed",\
            "integrated_movement_x", "integrated_movement_y",\
            "timestamp",\
            "seq",\
            "delta_timestamp",\
            "alternative_timestamp"])
    
        df.sort_values('frame_counter', inplace=True)
        # sql = '''SELECT MIN(r.fictrac_id) AS minf, MAX(r.fictrac_id) AS maxf 
        #          FROM Condition c 
        #          INNER JOIN rotation r on c.id = r.conditionID 
        #          INNER JOIN Experiment e ON c.experimentID = e.id 
        #          WHERE e.id=?'''
        # cur = conn.execute(sql, (experiment_id))
        # rows = cur.fetchall()
        # assert len(rows) == 1, "Something went wrong when finding min/max"
        # ficmin = rows[0][0]
        # ficmax = rows[0][1]
        df["experiment_id"] = self.experiment.id
        
        df.to_sql("fictrac_tmp", db, if_exists="replace", index=False)
        sql = '''
            INSERT OR IGNORE INTO fictrac (
                frame_counter, experiment_id, 
                d_cam_x, d_cam_y, d_cam_z, 
                err, 
                d_lab_x, d_lab_y, d_lab_z, 
                cam_x, cam_y, cam_z, 
                lab_x, lab_y, lab_z, 
                integrated_lab_x, integrated_lab_y,
                animal_lab_heading, animal_lab_movement, animal_speed,
                integrated_movement_x, integrated_movement_y,
                timestamp, seq, 
                delta_timestamp, alternative_timestamp) 
            SELECT 
                frame_counter, experiment_id, 
                d_cam_x, d_cam_y, d_cam_z, 
                err, 
                d_lab_x, d_lab_y, d_lab_z, 
                cam_x, cam_y, cam_z, 
                lab_x, lab_y, lab_z, 
                integrated_lab_x, integrated_lab_y,
                animal_lab_heading, animal_lab_movement, animal_speed,
                integrated_movement_x, integrated_movement_y,
                timestamp, seq, 
                delta_timestamp, alternative_timestamp 
            FROM fictrac_tmp'''
        db.execute_sql(sql)
        db.commit()
    
        db.execute_sql("DROP TABLE fictrac_tmp")
        db.commit()

        sql = '''
            SELECT MIN(id), MAX(id), fictrac_seq, COUNT(*)
            FROM Rotation
            GROUP BY fictrac_seq
        '''
        cur = db.execute_sql(sql)
        rows = cur.fetchall()

        # FIXME this will break with more than one experiment at a time. 
        sql = f'''
            UPDATE rotation AS r
            SET fictrac_id = fictrac.id
            FROM rotation 
                LEFT JOIN fictrac ON rotation.fictrac_seq=fictrac.frame_counter
            WHERE r.id = rotation.id 
        '''
        db.execute_sql(sql)

        # Clean out fictrac
        sql = '''DELETE from 
                 fictrac where experiment_id=? and (
                 id<(select min(r.fictrac_id) from Rotation r INNER JOIN Condition c on r.condition_id=c.ID where c.experiment_id=?) or 
                 id>(select max(r.fictrac_id) from Rotation r INNER JOIN Condition c on r.condition_id=c.ID where c.experiment_id=?))'''
        db.execute_sql(sql, (self.experiment.id,self.experiment.id,self.experiment.id,))
        db.commit()

        sql = '''
            CREATE VIEW IF NOT EXISTS
            v_move AS 
            SELECT 
                f.number AS fly_number, f.sex, f.strain, f.birth_after, f.birth_before, f.day_start, f.day_end, 
                b.number as ball_number,
                e.temperature, e.air, e.glue, e.start,
                c.repetition, c.stimulus_type, c.trial_number, c.trial_type, c.condition_number, c.condition_type, c.fps, c.bar_size, c.interval_size, c.gain, c.start_orientation, c.comment, c.fg_color, c.bg_color, c.left_right,
                c.contrast, c.brightness,
                r.rendered, r.speed, r.angle, r.client_ts_ms,
                -- at.turn,
                t.*
            FROM fly f 
            LEFT JOIN experiment e on f.id = e.fly_id 
            LEFT JOIN ball b on e.ball_id=b.id
            LEFT JOIN condition c on c.experiment_id = e.id
            LEFT JOIN rotation r on r.condition_id = c.id
            LEFT JOIN fictrac t ON r.fictrac_id = t.id
            -- LEFT JOIN a_fictrac at on at.fictrac_id=t.id
        '''
        db.execute_sql(sql)
        db.commit()