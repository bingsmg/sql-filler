import re


def read_sql_log(path):
    with open(path, 'r') as file:
        sql_log = file.read()
    return sql_log


def write_sql_output(sql_result):
    with open('result.sql', 'w') as file:
        file.write(sql_result)


def process_params_list(parameter_list):
    result = []
    for value in parameter_list:
        if value.lower() == 'null':
            result.append('null')
        elif value.isdigit():
            result.append(value)
        else:
            result.append(f"'{value}'")
    return result


if __name__ == '__main__':
    sql_content = read_sql_log("demo.sql")
    # print(sql_content)

    sql_body_pattern = re.compile(r'(insert|update|select).*?values \(\?.*?\);', re.DOTALL)
    sql_body_match = sql_body_pattern.search(sql_content)
    sql_body = sql_body_match.group(0) if sql_body_match else ''
    # print(sql_body)

    sql_parameters_pattern = re.compile(r'parameter is \[(.+?)]', re.DOTALL)
    sql_parameters_match = sql_parameters_pattern.search(sql_content)
    sql_parameters = sql_parameters_match.group(0) if sql_parameters_match else ''
    # print(sql_parameters)

    sql_parameters = sql_parameters[sql_parameters.find('[') + 1: sql_parameters.find(']')]
    parameter_list = [item.split(":")[1] for item in sql_parameters.split(";")] if sql_parameters else None
    # print(parameter_list)

    sql = sql_body.replace('?', '{}').format(*process_params_list(parameter_list))
    write_sql_output(sql)
