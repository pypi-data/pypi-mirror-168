import binascii
import copy
import json
from typing import Optional

from loguru import logger

from ssrspeed.utils import b64plus


class ParserShadowsocksBasic:
    def __init__(self, base_config: dict):
        self.__config_list: list = []
        self.__base_config: dict = base_config

    def __get_shadowsocks_base_config(self) -> dict:
        return copy.deepcopy(self.__base_config)

    def __parse_link(self, link: str) -> Optional[dict]:
        _config = self.__get_shadowsocks_base_config()

        if link[:5] != "ss://":
            logger.error(f"Unsupported link : {link}")
            return None

        try:
            invalid_link = "Not shadowsocks basic link."
            decoded = b64plus.decode(link[5:]).decode("utf-8")
            at_pos = decoded.rfind("@")
            if at_pos == -1:
                raise ValueError(invalid_link)
            mp = decoded[:at_pos]
            ap = decoded[at_pos + 1 :]
            mp_pos = mp.find(":")
            ap_pos = ap.find(":")
            if mp_pos == -1 or ap_pos == -1:
                raise ValueError(invalid_link)
            encryption = mp[:mp_pos]
            password = mp[mp_pos + 1 :]
            server = ap[:ap_pos]
            port = int(ap[ap_pos + 1 :])
            _config["server"] = server
            _config["server_port"] = port
            _config["method"] = encryption
            _config["password"] = password
            _config["remarks"] = _config["server"]
        except binascii.Error as error:
            raise ValueError(invalid_link) from error
        except Exception:
            logger.exception(f"Exception link {link}")
            return None
        return _config

    def parse_single_link(self, link: str) -> Optional[dict]:
        return self.__parse_link(link)

    def parse_subs_config(self, links: list) -> list:
        for link in links:
            link = link.strip()
            if cfg := self.__parse_link(link):
                self.__config_list.append(cfg)
        logger.info(f"Read {len(self.__config_list)} config(s).")
        return self.__config_list

    @staticmethod
    def __get_ssd_group(ssd_subs: list, sub_url: str) -> str:
        if not ssd_subs or not sub_url:
            return "N/A"
        return next(
            (
                item.get("airport", "N/A")
                for item in ssd_subs
                if item.get("url", "") == sub_url
            ),
            "N/A",
        )

    def parse_gui_data(self, data: dict) -> list:
        shadowsocksd_conf = False
        ssd_subs = []
        if "subscriptions" in data:
            shadowsocksd_conf = True
            ssd_subs = data["subscriptions"]
        configs = data["configs"]
        for item in configs:
            _dict = self.__get_shadowsocks_base_config()
            _dict["server"] = item["server"]
            _dict["server_port"] = int(item["server_port"])
            _dict["password"] = item["password"]
            _dict["method"] = item["method"]
            _dict["plugin"] = item.get("plugin", "")
            _dict["plugin_opts"] = item.get("plugin_opts", "")
            _dict["plugin_args"] = item.get("plugin_args", "")
            _dict["remarks"] = item.get("remarks", item["server"])
            if not _dict["remarks"]:
                _dict["remarks"] = _dict["server"]
            _dict["group"] = (
                self.__get_ssd_group(ssd_subs, item.get("subscription_url", ""))
                if shadowsocksd_conf
                else item.get("group", "N/A")
            )

            _dict["fast_open"] = False
            self.__config_list.append(_dict)
        return self.__config_list

    def parse_gui_config(self, filename: str) -> list:
        with open(filename, "r", encoding="utf-8") as f:
            try:
                full_conf = json.load(f)
                self.parse_gui_data(full_conf)
            except json.decoder.JSONDecodeError:
                return []
            except Exception:
                logger.exception("Not Shadowsocks configuration file.")
                return []

        logger.info(f"Read {len(self.__config_list)} node(s).")
        return self.__config_list
