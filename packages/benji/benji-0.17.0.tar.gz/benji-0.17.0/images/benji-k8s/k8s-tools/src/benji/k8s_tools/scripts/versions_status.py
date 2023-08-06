#!/usr/bin/env python3
import sys

import benji.helpers.prometheus as prometheus
import benji.helpers.settings as settings
from benji.helpers.utils import setup_logging, subprocess_run

setup_logging()


def main():
    incomplete_versions = subprocess_run([
        'benji',
        '--machine-output',
        '--log-level',
        settings.benji_log_level,
        'ls',
        'status == "incomplete" and date < "1 day ago"',
    ],
                                         decode_json=True)

    invalid_versions = subprocess_run([
        'benji',
        '--machine-output',
        '--log-level',
        settings.benji_log_level,
        'ls',
        'status == "invalid"',
    ],
                                      decode_json=True)

    prometheus.older_incomplete_versions.set(len(incomplete_versions['versions']))
    prometheus.invalid_versions.set(len(invalid_versions['versions']))
    prometheus.push(prometheus.version_status_registry, grouping_key={})
    sys.exit(0)
