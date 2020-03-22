from datetime import datetime


def transform_data(initial_data):
    """Formats the incoming file to a data structure we can use"""
    transformed_data = []
    for line in initial_data:
        line = line.split(',')
        line[2] = datetime.strptime(line[2], '%Y-%m-%d')
        if line[3] == 'NULL':
            line[3] = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            line[3] = datetime.strptime(line[3], '%Y-%m-%d')
        transformed_data.append(line)
    return transformed_data


def calculate_employees_workdays(final_data):
    """
    Calculates the employees working days
    """
    data_result = {}
    for employee in range(0, len(final_data)):
        employee_id, project_id, date_from, date_to = final_data[employee]
        data_result.setdefault(employee_id, {})
        for next_employee in range(employee + 1, len(final_data)):
            next_employee_id, next_project_id, next_date_from, next_date_to = final_data[next_employee]
            if employee_id == next_employee_id:
                continue
            else:
                if project_id == next_project_id:
                    data_result[employee_id].setdefault(next_employee_id, 0)
                    latest_start = max(date_from, next_date_from)
                    earliest_end = min(date_to, next_date_to)
                    days = (earliest_end - latest_start).days + 1
                    if days > 0:
                        data_result[employee_id][final_data[next_employee][0]] += days
    return data_result


def find_longest_working_pair(data):
    """
    Find the longest working pair of employees
    """
    employee_id = 0
    fellow_worker_id = 0
    max_days = 0

    for employee, value in data.items():
        for colleague, days in value.items():
            if days > max_days:
                max_days = days
                employee_id = employee
                fellow_worker_id = colleague
    return f'Employees with id {employee_id} and {fellow_worker_id} had been working ' \
           f'for the longest period of time: {max_days} days'


if __name__ == '__main__':
    with open('data_employees.txt', 'r') as file:
        file.seek(0)
        first_char = file.read(1)
        if not first_char:
            print('File is empty!')
        else:
            file.seek(0)
            file_data = file.read().split('\n')
            calculated_time = calculate_employees_workdays(transform_data(file_data))
            print(find_longest_working_pair(calculated_time))
