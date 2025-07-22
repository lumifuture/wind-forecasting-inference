FEATURE_NAMES = [
    'wind_speed', 'wind_direction', 'cabin_angle', 'total_cabin_angle',
    'paddle1_angle', 'paddle2_angle', 'paddle3_angle', 'outdoor_temp',
    'wind_speed_100m', 'wind_direction_100m', 'temperature', 'air_pressure', 'air_density',
    'hour', 'dayofweek', 'month',
    'power_lag_1', 'power_lag_2', 'power_lag_3', 'power_lag_4'
]

def extract_features(data_points):
    return [
        [getattr(dp, name, 0) if getattr(dp, name, None) is not None else 0 for name in FEATURE_NAMES]
        for dp in data_points
    ]