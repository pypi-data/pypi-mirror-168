from .base import *
from ..constants.google import *


class Google(Base):
    URL = "https://translate.google.com/"
    DEFAULT_TARGET = "zh-CN"
    SUPPORT_TTS = True

    def __init__(self, debug=False):
        super().__init__(debug)
        self.url_map = {
            ("batchexecute",): Handlers(
                [self._get_simple_result, self._get_dict_result], self._debug_save_raw
            ),
        }

    def validate_lang(self):
        if self.source not in SOURCE_LANG:
            raise Exception(f"{self.source} is not a valid source language.")
        if self.target not in TARGET_LANG:
            raise Exception(f"{self.target} is not a valid target language.")
        self.url = self.URL + f"?sl={self.source}&tl={self.target}&op=translate"

    def _get_simple_result(self, body):
        body = body[6:].splitlines()[1]
        body = json.loads(body)[0][2]
        body = json.loads(body)
        if body == []:
            return False
        try:
            translations = body[1][0][0][5][0][4]
            self.result = [t[0] for t in translations]
            return True
        except IndexError:
            return False

    def _get_dict_result(self, body):
        body = body[6:].splitlines()[1]
        body = json.loads(body)[0][2]
        body = json.loads(body)
        try:
            dict_result = []
            for wtypes, wmeans, _, _ in body[3][5][0]:
                dict_result.append(
                    {"type": wtypes, "means": [wmean[0] for wmean in wmeans]}
                )
            self.dict_result = dict_result
            return True
        except IndexError:
            return False

    def wait_for_response(self, text, urls=None):
        return super().wait_for_response(text, {"batchexecute": self._check_response})

    def _play_sound(self, check_interval=0.1):
        elem = self.driver.find_element(
            By.XPATH,
            f"//div/span/button[@data-idom-class='fzRBVc tmJved mN1ivc SSgGrd']",
        )
        class_attr = "VfPpkd-Bz112c-LgbsSe VfPpkd-Bz112c-LgbsSe-OWXEXe-e5LLRc-SxQuSe fzRBVc tmJved mN1ivc SSgGrd VfPpkd-ksKsZd-mWPk3d VfPpkd-ksKsZd-mWPk3d-OWXEXe-ZNMTqd"
        elem.click()
        while True:
            _attr = elem.get_attribute("class")
            if _attr == class_attr:
                break
            time.sleep(check_interval)
        time.sleep(check_interval)


register("google", Google)
