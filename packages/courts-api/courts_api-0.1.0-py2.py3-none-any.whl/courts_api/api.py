from pathlib import Path
import pandas as pd
import time
import json
from seleniumrequests import Firefox
from selenium.webdriver import FirefoxOptions
from juriscraper.pacer.docket_report import DocketReport
from courts_api.scales.code.support import fhandle_tools as ftools
from courts_api.scales.code.support import data_tools as dtools
from courts_api.scales.code.downloader import forms
from courts_api.scales.code.downloader.scrapers import DocketScraper, extract_court_caseno, PAUSE, MAX_LONGTIME_ATTEMPTS, PACER_ERROR_WRONG_CASE
import courts_api


PACER_TO_CL_IDS = {
	'azb': 'arb',
	'cofc': 'uscfc',
	'neb': 'nebraskab',
	'nysb-mega': 'nysb',
}


CL_ROLES = {
	1: "Attorney to be noticed",
	2: "Lead attorney",
	3: "Attorney in sealed group",
	4: "Pro hac vice",
	5: "Self-terminated",
	6: "Terminated",
	7: "Suspended",
	8: "Inactive",
	9: "Disbarred",
	10: "Unknown",
}


class SCALESDocketScraper(DocketScraper):
    def __init__(self, headless=True):
        courts_api.config['user']
        courts_api.config['pass']
        core_args = dict(
            court_dir=None, 
            court=None, 
            auth_path=courts_api.config.path, 
            headless=headless, 
            verbose=True,
        )
        super(DocketScraper, self).__init__(
            **core_args
        )

    def launch_browser(self):
        options = FirefoxOptions()
        options.set_preference("plugin.disable_full_page_plugin_for_types", "application/pdf")
        options.set_preference("pdfjs.disabled", True)
        options.headless = self.headless
        self.browser = Firefox(options=options)
        return self.login()
    
    def pull_case(self, court, docket_number, latest_date=None, exclude_parties=False, def_no=None):
        self.court = court
        if not self.browser:
            login_success = self.launch_browser()
            if not login_success:
                self.close_browser()
                raise ValueError('Cannot log in to PACER')

        ucid = dtools.ucid(court, docket_number)

        docket_url = ftools.get_pacer_url(court, 'docket')
        self.browser.get(docket_url)

        case_no_input = docket_number + f"-{def_no}" if def_no is not None else docket_number
        fill_values = {
            'case_no': case_no_input,
            # Sort by oldest date first by default, gets around issue in IASD
            'sort_by': 'oldest date first',
            # Explicitly grab parties and terminated parties
            'include_parties': True,
            'include_terminated': True,
        }
        
        if latest_date is not None:
            next_day = (pd.to_datetime(latest_date) + pd.Timedelta(days=1))
            fill_values['date_from'] = next_day.strftime(ftools.FMT_PACERDATE)
            print(f"Getting updated docket for <case:{docket_number}> from <date:{fill_values['date_from']}>")

        if exclude_parties:
            fill_values['include_parties'] = False
            fill_values['include_terminated'] = False
        
        time.sleep(PAUSE['mini'])
        docket_report_form = forms.FormFiller(self.browser, 'docket', fill_values)
        docket_report_form.fill()

        # Call the possible case no api again to get caseno data
        pacer_id = self.get_caseno_info_id(docket_number, def_no)

        # Submit the form
        docket_report_form.submit()
        time.sleep(PAUSE['mini'])

        # Checks before form submission stage complete
        if not self.at_docket_report():

            #Check if at "may take a long time page"
            if self.at_longtime():

                initially_requested = self.browser.find_elements_by_css_selector('input[name="date_from"]')[-1]
                initially_requested.click()
                time.sleep(PAUSE['micro'])

                print(f"{self} LONGTIME: case {ucid} at the 'long time' page, submitting form and pausing to let page load...")
                self.browser.execute_script('ProcessForm()')
                time.sleep(PAUSE['moment'])

                # For very slow loading pages, loop and check if page is fully loaded
                longtime_attempts = 0
                transaction_table = None
                while longtime_attempts < MAX_LONGTIME_ATTEMPTS:
                    print(f'LONGTIME loop {longtime_attempts=}')
                    transaction_table = self.get_transaction_table()
                    longtime_attempts += 1

                    if transaction_table:
                        break
                    else:
                        time.sleep(PAUSE['moment'])

                print(f"Out of LONGTIME loop, {longtime_attempts=}")
                if not transaction_table:
                    print('ERROR: LONGTIME exceeded maximum attempts and page not fully loaded')
                    return
            else:
                self.browser.execute_script('ProcessForm()')
                time.sleep(PAUSE['moment'])
            
        # Now assume form submitted correctly, check various scenarious
        if self.at_invalid_case():
            print(f'Invalid case: {docket_number}')

        elif self.at_sealed_case():
            print(f"Sealed case: {docket_number}")
            text = self.browser.find_element_by_css_selector('#cmecfMainContent').text[:200]
            print(f'Explanation from PACER: {text}')

        elif self.at_docket_report():
            # Check for correct caseno and court
            hstring_court, hstring_caseno = extract_court_caseno(self.browser.page_source)
            hstring_caseno = ftools.clean_case_id(hstring_caseno)

            # Training site
            if self.court=='psc':
                hstring_court='psc'

            if not (hstring_court==court and hstring_caseno==docket_number):
                print(f"PACER_ERROR_WRONG_CASE {ucid} {hstring_court=} {hstring_caseno=}")
                return PACER_ERROR_WRONG_CASE

            no_docketlines = self.no_docketlines()
            if no_docketlines:
                print(f'No new docket lines for case: {docket_number}')

            time.sleep(PAUSE['micro'])
            download_url = self.browser.current_url

            html_data = self.browser.page_source + self.stamp(download_url, pacer_id=pacer_id)

            return {
                'ucid': ucid,
                'html': html_data,
            }

        else:
            print(f'ERROR: <case: {ucid}> not found, reason unknown')


class JuriscraperDocketParser(DocketReport):
    def __init__(self, court):
        super().__init__(court, None)
    
    def parse(self, html):
        self._clear_caches()
        self._parse_text(html)
        return self.data


class CourtsAPI():
    def __init__(self, headless=True, allow_spend_money=False, suppress_spending_warnings=False):
        self.allow_spend_money = allow_spend_money
        self.suppress_spending_warnings = suppress_spending_warnings
        self.docket_scraper = SCALESDocketScraper(headless=headless)
    
    def get_case_from_recap(self):
        pass 

    def buy_case_for_recap(self):
        pass 

    def buy_and_download_case(self, court, docket_number, output_dir='.', latest_date=None, exclude_parties=False, def_no=None, skip_download=False):
        ucid = dtools.ucid(court, docket_number)
        fname = ucid.replace(':','-')
        html_path = Path(output_dir) / f'{fname}.html'
        json_path = Path(output_dir) / f'{fname}.json'
        if html_path.exists():
            print(f'File {html_path} already exists, not downloading again')
            case_html = html_path.read_text()
        else:
            case_html = self.docket_scraper.pull_case(court, docket_number, latest_date, exclude_parties, def_no)['html']
        
        parser = JuriscraperDocketParser(court)
        case_json = parser.parse(case_html)

        if not skip_download:
            with open(html_path, 'w') as f:
                f.write(case_html)
            with open(json_path, 'w') as f:
                json.dump(case_json, f, default=str)
        return case_html, case_json
    

def load(*args, **kwargs):
    return CourtsAPI(*args, **kwargs)
