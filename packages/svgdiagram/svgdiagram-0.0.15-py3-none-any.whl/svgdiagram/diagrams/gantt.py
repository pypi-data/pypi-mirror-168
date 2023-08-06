from svgdiagram.elements.svg import Svg
from svgdiagram.elements.group import Group
from svgdiagram.elements.text import Text
from svgdiagram.elements.path import Path
from svgdiagram.elements.rect import Rect
from datetime import datetime, timedelta, date
from svgdiagram.derived_elements.milestone import Milestone
from svgdiagram.derived_elements.task import Task

import re


DEFAULT_STYLING = {
    "CALENDAR": {
        "STYLE": "DAY",  # DAY, WEEK, MONTH, AUTO
        "DAY_WIDTH": 50.0,
        "DAY_FONT": {
            "SIZE": 16.0
        },
        "DAY_COLUMN_COLOR": "#bbbbbb",
        "DAY_COLUMN_COLOR_ODD": "#dddddd",
    }
}
DEFAULT_OPTIONS = {
    "DATE_DEFAULT_TIME": "T12:00:00"
}


def parse_date_string(date_string):
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_string):
        return date.fromisoformat(date_string)
    else:
        return datetime.fromisoformat(date_string)


class Gantt(Svg):
    def __init__(self, content, style=None, options=None):
        super().__init__()

        self.content = content
        self.style = style if style else DEFAULT_STYLING
        self.options = options if options else DEFAULT_OPTIONS

        self.group_calendar_tiles = Group()
        self.append_child(self.group_calendar_tiles)
        self.group_calendar_text = Group()
        self.append_child(self.group_calendar_text)

        self.group_swimlanes = Group()
        self.append_child(self.group_swimlanes)

    @property
    def start_date(self):
        return date.fromisoformat(self.content["start_date"])

    @property
    def end_date(self):
        return date.fromisoformat(self.content["end_date"])

    def date_to_column_index(self, date_value):
        """Gives the correct column index based on a date"""

        if isinstance(date_value, datetime):
            date_value = date_value.date()

        assert isinstance(date_value, date), \
            f'"{date_value}" is not a datetime.date!'

        return (date_value - self.start_date).days

    def date_to_column_fraction(self, datetime_value):
        """Gives the correct column index and the fraction within it based on a datetime."""

        if type(datetime_value) == date:
            datetimestr = datetime_value.isoformat() \
                + self.options["DATE_DEFAULT_TIME"]
            datetime_value = datetime.fromisoformat(datetimestr)

        assert isinstance(datetime_value, datetime), \
            f'"{datetime_value}" is not a datetime.datetime!'

        index = self.date_to_column_index(datetime_value)

        seconds_of_day = datetime_value.second \
            + datetime_value.minute * 60 \
            + datetime_value.hour * 3600
        fraction = seconds_of_day / float(24 * 3600)

        return index, fraction

    def _layout(self, x_con_min, x_con_max, y_con_min, y_con_max):
        calendar_x_left, calendar_x_right = self._build_calendar_text()
        swimlane_y_max = self._build_swimlanes(
            calendar_x_left, calendar_x_right)
        self._build_calender_tiles(swimlane_y_max)

    def _build_calendar_text(self):
        assert self.start_date <= self.end_date, \
            f'Enddate "{self.end_date}" is before startdate "{self.start_date}"!'

        DAY_WIDTH = self.style["CALENDAR"]["DAY_WIDTH"]
        DAY_FONT_SIZE = self.style["CALENDAR"]["DAY_FONT"]["SIZE"]
        DAY_COLUMN_COLOR = self.style["CALENDAR"]["DAY_COLUMN_COLOR"]
        DAY_COLUMN_COLOR_ODD = self.style["CALENDAR"]["DAY_COLUMN_COLOR_ODD"]

        c_date = self.start_date
        while c_date <= self.end_date:
            year, week, weekday = c_date.isocalendar()

            index, fraction = self.date_to_column_fraction(c_date)

            day_x = (index + fraction) * DAY_WIDTH
            day_y = 0

            day_color = DAY_COLUMN_COLOR if (
                index % 2) == 0 else DAY_COLUMN_COLOR_ODD

            self.group_calendar_tiles.append_child(Rect.midpoint_round_rect(
                mid_x=day_x,
                mid_y=day_y,
                width=DAY_WIDTH,
                height=DAY_FONT_SIZE,
                radius=0,
                stroke=day_color,
                stroke_width_px=0.1,
                fill=day_color,
            ))
            self.group_calendar_text.append_child(
                Text(day_x, day_y, c_date.strftime(r'%d')))

            if weekday == 1:
                self.group_calendar_text.append_child(
                    Text(index * DAY_WIDTH, -DAY_FONT_SIZE,
                         f"CW {week}", horizontal_alignment="left")
                )

            if c_date.day == 1:
                self.group_calendar_text.append_child(
                    Text(index * DAY_WIDTH, -DAY_FONT_SIZE*2,
                         c_date.strftime('%B').upper(), horizontal_alignment="left")
                )

            # iter
            c_date += timedelta(days=1)

        calendar_x_left = self.date_to_column_index(
            self.start_date) * DAY_WIDTH
        calendar_x_right = (self.date_to_column_index(
            self.end_date) + 1) * DAY_WIDTH
        return calendar_x_left, calendar_x_right

    def _build_swimlanes(self, calendar_x_left, calendar_x_right):
        DAY_WIDTH = self.style["CALENDAR"]["DAY_WIDTH"]

        for index, swimmlane in enumerate(self.content["swimlanes"]):
            swimlane_y = 40+80*index
            self.group_swimlanes.append_child(
                Text(-8, swimlane_y, swimmlane["name"],
                     horizontal_alignment="right")
            )

            self.group_swimlanes.append_child(Path(
                points=[(calendar_x_left, swimlane_y),
                        (calendar_x_right, swimlane_y)]
            ))

            for task in swimmlane.get("tasks", []):
                task_start_date = parse_date_string(task["start_date"])
                task_end_date = parse_date_string(task["end_date"])
                task_name = task["name"]
                task_progess = task["progress"]

                task_start_date_index, task_start_date_fraction = self.date_to_column_fraction(
                    task_start_date)
                task_end_date_index, task_end_date_fraction = self.date_to_column_fraction(
                    task_end_date)
                task_x_start = (task_start_date_index +
                                task_start_date_fraction) * DAY_WIDTH
                task_x_end = (task_end_date_index +
                              task_end_date_fraction) * DAY_WIDTH
                self.group_swimlanes.append_child(Task(
                    x_start=task_x_start,
                    x_end=task_x_end,
                    y=swimlane_y,
                    height=20,
                    radius=5,
                    text=task_name,
                    progess=task_progess,
                ))

            for milestone in swimmlane.get("milestones", []):
                milestone_datetime = parse_date_string(milestone["due"])
                milestone_index, milestone_fraction = self.date_to_column_fraction(
                    milestone_datetime)
                milestone_x = (milestone_index +
                               milestone_fraction) * DAY_WIDTH
                self.group_swimlanes.append_child(
                    Milestone(milestone_x, swimlane_y)
                )
                self.group_swimlanes.append_child(
                    Text(milestone_x, swimlane_y+30, milestone["name"])
                )

        swimlane_y_max = 100+80*index
        return swimlane_y_max

    def _build_calender_tiles(self, swimlane_y_max):
        DAY_WIDTH = self.style["CALENDAR"]["DAY_WIDTH"]
        DAY_FONT_SIZE = self.style["CALENDAR"]["DAY_FONT"]["SIZE"]
        DAY_COLUMN_COLOR = self.style["CALENDAR"]["DAY_COLUMN_COLOR"]
        DAY_COLUMN_COLOR_ODD = self.style["CALENDAR"]["DAY_COLUMN_COLOR_ODD"]

        c_date = self.start_date
        while c_date <= self.end_date:
            year, week, weekday = c_date.isocalendar()

            index, fraction = self.date_to_column_fraction(c_date)

            day_x = index * DAY_WIDTH
            day_y = 0

            day_color = DAY_COLUMN_COLOR if (
                index % 2) == 0 else DAY_COLUMN_COLOR_ODD

            self.group_calendar_tiles.append_child(Rect(
                x=day_x,
                y=day_y - DAY_FONT_SIZE/2.0,
                width=DAY_WIDTH,
                height=swimlane_y_max - (day_y - DAY_FONT_SIZE/2.0),
                rx=0, ry=0,
                stroke=day_color,
                stroke_width_px=0.1,
                fill=day_color,
            ))

            # iter
            c_date += timedelta(days=1)
