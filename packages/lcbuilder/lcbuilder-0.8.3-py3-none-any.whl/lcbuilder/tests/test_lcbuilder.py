import logging
import os
import unittest
from lcbuilder.lcbuilder_class import LcBuilder
from lcbuilder.objectinfo.InputObjectInfo import InputObjectInfo
from lcbuilder.objectinfo.MissionFfiCoordsObjectInfo import MissionFfiCoordsObjectInfo
from lcbuilder.objectinfo.MissionFfiIdObjectInfo import MissionFfiIdObjectInfo
from lcbuilder.objectinfo.MissionInputObjectInfo import MissionInputObjectInfo
from lcbuilder.objectinfo.MissionObjectInfo import MissionObjectInfo


class TestsLcBuilder(unittest.TestCase):
    def test_build_object_info(self):
        file = None
        cadence = 120
        sectors = "all"
        lcbuilder = LcBuilder()
        target_name = "TIC 1234"
        object_info = lcbuilder.build_object_info(target_name, None, sectors, file, cadence, None, None, None, None, None)
        assert object_info.mission_id() == target_name
        target_name = "KIC 1234"
        object_info = lcbuilder.build_object_info(target_name, None, sectors, file, cadence, None, None, None, None, None)
        assert object_info.mission_id() == target_name
        target_name = "EPIC 1234"
        object_info = lcbuilder.build_object_info(target_name, None, sectors, file, cadence, None, None, None, None, None)
        assert object_info.mission_id() == target_name
        target_name = "25.9_-19.3"
        cadence = 1800
        object_info = lcbuilder.build_object_info(target_name, None, sectors, file, cadence, None, None, None, None, None)
        assert object_info.mission_id() is None and object_info.sherlock_id() == "25.9_-19.3_FFI_all"
        target_name = "25.9_-19.3"
        cadence = 120
        try:
            lcbuilder.build_object_info(target_name, None, sectors, file, cadence, None, None, None, None,
                                                  None)
            assert False
        except ValueError as e:
            logging.info("Expected exception")
            # Expected exception
        target_name = "WHATEVER"
        file = "fake_lc.csv"
        object_info = lcbuilder.build_object_info(target_name, None, sectors, file, cadence, None, None, None, None, None)
        assert object_info.mission_id() is None and object_info.sherlock_id() == "INP_" + os.path.splitext(file)[0].replace("/", "_")


    def test_short_cadence(self):
        lc_build = LcBuilder().build(MissionObjectInfo("TIC 352315023", 'all'), "./")
        self.assertEqual(lc_build.cadence, 120)
        self.assertGreater(len(lc_build.lc), 0)
        self.__test_tess_star_params(lc_build.star_info)

    def test_short_cadence_kic(self):
        lc_build = LcBuilder().build(MissionObjectInfo("KIC 12557548", 'all'), "./")
        self.assertEqual(lc_build.cadence, 59)
        self.assertGreater(len(lc_build.lc), 0)
        self.__test_kepler_star_params(lc_build.star_info)

    def test_long_cadence_missing_star_kic(self):
        lc_build = LcBuilder().build(MissionFfiIdObjectInfo("KIC 12106934", 'all'), "./")
        self.assertEqual(lc_build.cadence, 1765)
        self.assertGreater(len(lc_build.lc), 0)

    def test_short_cadence_epic(self):
        lc_build = LcBuilder().build(MissionObjectInfo("EPIC 211945201", 'all'), "./")
        self.assertEqual(lc_build.cadence, 59)
        self.assertGreater(len(lc_build.lc), 0)
        self.__test_k2_star_params(lc_build.star_info)

    def test_long_cadence(self):
        lc_build = LcBuilder().build(MissionFfiIdObjectInfo("TIC 352315023", 'all'), "./")
        self.assertEqual(lc_build.cadence, 600)
        self.assertGreater(len(lc_build.lc), 0)
        self.__test_tess_star_params(lc_build.star_info)

    def test_long_cadence_coords(self):
        lc_build = LcBuilder().build(MissionFfiCoordsObjectInfo(300.47, -71.96, 'all'), "./")
        self.assertEqual(lc_build.cadence, 600)
        self.assertGreater(len(lc_build.lc), 0)
        self.__test_tess_star_params(lc_build.star_info)

    def test_input_with_id(self):
        directory = os.path.dirname(__file__) + "/input.csv"
        lc_build = LcBuilder().build(MissionInputObjectInfo("TIC 352315023", directory), "./")
        self.assertGreater(len(lc_build.lc), 0)
        self.__test_tess_star_params(lc_build.star_info)

    def test_input_without_id(self):
        directory = os.path.dirname(__file__) + "/input.csv"
        lc_build = LcBuilder().build(InputObjectInfo(directory), "./")
        self.assertGreater(len(lc_build.lc), 0)
        self.assertTrue(lc_build.star_info.mass_assumed)
        self.assertTrue(lc_build.star_info.radius_assumed)

    def __test_tess_star_params(self, star_info):
        self.assertAlmostEqual(star_info.mass, 0.47, 1)
        self.assertAlmostEqual(star_info.mass_min, 0.44, 2)
        self.assertAlmostEqual(star_info.mass_max, 0.5, 1)
        self.assertAlmostEqual(star_info.radius, 0.18, 1)
        self.assertAlmostEqual(star_info.radius_min, 0.076, 3)
        self.assertAlmostEqual(star_info.radius_max, 0.284, 3)
        self.assertEqual(star_info.teff, 31000)
        self.assertAlmostEqual(star_info.ra, 300.47, 2)
        self.assertAlmostEqual(star_info.dec, -71.96, 2)

    def __test_kepler_star_params(self, star_info):
        self.assertAlmostEqual(star_info.mass, 0.72, 2)
        self.assertAlmostEqual(star_info.mass_min, 0.22, 2)
        self.assertAlmostEqual(star_info.mass_max, 1.22, 2)
        self.assertAlmostEqual(star_info.radius, 0.734, 2)
        self.assertAlmostEqual(star_info.radius_min, 0.234, 2)
        self.assertAlmostEqual(star_info.radius_max, 1.234, 2)
        self.assertEqual(star_info.teff, 4571)
        self.assertAlmostEqual(star_info.ra, 290.966, 3)
        self.assertAlmostEqual(star_info.dec, 51.50472, 3)

    def __test_k2_star_params(self, star_info):
        self.assertAlmostEqual(star_info.mass, 1.102, 3)
        self.assertAlmostEqual(star_info.mass_min, 0.989, 3)
        self.assertAlmostEqual(star_info.mass_max, 1.215, 3)
        self.assertAlmostEqual(star_info.radius, 1.251, 2)
        self.assertAlmostEqual(star_info.radius_min, 1.012, 3)
        self.assertAlmostEqual(star_info.radius_max, 1.613, 3)
        self.assertEqual(star_info.teff, 6043)
        self.assertAlmostEqual(star_info.ra, 136.573975, 3)
        self.assertAlmostEqual(star_info.dec, 19.402252, 3)

    def test_build(self):
        lc_build = LcBuilder().build(MissionObjectInfo("TIC 352315023", [13]), "./")
        self.assertEqual(18107, len(lc_build.lc))
        self.assertEqual(20479, len(lc_build.lc_data))
        lc_build = LcBuilder().build(MissionObjectInfo("KIC 12557548", [13]), "./")
        self.assertEqual(127850, len(lc_build.lc))
        self.assertEqual(130290, len(lc_build.lc_data))
        lc_build = LcBuilder().build(MissionObjectInfo("EPIC 211945201", 'all'), "./")
        self.assertEqual(107670, len(lc_build.lc))
        self.assertEqual(116820, len(lc_build.lc_data))
        lc_build = LcBuilder().build(MissionFfiIdObjectInfo("KIC 12557548", [1]), "./")
        self.assertEqual(1543, len(lc_build.lc))
        self.assertEqual(1639, len(lc_build.lc_data))
        lc_build = LcBuilder().build(MissionFfiIdObjectInfo("EPIC 211945201", [5]), "./")
        self.assertEqual(3324, len(lc_build.lc))
        self.assertEqual(3663, len(lc_build.lc_data))
        lc_build = LcBuilder().build(MissionFfiIdObjectInfo("TIC 352315023", [13]), "./")
        self.assertEqual(1222, len(lc_build.lc))
        self.assertEqual(1320, len(lc_build.lc_data))

    def test_binning(self):
        directory = os.path.dirname(__file__) + "/input.csv"
        lc_build = LcBuilder().build(MissionInputObjectInfo("TIC 352315023", directory), "./")
        self.assertEqual(4551, len(lc_build.lc))
        lc_build = LcBuilder().build(MissionInputObjectInfo("TIC 352315023", directory, binning=2), "./")
        self.assertEqual(2893, len(lc_build.lc))
        lc_build = LcBuilder().build(MissionInputObjectInfo("TIC 352315023", directory, binning=4), "./")
        self.assertEqual(1771, len(lc_build.lc))


if __name__ == '__main__':
    unittest.main()
