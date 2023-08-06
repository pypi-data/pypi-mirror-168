import subprocess
from collections import OrderedDict
from datetime import datetime

from gitlogs.utils.bcolors import bcolors
from gitlogs.defaults.handle_defaults import current_symbol

weekdays = {
    1: "Mon",
    2:"Tue",
    3: "Wed",
    4: "Thu",
    5: "Fri",
    6: "Sat",
    7: "Sun"
}

months = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec"
}

def is_not_git() -> bool:
    """Check if git is initialized in the repository"""
    args = "git rev-parse --git-dir".split(" ")

    output = subprocess.run(
        args,
        universal_newlines=True,
        shell=False,
        stderr=subprocess.DEVNULL, # hide standard error
        stdout=subprocess.DEVNULL, # hide output 
    )
    if output.returncode == 0:
        return False
    return True


def get_logs(before: str, after: str, reverse: bool) -> list:
    """Return results of git log [args]"""

    # < day, date, author >
    args = ["git", "log", "--pretty=format:%ai,%aN"]

    commit_logs = []
    try:
        if after != "":
            args.append("--after=" + after)
        if before:
            args.append("--before=" + before)

        logs = subprocess.check_output(
            args, shell=False, universal_newlines=True
        ).split("\n")

        # Process each line
        for line in logs:
            time_stamp, author = line.split(",")
            commit_logs.append({"time_stamp": time_stamp, "author": author})

        if reverse:
            return commit_logs[::-1]

        return commit_logs

    except Exception:
        return []


def filter_logs(logs: list, author: str, frequency="month") -> dict:
    """Filter the logs based on author and frequency(day, week, month, year)"""

    commit_count_by_freq = OrderedDict()

    for commit_info in logs:
        commit_date = commit_info["time_stamp"].split(" ")[0]

        is_weekend = False
        if frequency == "week":
            # %V gives number of weeks so far in a given year
            commit_date = datetime.strptime(commit_date, "%Y-%m-%d").strftime("%Y/%V")
        elif frequency == "month":
            commit_date = commit_info["time_stamp"][:7]  # YYYY-MM
        elif frequency == "year":
            commit_date = commit_info["time_stamp"][:4]  # YYYY
        else:
            # return the day of the week
            is_weekend = (
                True
                if (datetime.strptime(commit_date, "%Y-%m-%d").isoweekday()>5)
                else False
            )
            # Monday=1, Tuesday=2, Wednesday=3 and so on..

        if author != "":
            if author not in commit_info["author"]:
                continue

        if commit_date not in commit_count_by_freq:
            # Add entry for that commit date
            commit_count_by_freq[commit_date] = {
                "time_stamp": commit_info["time_stamp"],
                "commits": 0,
                "is_weekend": is_weekend,
            }

        # Entry already exists for that commit date so increment
        commit_count_by_freq[commit_date]["commits"] += 1
    return commit_count_by_freq


def normalize(value: int, xmin: int, xmax: int) -> float:
    """Return min-max normalized value"""
    return float(value - xmin) / float(xmax - xmin)


def get_relative_count(filtered_commits: OrderedDict) -> OrderedDict:
    """Compute normalized score/count based on given filter"""

    values = [item["commits"] for item in filtered_commits.values()]
    values.append(0)  # To handle the case where only 1 value is present

    xmin = min(values)
    xmax = max(values)

    normalized_info = OrderedDict()

    for commit_date in filtered_commits.keys():
        normalized_info[commit_date] = filtered_commits[commit_date].copy()
        # add normalized value
        normalized_info[commit_date]["score"] = normalize(
            filtered_commits[commit_date]["commits"], xmin, xmax
        )

    return normalized_info


def display(logs: OrderedDict, frequency: str) -> None:
    """Display commit information to stdout"""

    for commit_date in logs:
        
        count = str(logs[commit_date]["commits"])  # how many commits based on frequency
        output_date = commit_date

        if(frequency=="month"):
            y,m = commit_date.split("-")
            y = int(y)
            m = int(m)
            output_date = f"{y} {months[m]}"
        elif(frequency=="day"):
            y,m,d = commit_date.split("-")
            y = int(y)
            m = int(m)
            d = int(d)
            
            output_date = f"{months[m]},{y} ({weekdays[datetime(y,m,d).isoweekday()]})"
            if (d<10):
                output_date = f" {d} {output_date}"
            else:
                output_date = f"{d} {output_date}"

        # is weekend
        if(logs[commit_date]["is_weekend"]): 
            print(f"{bcolors.colored(output_date, bcolors.BIPurple)}  {bcolors.okblue(count)}", end="\t")
        # not weekend
        else: 
            print(f"{bcolors.header(output_date)}  {bcolors.okblue(count)}", end="\t")


        # Scale up the scores by 50x
        print(bcolors.ok(current_symbol()) * int(logs[commit_date]["score"] * 50))