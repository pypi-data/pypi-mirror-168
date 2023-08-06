import datetime
import typing

import numpy as np


def julian_day(time_of_interest: datetime.datetime) -> float:
    """ Compute the Julian day, i.e. number of days since Jan 1, 4713 BC 12 UT

    Parameters
    ----------
    time_of_interest: datetime.datetime
        What time you would like to compute the Julian Day of

    Returns
    -------
    float:
        Julian Day for time of interest
    """
    starting_point = 1721425.5  # Hard code julian_day(January 1, 1)
    start = datetime.datetime(1, 1, 1)
    diff = (
        time_of_interest - start
    ).total_seconds() / 86400  # Get days since January 1, 1
    return diff + starting_point


def sun_angle(
    time: datetime.datetime,
    lat: typing.Union[np.array, float],
    lon: typing.Union[np.array, float],
    altitude: float = 0.0,
) -> typing.Union[np.array, float]:
    """ Compute the altitude angle of the sun

    Parameters
    ----------
    time: datetime.datetime
        Date and time to compute angles
    lat: typing.Union[np.array, float]
        Latitude(s) of interest
    lon: typing.Union[np.array, float]
        Longitude(s) of interest
    altitude: float, optional
        Height at which to compute altitude angle

    Returns
    -------
    float:
        Altitude angle
    """
    # Check for out of bounds
    try:
        if (
            (lat < -90).any()
            or (lat > 90).any()
            or (lon < -180).any()
            or (lon > 180).any()
        ):
            raise ValueError("Latitude or Longitude out of bounds")
    except AttributeError:
        if (lat < -90) or (lat > 90) or (lon < -180) or (lon > 180):
            raise ValueError("Latitude or Longitude out of bounds")
    if altitude < 0:
        raise ValueError("Negative altitude is not allowed")

    k = np.pi / 180

    # Number of Julian Centuries since Jan 1, 2000 12 UT
    jd = julian_day(time)
    num_centuries = (jd - 2451545.0) / 36525.0
    num_centuries2 = num_centuries * num_centuries
    num_centuries3 = num_centuries2 * num_centuries

    # Solar Coordinates:
    # Mean anomaly:
    M = np.deg2rad(
        357.52910
        + 35999.05030 * num_centuries
        - 0.0001559 * num_centuries2
        - 0.00000048 * num_centuries3
    )  # [rad]
    # Mean longitude:
    L0 = 280.46645 + 36000.76983 * num_centuries + 0.0003032 * num_centuries2  # [deg]
    DL = (
        (1.914600 - 0.004817 * num_centuries - 0.000014 * num_centuries2) * np.sin(M)
        + (0.019993 - 0.000101 * num_centuries) * np.sin(2 * M)
        + 0.000290 * np.sin(3 * M)
    )

    # True longitude
    L = np.deg2rad(L0 + DL)  # [deg]

    # Convert ecliptic longitude L to right ascension RA and declination delta:
    eps = 0.40910500213454565  # [rad] obliquity of ecliptic 23.43999 degrees
    X = np.cos(L)
    Y = np.cos(eps) * np.sin(L)
    Z = np.sin(eps) * np.sin(L)
    R = np.sqrt(1 - Z ** 2)

    delta = np.arctan2(Z, R)  # [rad] declination -- latitude position of sun --
    right_ascension = 7.63943726841098 * np.arctan2(
        Y, (X + R)
    )  # [hours] right ascension
    right_ascension = right_ascension * 360 / 24  # [deg] right ascension

    # Compute Sidereal time at Greenwich (only depends on time)
    theta0 = (
        280.46061837
        + 360.98564736629 * (jd - 2451545.0)
        + 0.000387933 * num_centuries2
        - num_centuries3 / 38710000.0
    )  # [deg]
    theta0 = theta0 % 360

    theta = np.deg2rad(theta0 + lon)  # [rad]
    tau = theta - np.deg2rad(right_ascension)  # [rad]
    beta = np.deg2rad(lat)  # [rad]
    altitude_angle = np.rad2deg(
        np.arcsin(
            np.sin(beta) * np.sin(delta) + np.cos(beta) * np.cos(delta) * np.cos(tau)
        )
    )  # [deg]
    azimuth_angle = np.rad2deg(
        np.arctan2(
            -np.sin(tau), (np.cos(beta) * np.tan(delta) - np.sin(beta) * np.cos(tau))
        )
    )

    # Radius of earth
    R = 6370  # [km]

    altitude_angle_corrected = altitude_angle + np.rad2deg(
        np.arccos(R / (R + altitude))
    )
    return altitude_angle_corrected


def mask(
    time: datetime.datetime,
    lat_grid: np.ndarray,
    lon_grid: np.ndarray,
    altitude: float = 0.0,
) -> np.ndarray:
    """ Create a mask where 1s represent daytime and 0s represent nighttime from provided lat/lon grid

    Parameters
    ----------
    time: datetime.datetime
        Time of interest [UT]
    lat_grid: np.ndarray
        Meshgrid of latitude points
    lon_grid: np.ndarray
        Meshgrid of longitude points
    altitude: float, optional
        km above sea level

    Returns
    -------
    np.ndarray:
        Mask of where daytime (1s) and nighttime (0s) occurs
    """
    output = np.zeros(lon_grid.shape)
    output[sun_angle(time, lat_grid, lon_grid, altitude) > 0] = 1
    return output


def easy_mask(
    time: datetime.datetime,
    lat_range: tuple,
    lon_range: tuple,
    resolution: typing.Union[float, tuple] = 1.0,
    altitude: float = 0.0,
) -> np.ndarray:
    """ Create a mask where 1s represent daytime and 0s represent nighttime from extent/resolution

    Parameters
    ----------
    time: datetime.datetime
        Time of interest [UT]
    lat_range: tuple
        (lat_min, lat_max)
    lon_range: tuple
        (lon_min, lon_max)
    resolution: Union[float, tuple]
        Step size for the mask
    altitude: float
        km above sea level

    Returns
    -------
    np.ndarray:
        Mask of where daytime (1s) and nighttime (0s) occurs
    """
    try:
        lat_resolution, lon_resolution = resolution
    except TypeError:
        lat_resolution = resolution
        lon_resolution = resolution
    lats = np.arange(
        lat_range[0], lat_range[1] + lat_resolution / 10, lat_resolution
    )  # divide by 10 for floating point errors
    lons = np.arange(lon_range[0], lon_range[1] + lon_resolution / 10, lon_resolution)
    lon_grid, lat_grid = np.meshgrid(lons, lats)
    return mask(time, lat_grid, lon_grid, altitude)
