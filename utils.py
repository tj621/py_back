#coding=utf-8
__author__ = 'Zxh'


def get_db_indoor(rows):
    response_json = '''{
                    '''
    temp_response = ''''''
    for row in rows:

        temp_json = '''"%s":{
                    ''' % str(i + 1)
        sql = 'select * from indoor where ' + 'node_number is ' + "'" + str(
            i + 1) + "'" + ' and update_time >= ' + '''"''' + start_time + '''"'''
        rv = query_db_2(sql)
        for row in rv:
            temp = '''"%s": {
                        "temperature": "%s",
                        "humidity": "%s",
                        "radiation": "%s",
                        "co2": "%s",
                        "update_time": "%s"
                        }''' % (row[0], row[3], row[4], row[5], row[6], row[2])
            temp = temp + ','
            temp_json = temp_json + temp
        temp_json = list(temp_json)
        temp_json.pop()
        temp_json = "".join(temp_json)
        temp_json = temp_json + '''},'''
        response_json = response_json + temp_json
        temp_response = temp_response + temp_json
    response_json = list(response_json)
    response_json.pop()
    response_json = "".join(response_json)
    response_json = response_json + '}'
    print 'get indoor data success from arm database'
    return response_json

