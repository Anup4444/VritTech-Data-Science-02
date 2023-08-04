import math
from datetime import datetime, timedelta

def calculate_sunrise_sunset(day, month, year, latitude, longitude, zenith):
    # Step 1: Calculate the day of the year
    N1 = math.floor(275 * month / 9)
    N2 = math.floor((month + 9) / 12)
    N3 = (1 + math.floor((year - 4 * math.floor(year / 4) + 2) / 3))
    N = N1 - (N2 * N3) + day - 30

    # Step 2: Convert the longitude to hour value and calculate an approximate time
    lngHour = longitude / 15
    t = N + ((6 - lngHour) / 24) if zenith == 'official' else N + ((18 - lngHour) / 24)

    # Step 3: Calculate the Sun's mean anomaly
    M = (0.9856 * t) - 3.289

    # Step 4: Calculate the Sun's true longitude
    L = M + (1.916 * math.sin(math.radians(M))) + (0.020 * math.sin(math.radians(2 * M))) + 282.634
    L = L - 360 if L >= 360 else L

    # Step 5a: Calculate the Sun's right ascension
    RA = math.atan(0.91764 * math.tan(math.radians(L)))
    RA = math.degrees(RA)
    RA = RA + 360 if RA < 0 else RA

    # Step 5b: Adjust the right ascension value to be in the same quadrant as L
    Lquadrant = (math.floor(L / 90)) * 90
    RAquadrant = (math.floor(RA / 90)) * 90
    RA = RA + (Lquadrant - RAquadrant)

    # Step 5c: Convert the right ascension value into hours
    RA = RA / 15

    # Step 6: Calculate the Sun's declination
    sinDec = 0.39782 * math.sin(math.radians(L))
    cosDec = math.cos(math.asin(sinDec))

    # Step 7: Calculate the Sun's local hour angle
    cosH = (math.cos(math.radians(zenith)) - (sinDec * math.sin(math.radians(latitude)))) / (cosDec * math.cos(math.radians(latitude)))
    if cosH > 1 or cosH < -1:
        return None  # The sun never rises/sets on the specified date and location

    # Step 7b: Finish calculating H and convert into hours
    H = math.acos(cosH)
    H = math.degrees(H)
    H = 360 - H if zenith == 'official' else H
    H = H / 15

    # Step 8: Calculate local mean time of rising/setting
    T = H + RA - (0.06571 * t) - 6.622

    # Step 9: Adjust back to UTC
    UT = T - lngHour
    UT = UT + 24 if UT < 0 else UT

    # Step 10: Convert UT value to local time zone of latitude/longitude
    local_offset = int(longitude / 15)  # Calculate local time zone offset
    localT = UT + local_offset
    localT = localT + 24 if localT < 0 else localT

    # Return the sunrise and sunset times as datetime objects
    sunrise_time = datetime(year, month, day, int(localT), int((localT % 1) * 60))
    sunset_time = sunrise_time + timedelta(hours=12)

    return sunrise_time, sunset_time

day, month, year = 25, 6, 1990
latitude, longitude = 40.9, -74.3
zenith = 'official'  # You can use 'civil', 'nautical', or 'astronomical' as well

sunrise, sunset = calculate_sunrise_sunset(day, month, year, latitude, longitude, zenith)
print("Sunrise:", sunrise.strftime('%H:%M'))
print("Sunset:", sunset.strftime('%H:%M'))
