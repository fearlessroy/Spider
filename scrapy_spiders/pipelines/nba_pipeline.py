"""
This module contains pipelines for NBA schedule spider.
"""

from datetime import datetime, timedelta


class NBASchedulePipeline(object):
    def __init__(self):
        self.item_map = {}

    def process_item(self, item, spider):
        source_team_name = item["source_team_name"]
        if source_team_name in self.item_map:
            self.item_map[source_team_name].append(item)
        else:
            self.item_map[source_team_name] = [item]
        return item

    def close_spider(self, spider):
        for source_team_name, items in self.item_map.items():
            out_filename = "./calendars/{0}.ics".format(source_team_name)
            with open(out_filename, "w") as out_file:
                out_file.write("BEGIN:VCALENDAR\n")
                for item in items:
                    start_time = datetime.strptime(item["game_time"], "%Y-%m-%d %H:%M:%S")
                    end_time = start_time + timedelta(hours=2, minutes=30)
                    event = ["BEGIN:VEVENT",
                             "DTSTART:{0}T{1}".format(start_time.strftime("%Y%m%d"), start_time.strftime("%H%M%S")),
                             "DTEND:{0}T{1}".format(end_time.strftime("%Y%m%d"), end_time.strftime("%H%M%S")),
                             "SUMMARY:{0} vs {1}".format(item["home_team_name"], item["away_team_name"]),
                             "END:VEVENT"]
                    out_file.write("\n".join(event))
                    out_file.write("\n")
                out_file.write("END:VCALENDAR")
