import json

settings_path = '/Users/leo/Projects/mc_uptime_server/app/settings.json'

def init_settings():
    settings = {
        'slot_length': 6
    }

    f = open(settings_path, 'w')
    json.dump(settings, f)
    f.close()

def get_setting(setting):
    f = open(settings_path, 'r')
    j = json.load(f)
    f.close()
    return j[setting]

def set_setting(setting, value):
    f = open(settings_path, 'r')
    j = json.load(f)
    f.close()
    j[setting] = value
    f = open(settings_path, 'w')
    json.dump(j, f)
    f.close()


if __name__ == '__main__':
    init_settings()
