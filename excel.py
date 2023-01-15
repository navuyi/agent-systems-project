
from datetime import datetime
import xlsxwriter


def generate_csv_file_for_simulation(humans_internal_data, occupancy_rate, steps_to_leave):
    now = datetime.now()
    dt_string = now.strftime('%H_%M_%S')
    workbook = xlsxwriter.Workbook("Simulation_{}.xlsx".format(dt_string))
    for hid in humans_internal_data:
        worksheet = workbook.add_worksheet(name=hid[0]['name'])
        for index in range(len(hid)):
            worksheet.write(index, 0, hid[index]['name'])
            worksheet.write(index, 1, hid[index]['type'])
            worksheet.write(index, 2, hid[index]['steps_taken'])
            worksheet.write(index, 3, hid[index]['distance_to_panic'])
            worksheet.write(index, 4, hid[index]['crowd_density'])

    workbook.close()
