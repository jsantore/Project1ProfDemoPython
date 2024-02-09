import DataProcessing
import DbUtils
def test_get_data():
    jobs_data = DataProcessing.get_multiple_pages_of_jobs(5)
    assert len(jobs_data) == 50

def test_insert_data():
    conn, cursor = DbUtils.open_db("TestDB")
    DbUtils.setup_db(cursor)
    sample_job = ("IDzxcvergqaer", "Test Job", "Comp490 Inc", "Work really hard and learn a lot",
                  "Bridgewater, MA", 50000, 90000, "Yearly", "Tomorrow",
                  "https://webhost.bridgew.edu/jsantore/Spring2024/Capstone/Project1Sprint2.html", True)
    DbUtils.insert_job(cursor, sample_job)
    cursor.execute("""SELECT job_title, location, min_salary 
    FROM jobs_listings WHERE job_id = ?""", (sample_job[0],))
    record = cursor.fetchone()
    assert record[0]=="Test Job"
    assert record[1]=="Bridgewater, MA"
    assert record[2]==50000