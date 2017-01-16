# coding=utf-8
'''

@author: Zxh
'''
from flask import Flask, g
import sqlite3
import os
from currenttime import get_current_time
from parameter import Parameter
from indoor import Indoor
from outdoor import Outdoor
from control import Control

app = Flask(__name__)

save_days = 10
indoor_data_count = save_days * 24 * 12
outdoor_data_count = save_days * 24 * 12
para_data_count = 30
node_number = 8

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'greenhouse.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def close_db():
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def save_db_indoor(Indoor):
    with app.app_context():
        db = get_db()
        db.execute('INSERT INTO indoor(node_number,update_time,temperature,humidity,radiation,co2) VALUES(?,?,?,?,?,?)',
                   [Indoor.get_name(), Indoor.get_update_time(), Indoor.get_temperature(), Indoor.get_humidity(),
                    Indoor.get_radiation(), Indoor.get_co2()])
        db.commit()
        db.close()
    print 'indoor save success'

def delete_db_data(value):
    with app.app_context():
        db=get_db()
        sql='''delete from %s;'''%value
        db.execute(sql)
        sql='''select * from sqlite_sequence;'''
        db.execute(sql)
        sql="update sqlite_sequence set seq=1 where name= '" + value+"'"
        db.execute(sql)
        db.commit()
        db.close()

def get_db_indoor(start_time):
    with app.app_context():
        response_json = '''{
                        '''
        temp_response = ''''''
        for i in range(node_number):
            # print temp_response
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


def get_db_outdoor(start_time):
    with app.app_context():
        response_json = '''{ "outdoor":{
                       '''
        sql = 'select * from outdoor where update_time >= ' + '''"''' + start_time + '''"'''
        rv = query_db_2(sql)
        for row in rv:
            temp = '''"%s": {
			        "temperature": "%s",
		        	"humidity": "%s",
		        	"radiation": "%s",
			        "co2": "%s",
		        	"wind_direction": "%s",
			        "wind_speed": "%s",
			        "rain": "%s",
			        "atmosphere": "%s",
		        	"update_time": "%s"
		        	}
            ''' % (row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[1])
            temp = temp + ','
            response_json = response_json + temp
        response_json = list(response_json)
        response_json.pop()
        response_json = "".join(response_json)
        response_json = response_json + '}}'
        print 'get outdoor data success from arm database'
        return response_json


def get_db_control():
    print 'get control data success from arm database'


def save_db_outdoor(Outdoor):
    with app.app_context():
        db = get_db()
        db.execute('INSERT INTO outdoor(update_time,temperature,humidity,radiation,co2,wind_direction,wind_speed,rain_snow,atmosphere)\
                   VALUES(?,?,?,?,?,?,?,?,?)',
                   [Outdoor.get_update_time(), Outdoor.get_temperature(), Outdoor.get_humidity(), Outdoor.get_radiation(),
                    Outdoor.get_co_2(),
                    Outdoor.get_wind_direction(), \
                    Outdoor.get_wind_speed(), Outdoor.get_rain(), Outdoor.get_atmosphere()])
        db.commit()
        db.close()
    print 'outdoor save success'


def save_db_control(Control):
    with app.app_context():
        db = get_db()
        db.execute('INSERT INTO control_state(update_time,roof_vent_south,roof_vent_north,side_vent,shade_screen_north,shade_screen_south,thermal_screen,\
        cooling_pump,cooling_fan,fan,fogging,heating,co2,lighting_1,lighting_2,irrigation) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                   [Control.get_update_time(), Control.get_roof_vent_south(), Control.get_roof_vent_north(),
                    Control.get_side_vent(), Control.get_shade_screen_north(), Control.get_shade_screen_south(), \
                    Control.get_thermal_screen(), Control.get_cooling_pump(), Control.get_cooling_fan(),
                    Control.get_fan(), Control.get_fogging(),
                    Control.get_heating(), Control.get_co2(), Control.get_lighting_1(), Control.get_lighting_2(),
                    Control.get_irrigation()])
        db.commit()
        db.cursor().close()
        db.close()
    print 'control save success'


