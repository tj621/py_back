from control import Control

c = Control()
print "roof vent south", c.get_roof_vent_south()
print "roof vent north", c.get_roof_vent_north()
print "side vent", c.get_side_vent()
print "shade screen out", c.get_shade_screen_out()
print "shade screen in", c.get_shade_screen_in()
print "thermal screen", c.get_thermal_screen()
print "cooling pad", c.get_cooling_pad()
print "fogging", c.get_fogging()
print "heating", c.get_heating()
print "co2", c.get_co2()
print "lighting 1", c.get_lighting_1()
print "lighting 2", c.get_lighting_2()
print "irrigation", c.get_irrigation()

print dir(c)
