
from datetime import datetime
import xlsxwriter


def generate_csv_file_for_simulation(humans_internal_data, occupancy_rate, steps_to_leave):
    now = datetime.now()
    dt_string = now.strftime('%H_%M_%S')
    workbook = xlsxwriter.Workbook("Simulation_{}.xlsx".format(dt_string))

    worksheet = workbook.add_worksheet(name='GENERAL')
    worksheet.write(0, 0, 'step_to_leave_all_humans')
    worksheet.write(1, 0, steps_to_leave)
    worksheet.write(0, 1, 'occupancy_rate')
    worksheet.write(1, 1, 'all')
    worksheet.write(1, 2, 'child')
    worksheet.write(1, 3, 'mid')
    worksheet.write(1, 4, 'senior')

    i = 2
    for oc in occupancy_rate:
        worksheet.write(i, 1, oc['all'])
        worksheet.write(i, 2, oc['child'])
        worksheet.write(i, 3, oc['mid'])
        worksheet.write(i, 4, oc['senior'])
        i += 1

    for hid in humans_internal_data:
        worksheet = workbook.add_worksheet(name=hid[0]['name'])
        worksheet.write(0, 0, 'NAME')
        worksheet.write(0, 1, 'TYPE')
        worksheet.write(0, 2, 'STEPS_TAKEN')
        worksheet.write(0, 3, 'DISTANCE_TO_PANIC_CELL')
        worksheet.write(0, 4, 'CROWD_DENSITY')
        for index in range(1, len(hid)+1):
            worksheet.write(index, 0, hid[index-1]['name'])
            worksheet.write(index, 1, hid[index-1]['type'])
            worksheet.write(index, 2, hid[index-1]['steps_taken'])
            worksheet.write(index, 3, hid[index-1]['distance_to_panic'])
            worksheet.write(index, 4, hid[index-1]['crowd_density'])

    workbook.close()
