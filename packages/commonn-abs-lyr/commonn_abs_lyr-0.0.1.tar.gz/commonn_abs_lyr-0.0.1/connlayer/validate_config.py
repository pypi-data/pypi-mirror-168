"""Parse config dict
# @Author : kazijavedalam
"""
import constants as constants

error_msg = dict()


class ValidateConfig(object):

    @staticmethod
    def mysql_config(self, config: dict):
        try:
            print("in mysql", config)
            global error_msg
            if type(config) is dict:
                if constants.host not in config:
                    error_msg["error"] = "host name not valid"
                    return error_msg
                if constants.user not in config:
                    error_msg["error"] = "please check user name"
                    return error_msg
                if constants.password not in config:
                    error_msg["error"] = "please check password"
                    return error_msg
                if constants.database not in config:
                    error_msg["error"] = "please check database name"
                    return error_msg
        except Exception as err:
            error_msg["error"] = "error while reading mysql config:-" + err
            return error_msg
        return error_msg

    @staticmethod
    def redis_config(self, config: dict):
        try:

            global error_msg
            if type(config) is dict:
                if constants.host not in config and config[constants.host]:
                    error_msg["error"] = "host name not valid"
                    return error_msg
                if constants.port not in config:
                    error_msg["error"] = "please check port"
                    return error_msg
                if constants.database not in config:
                    error_msg["error"] = "please check database"
                    return error_msg
        except Exception as err:
            error_msg["error"] = "error while reading redis config:-" + str(err)
            return error_msg
        return error_msg

    @staticmethod
    def cosmos_config(self, config: dict):
        try:
            global error_msg
            if type(config) is dict:
                if constants.host not in config and config[constants.host]:
                    error_msg["error"] = "host name not valid"
                    return error_msg
                if constants.master_key not in config:
                    error_msg["error"] = "please check master key"
                    return error_msg
        except Exception as err:
            error_msg["error"] = "error while reading cosmos config:-" + err
            return error_msg
        return error_msg

    @staticmethod
    def postgres_config(self, config: dict):
        try:
            global error_msg
            if type(config) is dict:
                if constants.host not in config:
                    error_msg["error"] = "host name not valid"
                    return error_msg
                if constants.user not in config:
                    error_msg["error"] = "please check user name"
                    return error_msg
                if constants.password not in config:
                    error_msg["error"] = "please check password"
                    return error_msg
                if constants.database not in config:
                    error_msg["error"] = "please check database name"
                    return error_msg
        except Exception as err:
            error_msg["error"] = "error while reading postgres config:-" + err
            return error_msg
        return error_msg

    @staticmethod
    def dwh_config(self, config: dict):
        try:

            global error_msg
            if type(config) is dict:
                if constants.host not in config:
                    error_msg["error"] = "host name not valid"
                    return error_msg
                if constants.port not in config:
                    error_msg["error"] = "please check port"
                    return error_msg
                if constants.database not in config:
                    error_msg["error"] = "please check database"
                    return error_msg
                if constants.user not in config:
                    error_msg["error"] = "please check user name"
                    return error_msg
                if constants.password not in config:
                    error_msg["error"] = "please check password"
                    return error_msg
                if constants.driver not in config:
                    error_msg["error"] = "please check driver"
                    return error_msg

        except Exception as err:
            error_msg["error"] = "error while reading dwh config:-" + err
            return error_msg
        return error_msg

    @staticmethod
    def clickhouse_config(self, config: dict):
        try:
            global error_msg
            if type(config) is dict:
                if constants.host not in config:
                    error_msg["error"] = "host name not valid"
                    return error_msg
                if constants.user not in config:
                    error_msg["error"] = "please check user name"
                    return error_msg
                if constants.password not in config:
                    error_msg["error"] = "please check password"
                    return error_msg
                if constants.database not in config:
                    error_msg["error"] = "please check database name"
                    return error_msg
        except Exception as err:
            error_msg["error"] = "error while reading clickhouse config:-" + err
            return error_msg
        return error_msg
