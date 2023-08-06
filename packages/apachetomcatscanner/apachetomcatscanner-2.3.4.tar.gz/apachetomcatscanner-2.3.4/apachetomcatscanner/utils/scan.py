#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : scan.py
# Author             : Podalirius (@podalirius_)
# Date created       : 29 Jul 2022

import base64
import re
import requests


def is_target_a_windows_machine() -> bool:
    # if port 135 and 445 open
    pass


def is_target_a_windows_domain_controller() -> bool:
    # if port 135 and 445 and 88 and ldap/ldaps open
    pass


def is_http_accessible(target, port, config, scheme="http"):
    url = "%s://%s:%d/" % (scheme, target, port)
    try:
        r = requests.get(
            url,
            timeout=config.request_timeout,
            proxies=config.request_proxies,
            verify=(not (config.request_no_check_certificate))
        )
        return True
    except Exception as e:
        config.debug("Error in is_http_accessible('%s', %d, '%s'): %s " % (target, port, scheme, e))
        return False


def is_tomcat_manager_accessible(target, port, config, scheme="http"):
    path = "/manager/html"
    url = "%s://%s:%d%s" % (scheme, target, port, path)
    try:
        r = requests.get(
            url,
            timeout=config.request_timeout,
            proxies=config.request_proxies,
            verify=(not (config.request_no_check_certificate))
        )
        if r.status_code in [401]:
            return True
        else:
            return False
    except Exception as e:
        config.debug("Error in is_tomcat_manager_accessible('%s', %d, '%s'): %s " % (target, port, scheme, e))
        return False


def get_version_from_malformed_http_request(target, port, config, scheme="http"):
    url = "%s://%s:%d/{}" % (scheme, target, port)
    try:
        r = requests.get(
            url,
            timeout=config.request_timeout,
            proxies=config.request_proxies,
            verify=(not (config.request_no_check_certificate))
        )
    except Exception as e:
        config.debug("Error in get_version_from_malformed_http_request('%s', %d, '%s'): %s " % (target, port, scheme, e))
        return None
    if r.status_code in [400, 404, 500]:
        # Bug triggered
        matched = re.search(b"(<h3>)Apache Tomcat(/)?([^<]+)(</h3>)", r.content)
        if matched is not None:
            _, _, version, _ = matched.groups()
            version = version.decode('utf-8')
            return version


def try_default_credentials(target, port, config, scheme="http"):
    found_credentials = []
    url = "%s://%s:%d/manager/html" % (scheme, target, port)
    try:
        for credentials in config.credentials:
            auth_string = bytes(credentials["username"] + ':' + credentials["password"], 'utf-8')
            r = requests.post(
                url,
                headers={
                    "Authorization": "Basic " + base64.b64encode(auth_string).decode('utf-8')
                },
                timeout=config.request_timeout,
                proxies=config.request_proxies,
                verify=(not (config.request_no_check_certificate))
            )
            if r.status_code in [200, 403]:
                found_credentials.append((r.status_code, credentials))
        return found_credentials
    except Exception as e:
        config.debug("Error in get_version_from_malformed_http_request('%s', %d, '%s'): %s " % (target, port, scheme, e))
        return found_credentials


def scan_worker(target, port, reporter, vulns_db, config):
    config.debug("scan_worker('%s', %d, ...)" % (target, port))
    result = {"target": target}
    for scheme in config.get_request_available_schemes():
        if is_http_accessible(target, port, config, scheme):
            result["version"] = get_version_from_malformed_http_request(target, port, config, scheme)
            if result["version"] is not None:
                config.debug("Found version %s" % result["version"])

                result["manager_accessible"] = is_tomcat_manager_accessible(target, port, config, scheme)

                credentials = []
                if result["manager_accessible"]:
                    config.debug("Manager is accessible")
                    # Test for default credentials
                    credentials = try_default_credentials(target, port, config, scheme)

                str_found_creds = []
                if len(credentials) != 0:
                    for statuscode, creds in credentials:
                        str_found_creds.append("(username:\x1b[1;92m%s\x1b[0m password:\x1b[1;92m%s\x1b[0m)" % (creds["username"], creds["password"]))

                # List of cves
                cve_str = ""
                if config.list_cves_mode == True:
                    cve_list = vulns_db.get_vulnerabilities_of_version_sorted_by_criticity(result["version"], colors=True, reverse=True)
                    if len(cve_list) != 0:
                        cve_str = "CVEs: %s" % ', '.join(cve_list)

                print("[>] [Apache Tomcat/\x1b[1;95m%s\x1b[0m] on \x1b[1;93m%s\x1b[0m:\x1b[1;93m%d\x1b[0m (manager:%s) %s %s\x1b[0m " % (
                        result["version"],
                        target,
                        port,
                        ("\x1b[1;92maccessible\x1b[0m" if result["manager_accessible"] else "\x1b[1;91mnot accessible\x1b[0m"),
                        ' '.join(str_found_creds),
                        cve_str
                    )
                )

                cve_list = vulns_db.get_vulnerabilities_of_version_sorted_by_criticity(result["version"], colors=False, reverse=True)
                credentials_str = "username:%s\npassword:%s" % (credentials[0][1]["username"], credentials[0][1]["password"])
                cve_str = ', '.join([cve["cve"]["id"] for cve in cve_list])

                reporter.report_result(
                    target,
                    port,
                    result["version"],
                    result["manager_accessible"],
                    credentials_str,
                    cve_str
                )


