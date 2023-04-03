import configparser
import hashlib

from utils.data_models import Config

activity_filter_out = ["Senderismo","Senderismo Urbano"]

activity_kind_mapper = {
"Acto Institucional":"Acto",
"Alpinismo-Alta Montaña":"Alp",
"Bicicleta/-/BTT":"Btt",
"Carreras por Montaña":"Run",
"Curso de Formación":"Curso",
"Escalada Clasica/Deportiva/Hielo":"Climb",
"Espelelología":"Cave",
"Esquí Alpino":"Ski-Alp",
"Esquí de Fondo":"Ski-Nord",
"Esquí en Familia":"Ski-Fam",
"Esquí de montaña":"Skimo",
"Medioambiental":"Eco",
"Micología":"Setas",
"Montaña en familia":"Fam",
"Montañismo":"Mont",
"Conjunta (Montañismo-Senderismo)":"M+S",
"Proyección":"Film",
"Senderismo":"Send",
"Senderismo Cultural":"Cultural",
"Vías Ferratas":"Fer",
"Senderismo Urbano":"Urb",
"Montaña Joven":"Teen",
"Trekking-Viajes":"Trip",
"Conjunta (Alpinismo-Montañismo)":"A+N",
"Bienvenida (Salidas tuteladas)":"Tut",
"Charla / Coloquio":"Meet",
"Peque-Rutas":"Kids",
"Curso de Montañismo Basico Area de Bienvenida":"Curso",
"Actividad ON-LINE":"online",
"Montaña Senior-Salidas entre semana":"Senior",
"Informativo Semanal del Club":"Info",
"Barrancos":"Barr",
"Talleres":"Curso",
"Salidas entre Semana":"Week"}

def generate_id(string):
    return hashlib.sha256(string.encode()).hexdigest()[:8]

def get_configuration(config_path = 'config.ini', is_test = True):
    # create a new instance of the ConfigParser class
    config = configparser.ConfigParser()

    # read the configuration file
    config.read(config_path)

    if is_test:
        calendar_id = config.get('google', 'TEST_CALENDAR_ID')
    else:
        calendar_id = config.get('google', 'PROD_CALENDAR_ID')

    return Config(
        GOOGLE_CALENDAR_ID = calendar_id,
        GOOGLE_SERVICE_ACCOUNT_FILE_PATH = config.get('google', 'SERVICE_ACCOUNT_FILE'),
        TELEGRAM_CHAT_ID = config.get('telegram', 'CHAT_ID'),
        TELEGRAM_TOKEN = config.get('telegram', 'TOKEN'),
        ACTIVITY_VISITED_ACTIVITIES_PATH = config.get('activity', 'VISITED_ACTIVITIES_PATH'),
    )