from typing import Literal, Optional, Union

# Duration is used to describe time periods in
# natural langauge. To specify using natural
# language, write the count of the unit you would
# like, followed by the representation of the unit.
#
# Chalk support the following units:
# | Signifier | Meaning  |
# | --------- | -------- |
# | w         | Weeks    |
# | d         | Days     |
# | h         | Hours    |
# | m         | Minutes  |
# | s         | Seconds  |
#
# Examples
# | Signifier   | Meaning                           |
# | ----------- | --------------------------------- |
# | "10h"       | 10 hours                          |
# | "1w 2m"     | 1 week and 2 minutes              |
# | "1h 10m 2s" | 1 hour, 10 minutes, and 2 seconds |
#
# Read more at https://docs.chalk.ai/docs/duration
Duration = str

# A schedule defined using the unix-cron
# string format (* * * * *).
# Values are given in the order below:
#
# | Field        | Values |
# | ------------ | ------ |
# | Minute       | 0-59   |
# | Hour         | 0-23   |
# | Day of Month | 1-31   |
# | Month        | 1-12   |
# | Day of Week  | 0-6    |
CronTab = str
ScheduleOptions = Optional[Union[CronTab, Duration, Literal[True]]]
