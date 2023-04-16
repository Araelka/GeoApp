typename = ['Water Content, m³/m³', 'Current, mA', 'PAR, µmol/m²/s', 'Temperature Air, °C', 'RH, %', 
                    'Wind Speed, mph', 'Gust Speed, mph', 'Wind Direction,  ø', 'Temperature Ground, °C',
                    'Pressure, Hg', 'Rain', 'Solar Radiation, W/m²']
        
tablename = ['water_content', 'current', 'PAR', 'temperature_air', 'RH', 
                     'wind_speed', 'gust_speed', 'wind_direction', 'temperature_ground',
                     'pressure', 'rain', 'solar_radiation']
        
typetb = {}
typetb['Все'] = 'Все'
j = 0
for i in typename:
    typetb[i] = tablename[j]
    j +=1
for i in typetb:
    print(i)


# print(typetb)