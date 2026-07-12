# Licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the project root for the full license text.
# Copyright (C) 2026 arvin, arvinrjb13@gmail.com

import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    filename="agent.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

try:
    handler = RotatingFileHandler(
    "agent.log",
    maxBytes=1024 * 1024,
    backupCount=3
    )
except:
    pass


logger = logging.getLogger("agent")
