

# Read the configuration on config.json file
def read_config_file():
    import ujson as json
    blank_config = """{
      "configuration": {
        "network": {
          "client": {
            "ssid": "",
            "password": ""
          },
          "ap": {
            "ssid": "WAITLESS",
            "password": "123456789"
          }
        }

      },
          "settings": {
          "transport_network": "urbanos",
          "stopid": ""
        },  
      "about": {
        "name": "WAITLESS",
        "model": "SVIZ",
        "version": "0.4.3a0"
      }
    }
    """ 
    try:
        with open('config.json') as config:
            #if config.read() != '':
            return json.loads(config.read())
            #else:
            #    raise OSError('File is empty')
    except (OSError, ValueError):
        with open('config.json','w') as config:
            config.write(blank_config)        
            return json.loads(blank_config)
        

#Starts the WiFi as client or AP    
def start_wifi(ssid, password, mode):
    import network, time
        
    if (mode == 'ap'):
        wlan = network.WLAN(network.AP_IF)
        wlan.config(essid=ssid, password=password)
        wlan.active(True)
        
    elif(mode == 'client'):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)
       
        max_wait = 10
        while max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            max_wait -= 1
            print('waiting for connection...')
            time.sleep(1)

        if wlan.status() != 3:
            #raise RuntimeError('network connection failed')
            print('network connection failed')
        else:
            print('connected')
            status = wlan.ifconfig()
            print( 'ip = ' + status[0] )
            
    return wlan


#Create a radio option for an HTML form
def html_scanned_ssid(x): #A list with SSIDs scanned
    selectString = ''

    for y in x:
        html_select ="""
            <label for=\"{0}\" class=\"form-radio\">
			<input type=\"radio\" id=\"{0}\" name=\"ssid\" value=\"{0}\" required >
			<i class=\"form-icon\"></i>{0}</label>
		"""
        selectString += html_select.format(y[0].decode())

    return selectString


#Configure parameters for asynchrounous web server
def init_server(action_form,ssids = []):
    def pass_data_server():
        return action_form, ssids
    return pass_data_server


finish_countdown = False


# Asynchronous countdown optimiezed   
async def waiting_for_config(time, message1):
    import uasyncio as asyncio
    from  lcd_i2c_printer import reset_waiting, print_on_lcd, insert_message
    figures = len(str(time))
    reset_waiting()
    message2 = str(time) + ' seg'
    
    print_on_lcd(message1, message2, False)
    
    while time > -1:
        await asyncio.sleep(1)
        insert_message(' ' * (figures - len(str(time))) + str(time) + ' seg',0,1)                         
        time -= 1
        
        global finish_countdown
        
        if finish_countdown == True:
            time = -1


# Read files by chunks, let read large files 
def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


# Manage the logic of web server according to the request
def manage_request(request_obj, form_action, ssids=[]):   
    request_str = str(request_obj)
    content_type = 'text/html'
    
    if request_str.find(form_action) ==7:
        update_config(request_obj, form_action)
        #global saved
        #saved = True
        response ='res/saved.html'
    
    elif '.css' in request_str:        
        ini = request_str.index('/css')
        fin = request_str.index('.css') + 4
        response = 'res' + request_str[ini : fin]
        content_type = 'text/css'
    
    elif '/finish' in request_str:
        #global saved
        #saved = True
        response = ''
        #raise RuntimeError
        
    else:
        if form_action == '/save_wifi':
            if ssids != []:
                temp_setup_html(ssids)
                response = 'tmp/tmp_setup.html'
            else:
                response = 'res/error_ssid.html'
                
        else:
            response = 'res/config.html'       
    print(saved)   
    return response, content_type


# Update the config.json file
def update_config(obj_request, form_action):
    import ujson as json
    
    number_of_lines = 2 
    
    if form_action == '/save_wifi':
        number_of_lines = 4

    
    request_str = str(obj_request)
    print(request_str)
            
    form_request = request_str.find(form_action)
    req_by_lines = obj_request.decode().split('\r\n')
    post_data = {}
    for line in (list(filter(None,req_by_lines[len(req_by_lines)-number_of_lines:len(req_by_lines)-1]))):
        #Mejorar captura de parámetros POST
        data_list = line.split('=')
        post_data[data_list[0]] = data_list[1]
        
    print(post_data)    
    prev_config_json = read_config_file()             
     
    with open('config.json','w') as config_json:
        if form_action == '/save_wifi':
            prev_config_json['configuration']['network']['client']['ssid']     = post_data['ssid']       
            prev_config_json['configuration']['network']['client']['password'] = post_data['password']        
        prev_config_json['settings']['stopid'] = post_data['stopid']
  
        config_json.write(json.dumps(prev_config_json))


# Create a html document joining a template along a form radio block whose which
# contains a list with SSIDs within the scope
def temp_setup_html(ssid_list):
    html_select = html_scanned_ssid(ssid_list)
    with open('res/setup.html') as f:
        readed_f = f.read()
        tmp_html = readed_f % html_select
        
    with open('tmp/tmp_setup.html','w') as f:
        f.write(tmp_html)


#################################################
def init_server(route,scanned_wifi=[]):
    global form_action, ssids
    form_action, ssids = route,scanned_wifi

        
async def serve_client(reader, writer):
    import uasyncio as asyncio
    import ujson as json
    import socket
    print('server running...')
    global virt_writer, saved

    virt_writer = writer   
    saved = False
    
    #action_form = data_server()[0]
    #form_action = '/save_stopid' OJO
    #form_action, ssids = load_data()
    
    request = await reader.read(1024)
    
    response, content_type = manage_request(request, form_action, ssids)
    
    if response == '':
        global finish_countdown
        finish_countdown = True
        #print(finish_countdown)
    
    writer.write('HTTP/1.0 200 OK\r\nContent-type: %s \r\n\r\n' % content_type) 

    try:
        with open(response) as f:
            for piece in read_in_chunks(f, 2048):
                writer.write(piece)
                print('chunk')
            print(response)
            
    except OSError:
        pass
    
    await writer.drain()
    await writer.wait_closed()
    
    print("Client disconnected")
