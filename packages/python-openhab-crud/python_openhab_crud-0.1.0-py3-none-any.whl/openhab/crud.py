import requests
import json
import time
import base64
from datetime import datetime

class CRUD(object):
    def __init__(self, url:str, username:str = None, password:str = None):
        self.url = url
        self.username = username
        self.password = password
        self.isCloud = False
        self.isLoggedIn = False

        self.itemTypes = ["Color", "Contact", "DateTime", "Dimmer", "Group", "Image", "Location", "Number", "Player", "Rollershutter", "String", "Switch"]

        self.session = requests.Session()

        if self.username is not None and self.password is not None:
            self.auth = (self.username, self.password)
            self.session.auth = self.auth
        else:
            self.auth = None
            self.session.auth = None

        self.__login()

    def __login(self):
        if self.url == "https://myopenhab.org" or self.url == "https://myopenhab.org/":
            self.url = "https://myopenhab.org"
            self.isCloud = True
            url = self.url
        else:
            if self.url[-1] == "/":
                self.url = self.url[:-1]
            self.isCloud = False
            url = self.url + "/rest"

        try:
            login_response = self.session.get(url, auth=self.auth, timeout=8)
            login_response.raise_for_status()

            if login_response.ok or login_response.status_code == 200:
                self.isLoggedIn = True
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    def __checkItemType(self, type:str):
        if type in self.itemTypes:
            return True
        return False

    def __checkItemValue(self, type:str, value):
        bool = False

        if type == self.itemTypes[0]:
            bool = self.__checkColorValue(value)
        elif type == self.itemTypes[1]:
            bool = self.__checkContactValue(value)
        elif type == self.itemTypes[2]:
            bool = self.__checkDateTimeValue(value)
        elif type == self.itemTypes[3]:
            bool = self.__checkDimmerValue(value)
        elif type == self.itemTypes[4]:
            bool = self.__checkGroupValue(value)
        elif type == self.itemTypes[5]:
            bool = self.__checkImageValue(value)
        elif type == self.itemTypes[6]:
            bool = self.__checkLocationValue(value)
        elif type == self.itemTypes[7]:
            bool = self.__checkNumberValue(value)
        elif type == self.itemTypes[8]:
            bool = self.__checkPlayerValue(value)
        elif type == self.itemTypes[9]:
            bool = self.__checkRollershutterValue(value)
        elif type == self.itemTypes[10]:
            bool = self.__checkStringValue(value)
        elif type == self.itemTypes[11]:
            bool = self.__checkSwitchValue(value)

        return bool


    def __checkColorValue(self, value):
        if isinstance(value, str):
            if value == "ON" or value == "OFF" or value == "INCREASE" or value == "DECREASE":
                return True
            else:
                value = value.replace(" ", "")
                splitted = value.split(",")
                hue = float(splitted[0])
                saturation = float(splitted[1])
                brightness = float(splitted[2])
                if isinstance(hue, float) or isinstance(saturation, float) or isinstance(brightness, float):
                    if (0 <= hue <= 360.0) and (0 <= saturation <= 255.0) and (0 <= brightness <= 255.0):
                        return True
                    return False
                return False
        elif isinstance(value, int):
            if 0 <= value <= 100:
                return True
            return False
        return False

    def __checkContactValue(self, value):
        if isinstance(value, str):
            if value == "OPEN" or value == "CLOSED":
                return True
            return False
        return False

    def __checkDateTimeValue(self, value):
        if isinstance(value, str):
            if value != datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").strftime('%Y-%m-%dT%H:%M:%SZ'):
                return True
            return False
        return False

    def __checkDimmerValue(self, value):
        if isinstance(value, str):
            if value == "ON" or value == "OFF" or value == "INCREASE" or value == "DECREASE":
                return True
            return False
        elif isinstance(value, int):
            if 0 <= value <= 100:
                return True
            return False

    def __checkGroupValue(self, value):
        if isinstance(value, str):
            return True
        return False

    def __checkImageValue(self, value):
        if base64.b64decode(value, validate=True) == True:
            return True
        return False

    def __checkLocationValue(self, value):
        if isinstance(value, str):
            value = value.replace(" ", "")
            splitted = value.split(",")
            latitude = float(splitted[0])
            longitude = float(splitted[1])
            altitude = float(splitted[2])
            if isinstance(latitude, float) or isinstance(longitude, float) or isinstance(altitude, float):
                return True
            return False
        return False

    def __checkNumberValue(self, value):
        if isinstance(value, int) or isinstance(value, float):
            return True
        return False

    def __checkPlayerValue(self, value):
        if value == "PLAY" or value == "PAUSE" or value == "NEXT" or value == "PREVIOUS" or value == "REWIND" or value == "FASTFORWARD":
            return True
        return False

    def __checkRollershutterValue(self, value):
        if isinstance(value, str):
            if value == "UP" or value == "DOWN" or value == "STOP" or value == "MOVE":
                return True
            return False
        elif isinstance(value, int):
            if 0 <= value <= 100:
                return True
            return False

    def __checkStringValue(self, value):
        if isinstance(value, str):
            return True
        return False

    def __checkSwitchValue(self, value):
        if value == "ON" or value == "OFF":
            return True
        return False

    def __executeRequest(self, header:dict = None, resource_path:str = None, method:str = None, data = None):
        if resource_path is not None and method is not None:
            method = method.lower()
            self.session.headers.update(header)
            try:
                if method == "get":
                    response = self.session.get(self.url + resource_path, auth=self.auth, timeout=5)
                    response.raise_for_status()

                    if response.ok or response.status_code == 200:
                        if "/state" in resource_path or resource_path.find("/state") != -1:
                            return response.text
                        return json.loads(response.text)
                elif method == "put":
                    response = self.session.put(self.url + resource_path, auth=self.auth, data=data, timeout=5)
                    response.raise_for_status()

                    return None
                elif method == "post":
                    response = self.session.post(self.url + resource_path, auth=self.auth, data=data, timeout=5)
                    response.raise_for_status()

                    return None
                elif method == "delete":
                    response = self.session.delete(self.url + resource_path, auth=self.auth, timeout=5)
                    response.raise_for_status()

                    return None
                else:
                    raise ValueError('The entered http method is not valid for accessing the rest api!')
            except requests.exceptions.HTTPError as errh:
                print(errh)
            except requests.exceptions.ConnectionError as errc:
                print(errc)
            except requests.exceptions.Timeout as errt:
                print(errt)
            except requests.exceptions.RequestException as err:
                print(err)
        else:
            raise ValueError('You have to enter a valid resource path for accessing the rest api!')

    def getAllItems(self):
        headers = {"Content-type": "application/json"}
        resource_path = "/rest/items"
        method = "get"

        return self.__executeRequest(headers, resource_path, method)

    def create(self, name:str, type:str, label:str = None, groupNames = None, state = None):
        if self.isCloud:
            raise Exception("Using the Create method is not supported if you are using the cloud. Please work with the local instance.")
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        resource_path = "/rest/items/" + name
        method = "put"

        if self.__checkItemType(type) == True:
            data = {"type": type, "name": name}
        else:
            raise ValueError(f"The item type does not exists. The item {name} cannot be created.")

        if label is not None:
            data.update({"label": label})

        if groupNames is not None:
            data.update({"groupNames": groupNames})

        if state is not None:
            if self.__checkItemValue(type, state) == True:
                data.update({"state": state})

        data = json.dumps(data)

        self.__executeRequest(headers, resource_path, method, data)

    def read(self, name:str):
        headers = {"Content-type": "application/json"}
        resource_path = "/rest/items/" + name
        method = "get"

        return self.__executeRequest(headers, resource_path, method)

    def update(self, name:str, value, openhab_method:str):
        if openhab_method == "sendCommand":
            self.sendCommand(name, value)
        else: ## defaulting to postUpdate
            self.postUpdate(name, value)

    def delete(self, name:str):
        if self.isCloud:
            raise Exception("Using the Delete method is not supported if you are using the cloud. Please work with the local instance.")
        headers = {"Content-type": "application/json"}
        resource_path = "/rest/items/" + name
        method = "delete"

        self.__executeRequest(headers, resource_path, method)

    def getState(self, name:str):
        headers = {"Content-type": "application/json"}
        resource_path = "/rest/items/" + name + "/state"
        method = "get"

        return self.__executeRequest(headers, resource_path, method)

    def postUpdate(self, name:str, value, type:str = None, validate:bool = None):
        headers = {"Content-type": "text/plain; charset=utf-8", "Accept": "text/plain"}
        resource_path = "/rest/items/" + name + "/state"
        method = "put"

        if validate:
            item = self.read(name)
            type = item.get("type")

            if self.__checkItemValue(type, value) == True:
                data = value
            else:
                data = None
        else:
            if type is not None:
                if self.__checkItemType(type) == True:
                    data =  value
                else:
                    data = None
            else:
                data = value

        self.__executeRequest(headers, resource_path, method, data)

    def sendCommand(self, name:str, value, type:str = None, validate:bool = None):
        headers = {"Content-type": "text/plain; charset=utf-8", "Accept": "text/plain"}
        resource_path = "/rest/items/" + name
        method = "post"

        if validate:
            item = self.read(name)
            type = item.get("type")

            if self.__checkItemValue(type, value) == True:
                data = value
            else:
                data = None
        else:
            if type is not None:
                if self.__checkItemType(type) == True:
                    data =  value
                else:
                    data = None
            else:
                data = value

        self.__executeRequest(headers, resource_path, method, data)

    def close(self):
        self.session.post(url=self.url, headers={'Connection':'close'})
