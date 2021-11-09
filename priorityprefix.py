

SD_EMERG = 0
SD_ALERT = 1
SD_CRIT = 2
SD_ERR = 3
SD_WARNING = 4
SD_NOTICE = 5
SD_INFO = 6
SD_DEBUG = 7


def level_to_priority(level):
    if level > 45:
        return SD_CRIT
    if level > 35:
        return SD_ERR
    if level > 25:
        return SD_WARNING
    if level > 15:
        return SD_INFO
    return SD_DEBUG
