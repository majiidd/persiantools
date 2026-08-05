"""Validation against the official Iranian calendar authority.

The table below is the leap-year (kabiseh) data published by the Calendar
Center of the Institute of Geophysics, University of Tehran -- the body that
determines the official Iranian calendar:
https://calendar.ut.ac.ir/documents/2139738/7092644/Kabise+Shamsi+1206-1498.pdf

Each row gives a Jalali year, whether it is a leap year (marked with * for
four-year and ** for five-year leap intervals in the original document), and
the Gregorian date of 1 Farvardin of that year. The plain-text transcription
of the PDF is dedicated to the public domain (CC0 1.0).
"""

from datetime import date, timedelta
from unittest import TestCase

from persiantools.jdatetime import JalaliDate

# (jalali_year, is_leap, gregorian_year, gregorian_month, gregorian_day of 1 Farvardin)
_OFFICIAL_KABISE = [
    (1206, False, 1827, 3, 22),
    (1207, False, 1828, 3, 21),
    (1208, False, 1829, 3, 21),
    (1209, False, 1830, 3, 21),
    (1210, True, 1831, 3, 21),
    (1211, False, 1832, 3, 21),
    (1212, False, 1833, 3, 21),
    (1213, False, 1834, 3, 21),
    (1214, True, 1835, 3, 21),
    (1215, False, 1836, 3, 21),
    (1216, False, 1837, 3, 21),
    (1217, False, 1838, 3, 21),
    (1218, True, 1839, 3, 21),
    (1219, False, 1840, 3, 21),
    (1220, False, 1841, 3, 21),
    (1221, False, 1842, 3, 21),
    (1222, True, 1843, 3, 21),
    (1223, False, 1844, 3, 21),
    (1224, False, 1845, 3, 21),
    (1225, False, 1846, 3, 21),
    (1226, True, 1847, 3, 21),
    (1227, False, 1848, 3, 21),
    (1228, False, 1849, 3, 21),
    (1229, False, 1850, 3, 21),
    (1230, True, 1851, 3, 21),
    (1231, False, 1852, 3, 21),
    (1232, False, 1853, 3, 21),
    (1233, False, 1854, 3, 21),
    (1234, True, 1855, 3, 21),
    (1235, False, 1856, 3, 21),
    (1236, False, 1857, 3, 21),
    (1237, False, 1858, 3, 21),
    (1238, True, 1859, 3, 21),
    (1239, False, 1860, 3, 21),
    (1240, False, 1861, 3, 21),
    (1241, False, 1862, 3, 21),
    (1242, False, 1863, 3, 21),
    (1243, True, 1864, 3, 20),
    (1244, False, 1865, 3, 21),
    (1245, False, 1866, 3, 21),
    (1246, False, 1867, 3, 21),
    (1247, True, 1868, 3, 20),
    (1248, False, 1869, 3, 21),
    (1249, False, 1870, 3, 21),
    (1250, False, 1871, 3, 21),
    (1251, True, 1872, 3, 20),
    (1252, False, 1873, 3, 21),
    (1253, False, 1874, 3, 21),
    (1254, False, 1875, 3, 21),
    (1255, True, 1876, 3, 20),
    (1256, False, 1877, 3, 21),
    (1257, False, 1878, 3, 21),
    (1258, False, 1879, 3, 21),
    (1259, True, 1880, 3, 20),
    (1260, False, 1881, 3, 21),
    (1261, False, 1882, 3, 21),
    (1262, False, 1883, 3, 21),
    (1263, True, 1884, 3, 20),
    (1264, False, 1885, 3, 21),
    (1265, False, 1886, 3, 21),
    (1266, False, 1887, 3, 21),
    (1267, True, 1888, 3, 20),
    (1268, False, 1889, 3, 21),
    (1269, False, 1890, 3, 21),
    (1270, False, 1891, 3, 21),
    (1271, True, 1892, 3, 20),
    (1272, False, 1893, 3, 21),
    (1273, False, 1894, 3, 21),
    (1274, False, 1895, 3, 21),
    (1275, False, 1896, 3, 20),
    (1276, True, 1897, 3, 20),
    (1277, False, 1898, 3, 21),
    (1278, False, 1899, 3, 21),
    (1279, False, 1900, 3, 21),
    (1280, True, 1901, 3, 21),
    (1281, False, 1902, 3, 22),
    (1282, False, 1903, 3, 22),
    (1283, False, 1904, 3, 21),
    (1284, True, 1905, 3, 21),
    (1285, False, 1906, 3, 22),
    (1286, False, 1907, 3, 22),
    (1287, False, 1908, 3, 21),
    (1288, True, 1909, 3, 21),
    (1289, False, 1910, 3, 22),
    (1290, False, 1911, 3, 22),
    (1291, False, 1912, 3, 21),
    (1292, True, 1913, 3, 21),
    (1293, False, 1914, 3, 22),
    (1294, False, 1915, 3, 22),
    (1295, False, 1916, 3, 21),
    (1296, True, 1917, 3, 21),
    (1297, False, 1918, 3, 22),
    (1298, False, 1919, 3, 22),
    (1299, False, 1920, 3, 21),
    (1300, True, 1921, 3, 21),
    (1301, False, 1922, 3, 22),
    (1302, False, 1923, 3, 22),
    (1303, False, 1924, 3, 21),
    (1304, True, 1925, 3, 21),
    (1305, False, 1926, 3, 22),
    (1306, False, 1927, 3, 22),
    (1307, False, 1928, 3, 21),
    (1308, False, 1929, 3, 21),
    (1309, True, 1930, 3, 21),
    (1310, False, 1931, 3, 22),
    (1311, False, 1932, 3, 21),
    (1312, False, 1933, 3, 21),
    (1313, True, 1934, 3, 21),
    (1314, False, 1935, 3, 22),
    (1315, False, 1936, 3, 21),
    (1316, False, 1937, 3, 21),
    (1317, True, 1938, 3, 21),
    (1318, False, 1939, 3, 22),
    (1319, False, 1940, 3, 21),
    (1320, False, 1941, 3, 21),
    (1321, True, 1942, 3, 21),
    (1322, False, 1943, 3, 22),
    (1323, False, 1944, 3, 21),
    (1324, False, 1945, 3, 21),
    (1325, True, 1946, 3, 21),
    (1326, False, 1947, 3, 22),
    (1327, False, 1948, 3, 21),
    (1328, False, 1949, 3, 21),
    (1329, True, 1950, 3, 21),
    (1330, False, 1951, 3, 22),
    (1331, False, 1952, 3, 21),
    (1332, False, 1953, 3, 21),
    (1333, True, 1954, 3, 21),
    (1334, False, 1955, 3, 22),
    (1335, False, 1956, 3, 21),
    (1336, False, 1957, 3, 21),
    (1337, True, 1958, 3, 21),
    (1338, False, 1959, 3, 22),
    (1339, False, 1960, 3, 21),
    (1340, False, 1961, 3, 21),
    (1341, False, 1962, 3, 21),
    (1342, True, 1963, 3, 21),
    (1343, False, 1964, 3, 21),
    (1344, False, 1965, 3, 21),
    (1345, False, 1966, 3, 21),
    (1346, True, 1967, 3, 21),
    (1347, False, 1968, 3, 21),
    (1348, False, 1969, 3, 21),
    (1349, False, 1970, 3, 21),
    (1350, True, 1971, 3, 21),
    (1351, False, 1972, 3, 21),
    (1352, False, 1973, 3, 21),
    (1353, False, 1974, 3, 21),
    (1354, True, 1975, 3, 21),
    (1355, False, 1976, 3, 21),
    (1356, False, 1977, 3, 21),
    (1357, False, 1978, 3, 21),
    (1358, True, 1979, 3, 21),
    (1359, False, 1980, 3, 21),
    (1360, False, 1981, 3, 21),
    (1361, False, 1982, 3, 21),
    (1362, True, 1983, 3, 21),
    (1363, False, 1984, 3, 21),
    (1364, False, 1985, 3, 21),
    (1365, False, 1986, 3, 21),
    (1366, True, 1987, 3, 21),
    (1367, False, 1988, 3, 21),
    (1368, False, 1989, 3, 21),
    (1369, False, 1990, 3, 21),
    (1370, True, 1991, 3, 21),
    (1371, False, 1992, 3, 21),
    (1372, False, 1993, 3, 21),
    (1373, False, 1994, 3, 21),
    (1374, False, 1995, 3, 21),
    (1375, True, 1996, 3, 20),
    (1376, False, 1997, 3, 21),
    (1377, False, 1998, 3, 21),
    (1378, False, 1999, 3, 21),
    (1379, True, 2000, 3, 20),
    (1380, False, 2001, 3, 21),
    (1381, False, 2002, 3, 21),
    (1382, False, 2003, 3, 21),
    (1383, True, 2004, 3, 20),
    (1384, False, 2005, 3, 21),
    (1385, False, 2006, 3, 21),
    (1386, False, 2007, 3, 21),
    (1387, True, 2008, 3, 20),
    (1388, False, 2009, 3, 21),
    (1389, False, 2010, 3, 21),
    (1390, False, 2011, 3, 21),
    (1391, True, 2012, 3, 20),
    (1392, False, 2013, 3, 21),
    (1393, False, 2014, 3, 21),
    (1394, False, 2015, 3, 21),
    (1395, True, 2016, 3, 20),
    (1396, False, 2017, 3, 21),
    (1397, False, 2018, 3, 21),
    (1398, False, 2019, 3, 21),
    (1399, True, 2020, 3, 20),
    (1400, False, 2021, 3, 21),
    (1401, False, 2022, 3, 21),
    (1402, False, 2023, 3, 21),
    (1403, True, 2024, 3, 20),
    (1404, False, 2025, 3, 21),
    (1405, False, 2026, 3, 21),
    (1406, False, 2027, 3, 21),
    (1407, False, 2028, 3, 20),
    (1408, True, 2029, 3, 20),
    (1409, False, 2030, 3, 21),
    (1410, False, 2031, 3, 21),
    (1411, False, 2032, 3, 20),
    (1412, True, 2033, 3, 20),
    (1413, False, 2034, 3, 21),
    (1414, False, 2035, 3, 21),
    (1415, False, 2036, 3, 20),
    (1416, True, 2037, 3, 20),
    (1417, False, 2038, 3, 21),
    (1418, False, 2039, 3, 21),
    (1419, False, 2040, 3, 20),
    (1420, True, 2041, 3, 20),
    (1421, False, 2042, 3, 21),
    (1422, False, 2043, 3, 21),
    (1423, False, 2044, 3, 20),
    (1424, True, 2045, 3, 20),
    (1425, False, 2046, 3, 21),
    (1426, False, 2047, 3, 21),
    (1427, False, 2048, 3, 20),
    (1428, True, 2049, 3, 20),
    (1429, False, 2050, 3, 21),
    (1430, False, 2051, 3, 21),
    (1431, False, 2052, 3, 20),
    (1432, True, 2053, 3, 20),
    (1433, False, 2054, 3, 21),
    (1434, False, 2055, 3, 21),
    (1435, False, 2056, 3, 20),
    (1436, True, 2057, 3, 20),
    (1437, False, 2058, 3, 21),
    (1438, False, 2059, 3, 21),
    (1439, False, 2060, 3, 20),
    (1440, False, 2061, 3, 20),
    (1441, True, 2062, 3, 20),
    (1442, False, 2063, 3, 21),
    (1443, False, 2064, 3, 20),
    (1444, False, 2065, 3, 20),
    (1445, True, 2066, 3, 20),
    (1446, False, 2067, 3, 21),
    (1447, False, 2068, 3, 20),
    (1448, False, 2069, 3, 20),
    (1449, True, 2070, 3, 20),
    (1450, False, 2071, 3, 21),
    (1451, False, 2072, 3, 20),
    (1452, False, 2073, 3, 20),
    (1453, True, 2074, 3, 20),
    (1454, False, 2075, 3, 21),
    (1455, False, 2076, 3, 20),
    (1456, False, 2077, 3, 20),
    (1457, True, 2078, 3, 20),
    (1458, False, 2079, 3, 21),
    (1459, False, 2080, 3, 20),
    (1460, False, 2081, 3, 20),
    (1461, True, 2082, 3, 20),
    (1462, False, 2083, 3, 21),
    (1463, False, 2084, 3, 20),
    (1464, False, 2085, 3, 20),
    (1465, True, 2086, 3, 20),
    (1466, False, 2087, 3, 21),
    (1467, False, 2088, 3, 20),
    (1468, False, 2089, 3, 20),
    (1469, True, 2090, 3, 20),
    (1470, False, 2091, 3, 21),
    (1471, False, 2092, 3, 20),
    (1472, False, 2093, 3, 20),
    (1473, False, 2094, 3, 20),
    (1474, True, 2095, 3, 20),
    (1475, False, 2096, 3, 20),
    (1476, False, 2097, 3, 20),
    (1477, False, 2098, 3, 20),
    (1478, True, 2099, 3, 20),
    (1479, False, 2100, 3, 21),
    (1480, False, 2101, 3, 21),
    (1481, False, 2102, 3, 21),
    (1482, True, 2103, 3, 21),
    (1483, False, 2104, 3, 21),
    (1484, False, 2105, 3, 21),
    (1485, False, 2106, 3, 21),
    (1486, True, 2107, 3, 21),
    (1487, False, 2108, 3, 21),
    (1488, False, 2109, 3, 21),
    (1489, False, 2110, 3, 21),
    (1490, True, 2111, 3, 21),
    (1491, False, 2112, 3, 21),
    (1492, False, 2113, 3, 21),
    (1493, False, 2114, 3, 21),
    (1494, True, 2115, 3, 21),
    (1495, False, 2116, 3, 21),
    (1496, False, 2117, 3, 21),
    (1497, False, 2118, 3, 21),
    (1498, True, 2119, 3, 21),
]