def save_db_parameter(Parameter):
    with app.app_context():
        db = get_db()
        db.execute('INSERT INTO parameter(update_time,time1,temperature1,time2,temperature2,time3,temperature3,time4,temperature4, co2_upper_limit,co2_lower_limit, cooling_start_temperature,cooling_stop_temperature,\
                    expect_humidity,humidity_influence_range_of_air_temperature,low_humidity_influence_on_air_temperature,high_humidity_influence_on_air_temperature,expect_light,light_influence_on_air_temperature_slope,high_light_influence_on_temperature,low_light_influence_on_temperature,frost_temperature,\
                    indoor_temperature_lower_limit,roof_vent_wind_speed_upper_limit,roof_vent_rain_upper_limit, heating_start_lowest_temperature,heating_stop_highest_temperature, month_to_open_thermal_screen,month_to_close_thermal_screen,time_to_open_thermal_screen,time_to_close_thermal_screen, temperature_to_open_side,\
                    wait_time_to_open_side,rain_upper_limit_to_close, upper_limit_light_to_open_shade_screen_out,upper_limit_light_to_open_shade_screen_in,soil_humidity_to_start_irrigation,soil_humidity_to_stop_irrigation,temperature_to_open_fogging,temperature_to_open_cooling_pad,\
                    month_to_open_lighting,month_to_close_lighting,period1_start_lighting,period1_stop_lighting,period2_start_lighting,period2_stop_lighting,radiation1_to_open_lighting,radiation2_to_open_lighting,roof_vent_open_time,side_vent_open_time,shade_screen_out_open_time,\
                    shade_screen_in_open_time,thermal_screen_open_time ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', \
                   [Parameter.get_update_time(), Parameter.get_time_1(), Parameter.get_temperature_1(),
                    Parameter.get_time_2(), Parameter.get_temperature_2(), Parameter.get_time_3(),
                    Parameter.get_temperature_3(), Parameter.get_time_4(), Parameter.get_temperature_4(),
                    Parameter.get_co_2_upper_limit(), Parameter.get_co_2_lower_limit(),
                    Parameter.get_cooling_start_temperature(), Parameter.get_cooling_stop_temperature(),
                    Parameter.get_expect_humidity(), Parameter.get_humidity_influence_range_of_air_temperature(),
                    Parameter.get_low_humidity_influence_on_air_temperature(),
                    Parameter.get_high_humidity_influence_on_air_temperature(), Parameter.get_expect_light(),
                    Parameter.get_light_influence_on_air_temperature_slope(),
                    Parameter.get_high_light_influence_on_temperature(),
                    Parameter.get_low_light_influence_on_temperature(), Parameter.get_frost_temperature(),
                    Parameter.get_indoor_temperature_lower_limit(), Parameter.get_roof_vent_wind_speed_upper_limit(),
                    Parameter.get_roof_vent_rain_upper_limit(),
                    Parameter.get_heating_start_lowest_temperature(), Parameter.get_heating_stop_highest_temperature(),
                    Parameter.get_month_to_open_thermal_screen(), Parameter.get_month_to_close_thermal_screen(),
                    Parameter.get_time_to_open_thermal_screen(), Parameter.get_time_to_close_thermal_screen(),
                    Parameter.get_temperature_to_open_side(),
                    Parameter.get_wait_time_to_open_side(),
                    Parameter.get_rain_upper_limit_to_close(),
                    Parameter.get_upper_limit_light_to_open_out_shade_screen(),
                    Parameter.get_upper_limit_light_to_open_in_shade_screen(),
                    Parameter.get_soil_humidity_to_start_irrigation(),
                    Parameter.get_soil_humidity_to_stop_irrigation(),
                    Parameter.get_temperature_to_open_fogging(),
                    Parameter.get_temperature_to_open_cooling_pad(),
                    Parameter.get_month_to_open_lighting(),
                    Parameter.get_month_to_close_lighting(),
                    Parameter.get_period_1_start_lighting(),
                    Parameter.get_period_1_stop_lighting(),
                    Parameter.get_period_2_start_lighting(),
                    Parameter.get_period_2_stop_lighting(),
                    Parameter.get_radiation_1_to_open_lighting(),
                    Parameter.get_radiation_2_to_open_lighting(),
                    Parameter.get_roof_vent_open_time(),
                    Parameter.get_side_vent_open_time(),
                    Parameter.get_shade_screen_out_open_time(),
                    Parameter.get_shade_screen_in_open_time(),
                    Parameter.get_thermal_screen_open_time()
                   ])
        db.commit()
        db.cursor().close()
        db.close()
    print 'parameter save success'


