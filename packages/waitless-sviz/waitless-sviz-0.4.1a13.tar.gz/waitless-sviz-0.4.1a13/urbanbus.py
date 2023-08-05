
def url(stopid): 
    return 'https://api.interurbanos.welbits.com/v1/stop/' + stopid


#Call to API and get json data
def call_for_data(url):
    try:
        import urequests as requests
    except ImportError:
        import requests
    r           = requests.get(url = url)
    json_data   = r.json() #r.text.json()
    status_code = r.status_code
    #print('Testeo si ejecuta r.close')
    r.close()
    return json_data, status_code


def how_much_to(value):
    import utime as time
    
    h, m     = int(value[0]), int(value[1])
    now      = time.localtime()
    after    = list(now)

    if now[3] >= h:
        if now[4] >= m:
            after[2] = after[2] + 1
    after[3],after[4] = h, m
    
    return time.mktime(tuple(after)) - time.time()


#Filter for the next arrival for each line
def sel_next_bus_each_line(api_data):
    import utime as time
    
    next_bus = [] ; control = []
    
    for i in api_data['lines']:
        if i['lineNumber'] not in control:
            next_bus.append([i['lineNumber'],i['waitTime']])
            control.append(i['lineNumber'])
            if all(list(map(lambda a: ':' in a[1], next_bus))):
                next_bus.sort(key = lambda x: int(x[1].replace(':','')))
                first_bus_time = next_bus[0][1].split(':')
                delay = how_much_to(first_bus_time) - 30 * 60
                time.sleep(delay)
                
    return next_bus  # output: list


#Manage the behaivor according to the API response
def handle_api_responses(schedule, HTTPResponseCode): # Llamar con callForData(url(stopid))
    import utime as time
    from lcd_i2c_printer import show_wait_time, waiting_message, moving_message
    
    global count_500
    break_while = False
    
    if HTTPResponseCode == 200:
        count_500 = 0
        delay = 60

        arrivals = sel_next_bus_each_line(schedule)
        delay = show_wait_time(arrivals, delay)
                       
    elif HTTPResponseCode == 404:
        print("Connection Failed. Code: " + str(HTTPResponseCode))
        moving_message('Reinicie el dispositivo y configure parada',
           1,
           0.2,
           'Parada erronea!',
           10
           )
        break_while = True
        
    elif HTTPResponseCode == 500:
        
        print("Connection Failed. Code: " + str(HTTPResponseCode))
        
        if count_500 < 10:               
            delay = 10
                
        else:
        
            waiting_message('Server Error:   Espere')
            delay = 300
        
        count_500 += 1
    
    else:
        waiting_message('Error. Reinicie')
        break_while = True
           
    time.sleep(delay)
    return break_while


#Launch the bus service
def bus_service():
    from configure import read_config_file
    
    global count_500
    count_500 = 0
    stopid = read_config_file()['settings']['stopid']
    
    while True:
        schedule, HTTPResponseCode = call_for_data(url(stopid))
        break_while = handle_api_responses(schedule, HTTPResponseCode)
        if break_while == True:
            break

