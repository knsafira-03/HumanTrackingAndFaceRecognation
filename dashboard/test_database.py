from services.attendance_service import AttendanceService

service = AttendanceService()

print("=" * 40)
print("Attendance History")
print("=" * 40)

for row in service.get_history():

    print(row)

print()

print("Total Masuk :", service.get_total_entry())
print("Total Keluar:", service.get_total_exit())
print("Di Dalam    :", service.get_people_inside())