def get_db_parameter(Parameter):
    query = 'select * from parameter where id=(select max(id) from parameter)'
    try:
        row = query_db_1(query)
        a = 2
        Parameter.set_update_time(row[1])
        Parameter.set_time_1(row[a])
        Parameter.set_temperature_1(row[a + 1])
        Parameter.set_time_2(row[a + 2])
        Parameter.set_temperature_2(row[a + 3])
        Parameter.set_time_3(row[a + 4])
        Parameter.set_temperature_3(row[a + 5])
        Parameter.set_time_4(row[a + 6])
        Parameter.set_temperature_4(row[a + 7])

        Parameter.set_co_2_upper_limit(row[a + 8])
        Parameter.set_co_2_lower_limit(row[a + 9])
        Parameter.set_cooling_start_temperature(row[a + 10])
        Parameter.set_cooling_stop_temperature(row[a + 11])

        Parameter.set_expect_humidity(row[a + 12])
        Parameter.set_humidity_influence_range_of_air_temperature(row[a + 13])
        Parameter.set_low_humidity_influence_on_air_temperature(row[a + 14])
        Parameter.set_high_humidity_influence_on_air_temperature(row[a + 15])
        Parameter.set_expect_light(row[a + 16])
        Parameter.set_light_influence_on_air_temperature_slope(row[a + 17])
        Parameter.set_high_light_influence_on_temperature(row[a + 18])
        Parameter.set_low_light_influence_on_temperature(row[a + 19])
        Parameter.set_frost_temperature(row[a + 20])
        Parameter.set_indoor_temperature_lower_limit(row[a + 21])
        Parameter.set_roof_vent_wind_speed_upper_limit(row[a + 22])
        Parameter.set_roof_vent_rain_upper_limit(row[a + 23])

        Parameter.set_heating_start_lowest_temperature(row[a + 24])
        Parameter.set_heating_stop_highest_temperature(row[a + 25])

        Parameter.set_month_to_open_thermal_screen(row[a + 26])
        Parameter.set_month_to_close_thermal_screen(row[a + 27])
        Parameter.set_time_to_open_thermal_screen(row[a + 28])
        Parameter.set_time_to_close_thermal_screen(row[a + 29])

        Parameter.set_temperature_to_open_side(row[a + 30])
        Parameter.set_wait_time_to_open_side(row[a + 31])
        Parameter.set_rain_upper_limit_to_close(row[a + 32])

        Parameter.set_upper_limit_light_to_open_out_shade_screen(row[a + 33])
        Parameter.set_upper_limit_light_to_open_in_shade_screen(row[a + 34])
        Parameter.set_soil_humidity_to_start_irrigation(row[a + 35])
        Parameter.set_soil_humidity_to_stop_irrigation(row[a + 36])
        Parameter.set_temperature_to_open_fogging(row[a + 37])
        Parameter.set_temperature_to_open_cooling_pad(row[a + 38])

        Parameter.set_month_to_open_lighting(row[a + 39])
        Parameter.set_month_to_close_lighting(row[a + 40])
        Parameter.set_period_1_start_lighting(row[a + 41])
        Parameter.set_period_1_stop_lighting(row[a + 42])
        Parameter.set_period_2_start_lighting(row[a + 43])
        Parameter.set_period_2_stop_lighting(row[a + 44])
        Parameter.set_radiation_1_to_open_lighting(row[a + 45])
        Parameter.set_radiation_2_to_open_lighting(row[a + 46])

        Parameter.set_roof_vent_open_time(row[a + 47])
        Parameter.set_side_vent_open_time(row[a + 48])
        Parameter.set_shade_screen_out_open_time(row[a + 49])
        Parameter.set_shade_screen_in_open_time(row[a + 50])
        Parameter.set_thermal_screen_open_time(row[a + 51])
        return Parameter.build_to_json()
    except:
        print 'database has no data'
    print 'get parameter success'


def query_db_1(query, args=(), one=True):
    with app.app_context():
        cur = get_db().execute(query, args)
        rv = cur.fetchone()
        cur.close()
        get_db().close()
        return rv


def query_db_2(query, args=(), one=False):
    with app.app_context():
        cur = get_db().execute(query, args)
        rv = cur.fetchall()
        cur.close()
        get_db().close()
        return rv


if __name__ == '__main__':
    # delete_db_data('parameter')
    # start_time="2016-09-18 22:22:22"
    # get_db_outdoor(start_time)
    init_db()
    # for i in range(8):
    #     indoor = Indoor(i + 1)
    #     save_db_indoor(indoor)
    # outdoor = Outdoor()
    # save_db_outdoor(outdoor)
    # c = Control()
    # save_db_control(c)
    p=Parameter()
    save_db_parameter(p)
    # query='select * from parameter where id=(select max(id) from parameter)'
    # print query_db_1(query)
    # get_db_parameter(p)
    # print p.get_co2_lower_liqmit()
# out=Outdoor()
# with app.app_context():
#          db=get_db()
#          db.execute('''insert into outdoor(update_time,temperature,humidity,radiation,co2,wind_direction,wind_speed,rain_snow,atmosphere)\
#                         values(?,?,?,?,?,?,?,?,?)''', [out.update_time,out.temperature,out.humidity,out.radiation,out.co2,out.wind_direction,\
#                                                      out.wind_speed,out.rain,out.atmosphere])
#          db.commit()
#      print(out.classtoJson())
