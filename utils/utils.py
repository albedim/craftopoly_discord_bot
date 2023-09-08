BASE_URL = "http://localhost:5000/api/v1"


def fixDate(date):
    return date.split("-")[2] + "/" + date.split("-")[1] + "/" + date.split("-")[0]


def fixTime(date):
    return date.split(":")[0] + ":" + date.split(":")[1]
