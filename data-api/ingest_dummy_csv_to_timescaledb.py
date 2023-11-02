import psycopg2

conn = psycopg2.connect("host='localhost' dbname='timescale_db' user='timescale_user' password='timescale_password'")
cur = conn.cursor()

with open('../92-Site_DKA-M6_B-Phase.csv', 'r') as f: # TO DO: change location to variable
    cur.copy_expert(sql="COPY solar_array_telemetry FROM stdin WITH CSV HEADER DELIMITER as ','", file=f)
    conn.commit()
    cur.close()
    conn.close()
