import time

from selenium.common.exceptions import TimeoutException

import processes
from logmgmt import logger
from exceptions import RenewalRequestNeededException
from input.input_management import InputManager
from model.ssodetection.sso_detection_strategy import SSODetectionStrategy
from processes.ssolandscapeanalysis.locators.social_login_information import SocialLoginInformation
from processes.ssolandscapeanalysis.locators.social_login_locator import SocialLoginLocator


def get_max_steps_for_detection(run_google, run_facebook, run_apple):
    steps = 0
    if run_google:
        steps += 1
    if run_facebook:
        steps += 1
    if run_apple:
        steps += 1
    return steps


class SSODetectionService:

    def __init__(self, known_sso_providers):
        self.known_sso_providers = known_sso_providers
        self.locators = {}
        for prov in known_sso_providers:
            self.locators[prov[1].lower()] = self.load_social_login_locater(prov[1].title())

    def automatic_sso_detection(self, chromedriver, latest_login_info, providers_to_detect, results, known_sso_provider,
                                progress_callback=None, special_check: callable = None, skip_result_check=False) -> [
        tuple]:
        ids = []
        # Todo: Maybe calculate which providers are already detected
        max_steps = len(providers_to_detect)
        current_step = 0
        for provider in providers_to_detect:
            if not skip_result_check and processes.ProcessHelper.contain_results_provider(results, provider, known_sso_provider):
                logger.info(provider + ' already found. Skipping!')
                continue
            current_step += 1
            if progress_callback is not None:
                progress_callback(current_step, max_steps,
                                  "Identifying " + provider.title() + " SSO Support for " + latest_login_info.loginPath)
            logger.info("--- " + provider.title() + " ---")
            start_time = time.time()
            try:
                locate_result = self.locators[provider.lower()].locate_login(chromedriver, latest_login_info,
                                                                             special_check)
                logger.info("--- Finished " + provider + " in " + str(round(time.time() - start_time, 2)) + "s ---")
            except TimeoutException:
                locate_result = False,
                logger.info("--- Analysis for " + provider + " failed after " + str(
                    round(time.time() - start_time, 2)) + "s ---")
            if locate_result[0]:
                ids.append((self.find_id_for_provider(provider), locate_result[1], locate_result[2],
                            latest_login_info.loginPath, locate_result[3], locate_result[4]))
        if len(ids) == 0:
            ids.append((self.find_id_for_provider('none'), None, None, None, SSODetectionStrategy.ELEMENT_SEARCH, None))
        return ids

    def manual_sso_detection(self) -> [tuple]:
        supported_sso = []
        inp = ""
        while inp != "Finish" and inp != "None" and inp != "Skip" and inp != "Send Renewal Request":
            valid = self.create_valid_inputs_from_already_gathered_sso(supported_sso)
            if len(supported_sso) == 0:
                valid.append("Skip")
                valid.append("Send Renewal Request")
            if len(supported_sso) > 0:
                valid.append("Finish")
                valid.append("Reset")
            inp = InputManager.get_input_from_gui_with_specific_answer_values("Input", valid, False)
            if inp == "Reset":
                supported_sso.clear()
            if inp == "Send Renewal Request":
                raise RenewalRequestNeededException()
            elif inp != "Finish":
                supported_sso.append(inp)
            if inp == "Finish" or inp == "None" or inp == "Skip":
                savable_sso_providers = []
                for supported_sso_provider in supported_sso:
                    for backend_sso_provider in self.known_sso_providers:
                        if backend_sso_provider[1].startswith(supported_sso_provider):
                            savable_sso_providers.append(backend_sso_provider)
                text = ""
                ids = []
                for save_sso_provider in savable_sso_providers:
                    text += " " + save_sso_provider[1]
                    ids.append((save_sso_provider[0], None, None, None, SSODetectionStrategy.MANUAL))
                if len(ids) > 1 or ids[0][0] != 9999:
                    if InputManager.get_input_from_gui_with_specific_answer_values(
                            "Saving:" + text + ". Correct?", ["y", "n"], False) == "n":
                        logger.info("Restarting gathering process...")
                        supported_sso.clear()
                        inp = ""
                    else:
                        return ids
                else:
                    return ids

    def create_valid_inputs_from_already_gathered_sso(self, supported_sso):
        valid_inputs_raw = InputManager.create_supported_sso_user_inputs(self.known_sso_providers)
        return_list = []
        for inp in valid_inputs_raw:
            # inp_to_check = inp[0][0:1].upper() + inp[0][1:len(inp)]
            inp_to_check = inp[1]
            if inp_to_check not in supported_sso:
                if inp[1].lower() != "none" or len(supported_sso) == 0:
                    return_list.append(inp[1])  # Change this to 0 and change commented line above for short form
        return return_list

    def find_id_for_provider(self, provider_name):
        for sso in self.known_sso_providers:
            if sso[1].lower() == provider_name.lower():
                return sso[0]
        raise Exception("Unknown provider")

    @staticmethod
    def load_social_login_locater(social_login_name):
        if social_login_name in SocialLoginInformation:
            return SocialLoginLocator(SocialLoginInformation[social_login_name]["name"],
                                      SocialLoginInformation[social_login_name]["exclude_url_starts_with"],
                                      SocialLoginInformation[social_login_name]["valid_login_urls"],
                                      SocialLoginInformation[social_login_name]["must_have_texts_in_valid_login_urls"],
                                      SocialLoginInformation[social_login_name]["extra_texts"])
        return None
