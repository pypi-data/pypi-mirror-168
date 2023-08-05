"""
The aurori project

Copyright (C) 2022  Marcus Drobisch,

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__authors__ = ["Marcus Drobisch"]
__contact__ = "aurori@fabba.space"
__credits__ = []
__license__ = "AGPLv3"

from aurori.monits.monits import Monit
from aurori.monits.events import MonitorBaseEvent
from aurori.monits.types import MonitType, MonitTimeAggregationType, MonitPropertyType


class UserLoginEvent(MonitorBaseEvent):
    name = "UserLogin"


class UserLogins(Monit):
    event = UserLoginEvent
    monit_type = MonitType.TIMELINE
    monit_time_aggregation = MonitTimeAggregationType.HOURLY
    monit_display_property = MonitPropertyType.TOTAL_COUNT

    def define_views(self):
        self.add_timelinechart_view("total",
                                    "Total Count",
                                    MonitPropertyType.TOTAL_COUNT,
                                    fill_timeline_gaps=False)
        self.add_barchart_view("count",
                               "Count",
                               MonitPropertyType.COUNT,
                               fill_timeline_gaps=True)
