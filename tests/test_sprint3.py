import DataProcessing
import openpyxl
import DbUtils


def test_get_excel():  # this is beyond the test I asked for
    excel_worbook = openpyxl.Workbook()
    sheet = excel_worbook.active
    sheet.append(
        [
            "Company Name",
            "Posting Age",
            "Job Id",
            "Country",
            "Location",
            "Publication Date",
            "Salary Max",
            "Salary Min",
            "Salary Type",
            "Job Title",
        ]
    )
    for row in range(10):
        sheet.append(
            [
                f"Company-{row}",
                f"Posted {row} days ago",
                f"Job-{row}",
                "US",
                "Bridgewater, MA",
                1235324534215,
                f"{(row + row) * 10000}",
                f"{row * 10000}",
                "yearly",
                "Software Developer Level {row}",
            ]
        )
    excel_worbook.save("test.xlsx")
    test_data = DataProcessing.get_excel_data("test.xlsx")
    assert (
        len(test_data) == 10
    )  # we put ten peices of data plus the header - we should get that out.
    third_row = test_data[3]
    print(third_row)
    assert third_row[0] == "Job-3"


def test_get_excel_data_existing_artifact():
    test_data = DataProcessing.get_excel_data("Sprint3Data.xlsx")
    assert len(test_data) >= 300


def test_jobs_table_exists():
    conn, cursor = DbUtils.open_db("Sprint3Test.db")
    DbUtils.setup_db(cursor)
    cursor.execute(
        "Select * from sqlite_master where type='table' and name='jobs_listings';"
    )
    table_records = cursor.fetchall()
    assert len(table_records) == 1


# no need to test write to table because I used the same one as in sprint2
