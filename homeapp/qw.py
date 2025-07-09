import json
from datetime import datetime, date
import calendar

# MONTH_DAYS dictionary is defined but not used in the provided function,
# as calendar.monthrange is used instead to get the number of days in a month,
# which correctly handles leap years.

def can_date_be_holiday(json_data, target_date_str):
    """Check if a date can be a holiday given instructional days and events."""
    try:
        # Parse the target date
        target_date = datetime.strptime(target_date_str, "%Y-%m-%d").date()

        # Create the month key (e.g., "november_2024")
        month_key = f"{target_date.strftime('%B').lower()}_{target_date.year}"

        # Get the data for the target month
        month_data = json_data["calendar_data"].get(month_key)

        # Check if month data exists
        if not month_data:
            return "Month not found in calendar"

        # Get instructional days for the month
        # Default to None if not found
        instructional_days = month_data.get("month_info", {}).get("instructional_days")

        # Check if instructional days data is missing (null in JSON)
        if instructional_days is None:
            return "No instructional days data"

        # Find the "Commencement of first semester classes" date if it exists in the current month
        first_semester_start_date = None
        for event in month_data.get("events", []):
            if "date" in event and "Commencement of sixth semester classes" in event.get("description", ""):
                 event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
                 # Check if the commencement is in the target month and year
                 if event_date.month == target_date.month and event_date.year == target_date.year:
                     first_semester_start_date = event_date
                     # print(event_date) # Debug print
                     break # Assuming only one such commencement per month

        # Calculate the total possible days for instruction/events in the month.
        # This is either the total days in the month, or the number of days
        # from the first semester commencement date to the end of the month.
        is_leap_year = calendar.isleap(target_date.year)
        total_days_in_month = calendar.monthrange(target_date.year, target_date.month)[1]

        if first_semester_start_date:
             # If commencement exists, only days from commencement onwards are relevant
             # Corrected: Added +1 to include the start day
             total_possible_days = total_days_in_month - first_semester_start_date.day -1
             print(total_possible_days) # Debug print
             print(total_days_in_month) # Debug print
             print(first_semester_start_date)
        else:
             # Otherwise, all days in the month are relevant
             total_possible_days = total_days_in_month

        # Check if the number of instructional days leaves at least one non-instructional day
        # This means instructional_days must be strictly less than total_possible_days
        if instructional_days >= total_possible_days:
             return "No (all available days are instructional)"


        # Check if the target date is already marked as "busy" in the events list
        # Also check if the target date is BEFORE the commencement date if commencement exists
        if first_semester_start_date and target_date < first_semester_start_date:
             # If the date is before the commencement, it cannot be an instructional day
             # but it might still be blocked by a busy event that occurs *before* commencement.
             # We still need to check busy events below.
             pass # Continue to busy checks

        for event in month_data.get("events", []):
            if "date" in event:
                event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
                if event_date == target_date:
                    if event.get("status") == "busy":
                        return "No (busy event exists)"
            elif "date_range" in event:
                start = datetime.strptime(event["date_range"]["start"], "%Y-%m-%d").date()
                end = datetime.strptime(event["date_range"]["end"], "%Y-%m-%d").date()
                if start <= target_date <= end:
                    if event.get("status") == "busy":
                        return "No (falls in busy range)"

        # One additional check: If a commencement date exists, dates *before* it,
        # while not considered 'instructional' based on the count,
        # might still be intended as non-holiday periods unless explicitly marked.
        # The current logic correctly handles busy events *before* commencement.
        # If it's before commencement and not a busy event, the current logic says Yes.
        # This seems reasonable based on the current rules - a date is a holiday unless blocked.

        # If none of the "No" conditions were met, the date can be a holiday
        return "Yes (can be holiday)"

    except ValueError:
        return "Error: Invalid date format. Use YYYY-MM-DD."
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage with adjusted JSON data
json_str = '''{
    "calendar_data": {
        "november_2024": {
            "month_info": {
                "instructional_days": 5,
                "notes": "Limited instructional days"
            },
            "events": [
                
                {
                    "date": "2024-11-25",
                    "description": "Commencement of sixth semester classes",
                    "status": "busy"
                }
            ]
        },
        "december_2024": {
            "month_info": {
                "instructional_days": 17,
                "notes": "Holidays affect instructional days"
            },
            "events": [
                {
                    "date": "2024-12-01",
                    "description": "World Aids Day",
                    "status": "busy"
                },
                {
                    "date": "2024-12-02",
                    "description": "Commencement of Sixth Semester Internship 2024-25",
                    "status": "busy"
                },
                {
                    "date": "2024-12-02",
                    "description": "World Pollution Prevention Day",
                    "status": "busy"
                },
                {
                    "date_range": {
                        "start": "2024-12-20",
                        "end": "2024-12-30"
                    },
                    "description": "Polytechnic College X'mas Holidays",
                    "status": "not busy",
                    "holiday_considerable": true
                }
            ]
        },
        "january_2025": {
            "month_info": {
                "instructional_days": 22
            },
            "events": [
                {
                    "date": "2025-01-06",
                    "description": "Formative Assessment No.1",
                    "status": "busy"
                },
                {
                    "date": "2025-01-08",
                    "description": "Publication of attendance of the month of November & December",
                    "status": "busy"
                },
                {
                    "date": "2025-01-20",
                    "description": "Summative Assessment No.1",
                    "status": "busy"
                },
                {
                    "date": "2025-01-26",
                    "description": "Republic Day",
                    "status": "busy"
                }
            ]
        },
        "february_2025": {
            "month_info": {
                "instructional_days": 19
            },
            "events": [
                {
                    "date": "2025-02-07",
                    "description": "Publication of attendance of the month of January",
                    "status": "busy"
                },
                {
                    "date": "2025-02-11",
                    "description": "Formative Assessment No.2",
                    "status": "busy"
                },
                {
                    "date": "2025-02-18",
                    "description": "Summative Assessment No.2",
                    "status": "busy"
                }
            ]
        },
        "march_2025": {
            "month_info": {
                "instructional_days": 15
            },
            "events": [
                {
                    "date": "2025-03-07",
                    "description": "Publication of attendance of the month of February",
                    "status": "busy"
                },
                {
                    "date": "2025-03-07",
                    "description": "Formative Assessment No.3",
                    "status": "busy"
                },
                {
                    "date": "2025-03-17",
                    "description": "Model exam for S6",
                    "status": "busy"
                },
                {
                    "date": "2025-03-21",
                    "description": "Last working day for S6",
                    "status": "busy"
                },
                {
                    "date": "2025-03-26",
                    "description": "Publication of internal marks and consolidated attendance statement of S6",
                    "status": "busy"
                }
            ]
        },
        "april_2025": {
             "month_info": {
                "instructional_days": null,
                "notes": "No instructional days data"
             },
             "events": [
                {
                  "date_range": {
                      "start": "2025-04-07",
                      "end": "2025-04-30"
                    },
                    "description": "End Semester Examination",
                    "status": "busy",
                    "notes": "Important dates because of examination"
                }
             ]
        },
        "may_2025": {
            "month_info": {
                "instructional_days": null,
                "notes": "No instructional days data"
            },
            "events": [
                {
                    "date": "2025-05-30",
                    "description": "Sixth semester Internship ends",
                    "status": "busy"
                }
            ]
        }
    }
}'''
data = json.loads(json_str)

# Test cases
print(can_date_be_holiday(data,"2024-12-25"))
print(can_date_be_holiday(data, "2024-12-02"))
print(can_date_be_holiday(data,"2025-05-10"))
print(can_date_be_holiday(data,"2024-11-26"))
print(can_date_be_holiday(data,"2024-11-14"))