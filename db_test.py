import psycopg2

def test_database_connection():
    try:
        conn = psycopg2.connect(
            dbname="db",
            user="postgres",
            password="Ok1234567890.",
            host="localhost",
            port="5432"
        )
        
        cur = conn.cursor()
        print("Tilkobling til 'db' vellykket! 🟢")

        cur.execute("SELECT * FROM kontakter;")
        rows = cur.fetchall()
        print(f"Antall rader i 'kontakter' akkurat nå: {len(rows)}")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"Feilet ved tilkobling: {e}")

if __name__ == "__main__":
    test_database_connection()