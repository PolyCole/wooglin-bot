from .custom_block_elements import *
from slackblocks import SectionBlock, DividerBlock, HeaderBlock


def get_sb_shift_blocks(title, date, time_start, time_end, brothers):
    time_format = "%-I:%M %p on %A, %B %d %Y"

    blocks = [
        HeaderBlock(f":no_entry_sign: :beer: Sober Bro Shift Report {date}"),
        SectionBlock(f"*Shift Title*: {title}"),
        SectionBlock(f"*Shift Start*: {time_start.strftime(time_format)}"),
        SectionBlock(f"*Shift End*: {time_end.strftime(time_format)}"),
        DividerBlock(),
        SectionBlock(f"*Assigned Brothers*:")
    ]

    counter = 1

    for brother in brothers:
        blocks.append(SectionBlock(f"{counter}. {brother['name']} ({brother['phone']})"))
        counter += 1

    return blocks
