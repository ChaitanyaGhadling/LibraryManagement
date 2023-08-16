import mysql.connector
import datetime


def get_connection():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="7004",
            database='librarydatabase'
        )
        return mydb
    except Exception as e:
        print("Unable to connect to Database. \n Error:", e)


def authorize_admin(id, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("select * from admin_login where admin_id =%s and password = %s", (id, password))
    validate = cursor.fetchone()
    conn.close()
    return validate


def authorize_reader(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("select rid from reader where rid = %s", (id,))
    validate = cursor.fetchone()
    conn.close()
    return validate


def reader_menu(rid):
    conn = get_connection()
    while True:
        print("1. Search a document by ID, title, or publisher name. ")
        print("2. Document checkout.")
        print("3. Document return.")
        print("4. Document reserve.")
        print("5. Compute Fine")
        print("6. List of Reserved Documents and Status")
        print("7. Document ID and and document titles of the publisher.")
        print("8. Exit")
        choice = input("Enter your choice:")
        match choice:
            case "1":
                search_by = input("Enter a document ID, title or publisher name:")
                try:
                    cursor = conn.cursor()
                    cursor.execute("select d.docid, d.title, d.pdate, p.pubname from document d, publisher p"
                                   " where d.docid = %s or d.title = %s or p.pubname = %s;", (int(search_by), search_by,
                                                                                         search_by))
                except ValueError:
                    cursor = conn.cursor()
                    cursor.execute("select d.docid, d.title, d.pdate, p.pubname from document d, publisher p"
                                   " where d.title = %s or p.pubname = %s;", (search_by, search_by))
                for row in cursor:
                    print(" Document ID:",row[0], ".\n Title:", row[1], ".\n Date Published:", row[2],
                          ".\n Publisher Name:", row[3])
            case "2":
                docid, bid = input("Enter DocumentID and Branch ID of the document "
                                           "to be borrowed:").split()
                docid = int(docid)
                bid = int(bid)

                cursor = conn.cursor()
                cursor.execute("select bor_no from borrowing order by bor_no DESC limit 1")
                bor_no = cursor.fetchone()[0] + 1
                cursor.execute("select copyno from reserves where docid=%s and bid=%s and rid=%s",
                               (docid, bid, rid))
                reserved_copyno = cursor.fetchone()
                if reserved_copyno:
                    reserved_copyno = reserved_copyno[0]
                    cursor.execute("delete from reserves where docid=%s and bid=%s and rid=%s and copyno=%s",
                                   (docid, bid, rid, reserved_copyno))
                    conn.commit()
                    cursor.execute("insert into borrowing (bor_no, bdtime) values (%s,%s) ", (bor_no, datetime.datetime.now()))
                    conn.commit()
                    cursor.execute("insert into borrows values (%s,%s,%s,%s,) ", (bor_no, docid, reserved_copyno
                                                                             , bid, rid))
                    conn.commit()
                    print("Borrowing complete")
                else:
                    cursor.execute("select count(docid) from borrows where rid = %s", (rid, ))
                    bor_count = cursor.fetchone()[0]
                    cursor.execute("select count(docid) from reserves where rid = %s", (rid, ))
                    res_count = cursor.fetchone()[0]
                    doc_count = bor_count + res_count
                    print("Number of Documents borrowed or reserved: ", doc_count)
                    if doc_count > 10:
                        print("Borrowing limit Exceeded.\n Please return books or borrow a reserved book. ")
                    else:
                        cursor.execute("select copyno from copy where docid = %s and bid = %s and copyno not in( "
                                       "(select copyno from reserves where docid = %s and bid = %s) union "
                                       "(select copyno from borrows where docid = %s and bid = %s)) limit 1",
                                       (docid, bid, docid, bid, docid, bid))
                        copyno = cursor.fetchone()
                        if copyno:
                            cursor.execute("insert into borrowing (bor_no, bdtime) values (%s,%s) ",
                                           (bor_no, datetime.datetime.now()))
                            conn.commit()
                            cursor.execute("insert into borrows values (%s,%s,%s,%s,%s) ",
                                           (bor_no, docid, copyno[0], bid, rid))
                            conn.commit()
                            print("Borrowing complete")
                        else:
                            print("Document not available at the moment.")
            case "3":
                cursor = conn.cursor()
                cursor.execute("select * from borrows where rid =%s", (rid,))
                docs_borrowed = cursor.fetchall()
                i = 1
                for docs in docs_borrowed:
                    print(i, ". Borrowing No:", docs[0], "DocumentID:", docs[1], "CopyNo:", docs[2],
                          "BranchID:", docs[3])
                    i += 1
                bor_no = input("Enter the Borrowing No of the document you want to return:")
                bor_no = int(bor_no)
                cursor.execute("delete from borrows where bor_no = %s ", (bor_no,))
                conn.commit()
                cursor.execute("update borrowing set rdtime = %s where bor_no =%s", (datetime.datetime.now(),
                                                                                    bor_no))
                conn.commit()
                print("Returned Successfully")
            case "4":
                docid, bid = input("Enter DocumentID and Branch ID of the document "
                                   "to be borrowed.").split()
                docid = int(docid)
                bid = int(bid)

                cursor = conn.cursor()
                cursor.execute("select res_no from reservation order by res_no DESC limit 1")
                res_no = cursor.fetchone()[0] + 1
                cursor.execute("select copyno from copy where docid = %s and bid = %s and copyno not in( "
                               "(select copyno from reserves where docid = %s and bid = %s) union "
                               "(select copyno from borrows where docid = %s and bid = %s)) limit 1",
                               (docid, bid, docid, bid, docid, bid))
                copyno = cursor.fetchone()
                if copyno:
                    cursor.execute("insert into reservation (res_no, dtime) values (%s,%s) ",
                                   (res_no, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    conn.commit()
                    cursor.execute("insert into reserves values (%s,%s,%s,%s,%s) ",
                                   (rid, res_no, docid, copyno[0], bid))
                    conn.commit()
                    print("Reservation Complete")
                else:
                    print("Document not available at the moment.")
            case "5":
                cursor = conn.cursor()
                cursor.execute("create or replace view calculate_fine as select t.rid, t.bor_no, "
                               "t.bdtime, t.rdtime, t.duedate, datediff(t.rdtime, t.duedate) * 0.2 as fine from "
                               "(select b.rid, bo.bor_no, bo.bdtime, bo.rdtime, adddate(bo.bdtime, 20) as duedate "
                               "from borrowing bo join borrows b on bo.bor_no = b.bor_no where b.rid =%s) as t", (rid, ))
                conn.commit()
                cursor.execute("select sum(fine) from calculate_fine where fine > 0")
                fine = cursor.fetchone()
                if fine:
                    print(" Total Fine calculated: ", fine[0])
                else:
                    print(" No fine amount on record.")
            case "6":
                cursor = conn.cursor()
                cursor.execute("select d.title, d.docid, r.reservation_no from document d, copy c, "
                               "reserves r where d.docid = c.docid and c.docid = r.docid and "
                               "c.copyno = r.copyno and c.bid = r.bid and r.rid =%s", (rid, ))
                docs = cursor.fetchall()
                for doc in docs:
                    print(" Title:", doc[0], ". DocumentID:", doc[1], ". ReservationNo:", doc[2])
            case "7":
                pub_name = input("Enter the publisher name whose documents you want to search:")
                cursor = conn.cursor()
                cursor.execute("select d.docid, d.title from document d, publisher p where "
                               "d.publisherid = p.publisherid and p.pubname = %s", (pub_name, ))
                docs = cursor.fetchall()
                for doc in docs:
                    print("DocumentID:", doc[0], ".Title: ", doc[1])
            case "8":
                break
            case _:
                print("Enter correct choice.")


def admin_menu():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("")
    while True:
        print("1. Add document Copy ")
        print("2. Search Document Copy and its Status.")
        print("3. Add new Reader")
        print("4. Print Branch Name and Location.")
        print("5. Check Most frequent Borrowers in a given Branch with Book Info.")
        print("6. Check Most frequent Borrowers overall with Book Info")
        print("7. Check Most Borrowed books in a given branch")
        print("8. Most Borrowed books overall.")
        print("9. Most Borrowed books by year.")
        print("10. Average fine paid by borrowers in given time period")
        print("11. Exit")
        choice = input("Enter your choice:")
        match choice:
            case "1":
                pass
            case "2":
                pass
            case "3":
                pass
            case "4":
                pass
            case "5":
                pass
            case "6":
                pass
            case "7":
                pass
            case "8":
                pass
            case "9":
                pass
            case "10":
                pass
            case "11":
                break
            case _:
                print("Enter correct choice.")


if __name__ == '__main__':
    conn = get_connection()
    while True:
        print("1. Reader")
        print("2. Administrators")
        print("3. Exit")
        choice = input("Enter the choice:")
        match choice:
            case "1":
                card_number = int(input("Enter the card number/Reader ID:"))
                if authorize_reader(card_number):
                    reader_menu(card_number)
                else:
                    print("No user with " + str(card_number) + " card_number found")
            case "2":
                admin_id = input("Enter the Admin ID:")
                password = input("Enter your password:")
                if authorize_admin(admin_id, password):
                    admin_menu()
                else:
                    print("User Id or Password Incorrect")
            case "3":
                break
            case _:
                print("Enter correct choice.")





