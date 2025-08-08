from rest_framework.throttling import AnonRateThrottle


class BurstRateThrottle(AnonRateThrottle):
    rate = '60/minute'
    scope = 'burst'

class SustainedRateThrottle(AnonRateThrottle):
    rate = '1000/day'
    scope = 'sustained'