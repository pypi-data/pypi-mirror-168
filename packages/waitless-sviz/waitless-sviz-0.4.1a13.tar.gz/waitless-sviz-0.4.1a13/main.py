import utime as time
import uasyncio as asyncio
import machine

from configure import *
from lcd_i2c_printer import *
from urbanbus import bus_service
        
text_added      = 'Powered by welbits.com'

# Read de configuration files                       
config          = read_config_file()
config_client   = config['configuration']['network']['client']
stopid          = config['settings']['stopid']

# Boot message sequence
name  = config['about']['name']
model = config['about']['model']

print_on_lcd(name)
time.sleep(1)
print_on_lcd(name, 'Model: '+ model)
time.sleep(2)
moving_message(text_added,
               1,
               0.2,
               config['about']['name'].center(I2C_NUM_COLS),
               4.8)

# Attempting to connect network

waiting_message('Conectando Wi-Fi')

try:
    wifi_client = start_wifi(config_client['ssid'],
                             config_client['password'],
                             'client')
    
    print("Status: ",wifi_client.status())
    
    if wifi_client.status() != 3: # Trigger setup
        raise OSError('ssid is empty')
    
    else: # Allow change stop id during x time
        
        waiting_message("Elija parada")
        time.sleep(2)
        
        init_server('/save_stopid')
        task1 = waiting_for_config(60, 'IP: ' + wifi_client.ifconfig()[0])
        task2 = asyncio.start_server(serve_client, '0.0.0.0', 80)
        
        asyncio.run(asyncio.gather(task1, task2))
        
        stopid = read_config_file()['settings']['stopid']
        
except OSError: # As can't connect let entry to setup page

    wifi_connected = False
    
    while not wifi_connected:
        waiting_message('Configurando')
        
        net_name        = config['configuration']['network']['ap']['ssid']
        psswrd          = config['configuration']['network']['ap']['password']
        
        access_point    = start_wifi(net_name, psswrd, 'ap')

##################################################################33
        
        init_server('/save_wifi', access_point.scan())
        
        #           0123456789ABCDEF
        msg     = ['Configure su ',
                   'dispositivo:',
                   'Conecte a SSID' ,
                   config['about']['name'],
                   'con contrase\356a:',
                   config['configuration']['network']['ap']['password'],
                   'Navegue a:',
                   access_point.ifconfig()[0]
                  ]
               
        task1 = info_during_setup(msg)
        task2 = asyncio.start_server(serve_client, '0.0.0.0', 80)

        tasks = asyncio.gather(task1,task2)
            
        asyncio.run(tasks)                        

        waiting_message('Conectando Wi-Fi')        
 #####################################################################       
        print(access_point.ifconfig())   

        time.sleep(3)
   
        access_point.active(False); access_point.deinit(); del access_point
          
        config_client = read_config_file()['configuration']['network']['client']
        time.sleep(3)
        wifi_client   = start_wifi(config_client['ssid'],
                                   config_client['password'],
                                   'client')
        
        if wifi_client.status() == 3:
            wifi_connected = True
            
        wifi_client.status()
        print ('Status: ' + str(wifi_client.status()))

    stopid = read_config_file()['settings']['stopid']
    
waiting_message('Buscando datos')
     
try : #Para la fase de desarrollo
    bus_service()
    
    
finally:
    wifi_client.active(False); wifi_client.deinit() ; del wifi_client #No conecta AP en la segunda ejecución