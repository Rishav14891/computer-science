import mysql.connector
from datetime import datetime

# -----------------------------------------------------------
#  CONNECTING TO MYSQL DATABASE
# -----------------------------------------------------------
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rishav",
    database="parkingsystem"
)

cursor = con.cursor()

# -----------------------------------------------------------
#  CREATE TABLE IF NOT EXISTS
# -----------------------------------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS parking_slots (
    slot_no INT PRIMARY KEY,
    vehicle_no VARCHAR(20),
    vehicle_type VARCHAR(20),
    entry_time DATETIME,
    exit_time DATETIME,
    status VARCHAR(10)
)
""")
con.commit()

# -----------------------------------------------------------
#  FUNCTION 1: ADD NEW VEHICLE
# -----------------------------------------------------------
def park_vehicle():
    print("\n----- PARK A VEHICLE -----")
    slot = int(input("Enter available slot number: "))
    vehicle_no = input("Enter vehicle number: ")
    v_type = input("Enter vehicle type (Car/Bike): ")
    entry_time = datetime.now()

    cursor.execute("SELECT * FROM parking_slots WHERE slot_no=%s", (slot,))
    data = cursor.fetchone()

    if data:
        print("❌ Slot already exists. Use another slot.")
        return

    query = "INSERT INTO parking_slots VALUES (%s, %s, %s, %s, NULL, 'Occupied')"
    cursor.execute(query, (slot, vehicle_no, v_type, entry_time))
    con.commit()

    print("✅ Vehicle parked successfully!")

# -----------------------------------------------------------
#  FUNCTION 2: REMOVE VEHICLE / EXIT
# -----------------------------------------------------------
def vehicle_exit():
    print("\n----- VEHICLE EXIT -----")
    slot = int(input("Enter slot number of exiting vehicle: "))
    exit_time = datetime.now()

    cursor.execute("SELECT * FROM parking_slots WHERE slot_no=%s", (slot,))
    data = cursor.fetchone()

    if not data:
        print("❌ No vehicle found in this slot.")
        return

    cursor.execute("""
        UPDATE parking_slots 
        SET exit_time=%s, status='Empty', vehicle_no=NULL, vehicle_type=NULL, entry_time=NULL
        WHERE slot_no=%s
    """, (exit_time, slot))

    con.commit()
    print("🚗 Vehicle exited successfully!")

# -----------------------------------------------------------
#  FUNCTION 3: CHECK AVAILABLE SLOTS
# -----------------------------------------------------------
def show_available_slots():
    print("\n----- AVAILABLE SLOTS -----")
    cursor.execute("SELECT slot_no FROM parking_slots WHERE status='Empty' OR status IS NULL")
    rows = cursor.fetchall()

    if not rows:
        print("❌ No empty slots right now.")
    else:
        print("Empty Slots:")
        for r in rows:
            print("• Slot", r[0])

# -----------------------------------------------------------
#  FUNCTION 4: VIEW ALL PARKED VEHICLES
# -----------------------------------------------------------
def view_all():
    print("\n----- ALL PARKED VEHICLES -----")
    cursor.execute("SELECT * FROM parking_slots")
    rows = cursor.fetchall()

    if not rows:
        print("No data found.")
        return

    for r in rows:
        print("---------------------------------------------")
        print("Slot No      :", r[0])
        print("Vehicle No   :", r[1])
        print("Type         :", r[2])
        print("Entry Time   :", r[3])
        print("Exit Time    :", r[4])
        print("Status       :", r[5])
    print("---------------------------------------------")

# -----------------------------------------------------------
#  FUNCTION 5: SEARCH VEHICLE
# -----------------------------------------------------------
def search_vehicle():
    print("\n----- SEARCH VEHICLE -----")
    number = input("Enter vehicle number to search: ")

    cursor.execute("SELECT * FROM parking_slots WHERE vehicle_no=%s", (number,))
    d = cursor.fetchone()

    if d:
        print("Vehicle Found:")
        print("Slot:", d[0], "| Type:", d[2], "| Entry:", d[3])
    else:
        print("❌ Vehicle not found.")

# -----------------------------------------------------------
#  FUNCTION 6: DELETE SLOT COMPLETELY
# -----------------------------------------------------------
def delete_slot():
    print("\n----- DELETE SLOT RECORD -----")
    slot = int(input("Enter slot number to delete permanently: "))

    cursor.execute("DELETE FROM parking_slots WHERE slot_no=%s", (slot,))
    con.commit()

    print("🗑 Slot record deleted.")

# -----------------------------------------------------------
#  MAIN MENU LOOP
# -----------------------------------------------------------
while True:
    print("\n========== PARKING MANAGEMENT SYSTEM ==========")
    print("1. Park a Vehicle")
    print("2. Exit Vehicle")
    print("3. Show Available Slots")
    print("4. View All Vehicles")
    print("5. Search a Vehicle")
    print("6. Delete a Slot")
    print("7. Exit Program")
    
    choice = input("\nEnter your choice: ")

    if choice == '1':
        park_vehicle()
    elif choice == '2':
        vehicle_exit()
    elif choice == '3':
        show_available_slots()
    elif choice == '4':
        view_all()
    elif choice == '5':
        search_vehicle()
    elif choice == '6':
        delete_slot()
    elif choice == '7':
        print("Thank you for using the system!")
        break
    else:
        print("Invalid choice! Try again.")
