from thonny import THONNY_USER_DIR, get_workbench

#Default config
DEFAULT_PATH = THONNY_USER_DIR+"/LoggingPlugin/"
DEFAULT_SERVER = 'http://127.0.0.1:8000' #'http://localhost:8081' 
DEFAULT_STORE = True
DEFAULT_SEND = False
DEFAULT_LOG_IN_CONSOLE = False

URL_TERMS_OF_USE = "https://www.fil.univ-lille.fr/~L1S1Info/last/collecte_donnees_thonny.pdf"

#Dict of options name and default value
OPTIONS = {
    "local_path" : DEFAULT_PATH,
    "server_address" : DEFAULT_SERVER,
    "store_logs" : DEFAULT_STORE,
    "log_in_console" : DEFAULT_LOG_IN_CONSOLE,
    "send_logs" : DEFAULT_SEND,
    "first_run" : True,
}

#Get the thonny workbench object
WB = get_workbench()
