# @Author : kazijavedalam
import json


class CastConfig(object):
    @staticmethod
    def mysql(self, config: dict):
        try:
            f = open('defaultconfig/mysql_config.json')
            data = json.load(f)
            if config["host"] is not None:
                data["host"] = config["host"]
            if config["user"] is not None:
                data["user"] = config["user"]
            if config["password"] is not None:
                data["password"] = config["password"]
            if config["database"] is not None:
                data["database"] = config["database"]
            f.close()
            return data
        except Exception as err:
            return err

    @staticmethod
    def cosmos(self, config: dict):
        try:
            f = open('defaultconfig/cosmos_config.json')
            data = json.load(f)
            if config["host"] is not None:
                data["host"] = config["host"]
            if config["masterKey"] is not None:
                data["masterKey"] = config["masterKey"]
            f.close()
            return data
        except Exception as err:
            return err

    @staticmethod
    def redis(self, config: dict):
        try:
            f = open('defaultconfig/redis_config.json')
            data = json.load(f)
            all_keys = config.keys()
            if all_keys.__contains__("port") is not False:
                data["host"] = config["host"]
            if all_keys.__contains__("port") is not False:
                data["port"] = config["port"]
            if all_keys.__contains__("db") is not False:
                data["db"] = config["db"]
            else:
                data["db"] = 0
            if all_keys.__contains__("password") is not False:
                data["password"] = config["password"]
            else:
                data["password"] = None
            if all_keys.__contains__("socket_timeout") is not False:
                data["socket_timeout"] = config["socket_timeout"]
            else:
                data["socket_timeout"] = None

            if all_keys.__contains__("socket_connect_timeout") is not False:
                data["socket_connect_timeout"] = config["socket_connect_timeout"]
            else:
                data["socket_connect_timeout"] = None
            if all_keys.__contains__("socket_keepalive") is not False:
                data["socket_keepalive"] = config["socket_keepalive"]
            else:
                data["socket_keepalive"] = None
            if all_keys.__contains__("socket_keepalive_options") is not False:
                data["socket_keepalive_options"] = config["socket_keepalive_options"]
            else:
                data["socket_keepalive_options"] = None
            if all_keys.__contains__("connection_pool") is not False:
                data["connection_pool"] = config["connection_pool"]
            else:
                data["connection_pool"] = None
            if all_keys.__contains__("unix_socket_path") is not False:
                data["unix_socket_path"] = config["unix_socket_path"]
            else:
                data["unix_socket_path"] = None
            if all_keys.__contains__("encoding") is not False:
                data["encoding"] = config["encoding"]
            if all_keys.__contains__("encoding_errors") is not False:
                data["encoding_errors"] = config["encoding_errors"]
            if all_keys.__contains__("charset") is not False:
                data["charset"] = config["charset"]
            else:
                data["charset"] = None
            if all_keys.__contains__("errors") is not False:
                data["errors"] = config["errors"]
            else:
                data["errors"] = None
            if all_keys.__contains__("decode_responses") is not False:
                data["decode_responses"] = config["decode_responses"]
            else:
                data["decode_responses"] = False
            if all_keys.__contains__("retry_on_timeout") is not False:
                data["retry_on_timeout"] = config["retry_on_timeout"]
            else:
                data["retry_on_timeout"] = False
            if all_keys.__contains__("retry_on_error") is not False:
                data["retry_on_error"] = config["retry_on_error"]
            else:
                data["retry_on_error"] = None
            if all_keys.__contains__("ssl") is not False:
                data["ssl"] = config["ssl"]
            else:
                data["ssl"] = False
            if all_keys.__contains__("ssl_keyfile") is not False:
                data["ssl_keyfile"] = config["ssl_keyfile"]
            else:
                data["ssl_keyfile"] = None
            if all_keys.__contains__("ssl_certfile") is not False:
                data["ssl_certfile"] = config["ssl_certfile"]
            else:
                data["ssl_certfile"] = None
            if all_keys.__contains__("ssl_cert_reqs") is not False:
                data["ssl_cert_reqs"] = config["ssl_cert_reqs"]
            if all_keys.__contains__("ssl_ca_certs") is not False:
                data["ssl_ca_certs"] = config["ssl_ca_certs"]
            else:
                data["ssl_ca_certs"] = None
            if all_keys.__contains__("ssl_ca_path") is not False:
                data["ssl_ca_path"] = config["ssl_ca_path"]
            else:
                data["ssl_ca_path"] = None
            if all_keys.__contains__("ssl_ca_data") is not False:
                data["ssl_ca_data"] = config["ssl_ca_data"]
            else:
                data["ssl_ca_data"] = None
            if all_keys.__contains__("ssl_check_hostname") is not False:
                data["ssl_check_hostname"] = config["ssl_check_hostname"]
            else:
                data["ssl_check_hostname"] = False
            if all_keys.__contains__("ssl_password") is not False:
                data["ssl_password"] = config["ssl_password"]
            else:
                data["ssl_password"] = None
            if all_keys.__contains__("ssl_validate_ocsp") is not False:
                data["ssl_validate_ocsp"] = config["ssl_validate_ocsp"]
            else:
                data["ssl_validate_ocsp"] = False
            if all_keys.__contains__("ssl_validate_ocsp_stapled") is not False:
                data["ssl_validate_ocsp_stapled"] = config["ssl_validate_ocsp_stapled"]
            else:
                data["ssl_validate_ocsp_stapled"] = False
            if all_keys.__contains__("ssl_ocsp_context") is not False:
                data["ssl_ocsp_context"] = config["ssl_ocsp_context"]
            else:
                data["ssl_ocsp_context"] = None
            if all_keys.__contains__("ssl_ocsp_expected_cert") is not False:
                data["ssl_ocsp_expected_cert"] = config["ssl_ocsp_expected_cert"]
            else:
                data["ssl_ocsp_expected_cert"] = None
            if all_keys.__contains__("max_connections") is not False:
                data["max_connections"] = config["max_connections"]
            else:
                data["max_connections"] = None
            if all_keys.__contains__("single_connection_client") is not False:
                data["single_connection_client"] = config["single_connection_client"]
            else:
                data["single_connection_client"] = False
            if all_keys.__contains__("health_check_interval") is not False:
                data["health_check_interval"] = config["health_check_interval"]
            if all_keys.__contains__("client_name") is not False:
                data["client_name"] = config["client_name"]
            else:
                data["client_name"] = None
            if all_keys.__contains__("username") is not False:
                data["username"] = config["username"]
            else:
                data["username"] = None
            if all_keys.__contains__("retry") is not False:
                data["retry"] = config["retry"]
            else:
                data["retry"] = None
            if all_keys.__contains__("redis_connect_func") is not False:
                data["redis_connect_func"] = config["redis_connect_func"]
            else:
                data["redis_connect_func"] = None

            f.close()
            return data
        except Exception as err:
            return err

    @staticmethod
    def redispool(self, config: dict):
        try:
            f = open('defaultconfig/redis_pool_config.json')
            data = json.load(f)
            all_keys = config.keys()
            if all_keys.__contains__("host") is not False:
                data["host"] = config["host"]
            if all_keys.__contains__("port") is not False:
                data["port"] = config["port"]
            if all_keys.__contains__("db") is not False:
                data["db"] = config["db"]
            else:
                data["db"] = 0
            if all_keys.__contains__("password") is not False:
                data["password"] = config["password"]
            else:
                data["password"] = None
            if all_keys.__contains__("socket_timeout") is not False:
                data["socket_timeout"] = config["socket_timeout"]
            else:
                data["socket_timeout"] = None

            if all_keys.__contains__("socket_connect_timeout") is not False:
                data["socket_connect_timeout"] = config["socket_connect_timeout"]
            else:
                data["socket_connect_timeout"] = None
            if all_keys.__contains__("socket_keepalive") is not False:
                data["socket_keepalive"] = config["socket_keepalive"]
            else:
                data["socket_keepalive"] = False
            if all_keys.__contains__("socket_keepalive_options") is not False:
                data["socket_keepalive_options"] = config["socket_keepalive_options"]
            else:
                data["socket_keepalive_options"] = None
            if all_keys.__contains__("socket_type") is not False:
                data["socket_type"] = config["socket_type"]
            if all_keys.__contains__("retry_on_timeout") is not False:
                data["retry_on_timeout"] = config["retry_on_timeout"]
            else:
                data["retry_on_timeout"] = False
            if all_keys.__contains__("retry_on_error") is not False:
                data["retry_on_error"] = config["retry_on_error"]
            if all_keys.__contains__("encoding") is not False:
                data["encoding"] = config["encoding"]
            if all_keys.__contains__("encoding_errors") is not False:
                data["encoding_errors"] = config["encoding_errors"]
            if all_keys.__contains__("decode_responses") is not False:
                data["decode_responses"] = config["decode_responses"]
            else:
                data["decode_responses"] = False
            if all_keys.__contains__("socket_read_size") is not False:
                data["socket_read_size"] = config["socket_read_size"]
            if all_keys.__contains__("health_check_interval") is not False:
                data["health_check_interval"] = config["health_check_interval"]
            if all_keys.__contains__("client_name") is not False:
                data["client_name"] = config["client_name"]
            else:
                data["client_name"] = None
            if all_keys.__contains__("username") is not False:
                data["username"] = config["username"]
            else:
                data["username"] = None
            if all_keys.__contains__("retry") is not False:
                data["retry"] = config["retry"]
            else:
                data["retry"] = None
            if all_keys.__contains__("redis_connect_func") is not False:
                data["redis_connect_func"] = config["redis_connect_func"]
            else:
                data["redis_connect_func"] = None
            f.close()
            return data
        except Exception as err:
            return err

    @staticmethod
    def postgres(self, config: dict):
        try:
            f = open('defaultconfig/postgres_config.json')
            data = json.load(f)
            if config["host"] is not None:
                data["host"] = config["host"]
            if config["user"] is not None:
                data["user"] = config["user"]
            if config["password"] is not None:
                data["password"] = config["password"]
            if config["dbname"] is not None:
                data["dbname"] = config["dbname"]
            if config["sslmode"] is not None:
                data["sslmode"] = config["sslmode"]
            else:
                data["sslmode"] = True
            f.close()
            return data
        except Exception as err:
            return err

    @staticmethod
    def clickhouse(self, config: dict):
        try:
            f = open('defaultconfig/clickhouse_config.json')
            data = json.load(f)
            if config["host"] is not None:
                data["host"] = config["host"]
            if config["user"] is not None:
                data["user"] = config["user"]
            if config["password"] is not None:
                data["password"] = config["password"]
            if config["database"] is not None:
                data["database"] = config["database"]
            if config["secure"] is not None:
                data["secure"] = config["secure"]
            else:
                data["secure"] = True
            if config["verify"] is not None:
                data["verify"] = config["verify"]
            else:
                data["verify"] = False
            if config["compression"] is not None:
                data["compression"] = config["compression"]
            else:
                data["compression"] = True
            f.close()
            return data
        except Exception as err:
            return err