class OfficialKabiseTestCase(TestCase):
    def test_table_integrity(self):
        # The transcription must cover 1206..1498 contiguously, and a starred
        # year must be exactly one whose next Norouz is 366 days later.
        self.assertEqual(len(_OFFICIAL_KABISE), 293)
        self.assertEqual(_OFFICIAL_KABISE[0][0], 1206)
        self.assertEqual(_OFFICIAL_KABISE[-1][0], 1498)

        for (year, leap, *norouz), (next_year, _, *next_norouz) in zip(_OFFICIAL_KABISE, _OFFICIAL_KABISE[1:]):
            self.assertEqual(next_year, year + 1)
            year_length = (date(*next_norouz) - date(*norouz)).days
            self.assertEqual(year_length, 366 if leap else 365, f"year {year}")

    def test_norouz_to_gregorian(self):
        for year, _, gy, gm, gd in _OFFICIAL_KABISE:
            self.assertEqual(JalaliDate(year, 1, 1).to_gregorian(), date(gy, gm, gd), f"1 Farvardin {year}")

    def test_norouz_from_gregorian(self):
        for year, _, gy, gm, gd in _OFFICIAL_KABISE:
            self.assertEqual(JalaliDate.to_jalali(date(gy, gm, gd)), JalaliDate(year, 1, 1), f"{gy}-{gm:02d}-{gd:02d}")

    def test_is_leap_matches_official(self):
        for year, leap, *_ in _OFFICIAL_KABISE:
            self.assertEqual(JalaliDate.is_leap(year), leap, f"year {year}")

    def test_esfand_length_matches_official(self):
        for year, leap, *_ in _OFFICIAL_KABISE:
            self.assertEqual(JalaliDate.days_in_month(12, year), 30 if leap else 29, f"Esfand {year}")

    def test_year_boundaries(self):
        # The day before each official Norouz must be the last day of Esfand of
        # the previous year, in both conversion directions.
        one_day = timedelta(days=1)

        for (prev_year, prev_leap, *_), (year, _, gy, gm, gd) in zip(_OFFICIAL_KABISE, _OFFICIAL_KABISE[1:]):
            eve = date(gy, gm, gd) - one_day
            last_esfand_day = 30 if prev_leap else 29

            self.assertEqual(JalaliDate.to_jalali(eve), JalaliDate(prev_year, 12, last_esfand_day), f"eve of {year}")
            self.assertEqual(JalaliDate(prev_year, 12, last_esfand_day).to_gregorian(), eve, f"end of {prev_year}")

    def test_round_trip_full_official_range(self):
        # Walk every Gregorian day covered by the official table (1 Farvardin
        # 1206 through the last day of 1498) and require an exact round trip
        # advancing one Jalali day at a time.
        first_year = _OFFICIAL_KABISE[0]
        last_year = _OFFICIAL_KABISE[-1]

        start = date(*first_year[2:])
        end = date(*last_year[2:]) + timedelta(days=(366 if last_year[1] else 365) - 1)

        previous = JalaliDate.to_jalali(start)
        self.assertEqual(previous, JalaliDate(first_year[0], 1, 1))
        self.assertEqual(previous.to_gregorian(), start)

        one_day = timedelta(days=1)
        gdate = start + one_day
        while gdate <= end:
            jdate = JalaliDate.to_jalali(gdate)
            self.assertEqual(jdate - previous, one_day, gdate)
            self.assertEqual(jdate.to_gregorian(), gdate, gdate)
            previous = jdate
            gdate += one_day

        self.assertEqual(previous, JalaliDate(last_year[0], 12, 30))
