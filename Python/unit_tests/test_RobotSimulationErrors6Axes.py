"""Test RoboDK InstructionListJoints() with expected simulation errors for robot with 6 axes"""

from parameterized import parameterized_class
from path_simulation import *
import test_RobotSimBase
from robolink import *


def get_program_wrist_singularity1():
    """Test program to simulate WristSingularity error"""
    j1 = [84.042754, -57.261200, 115.707342, 78.814999, -83.206905, 59.112086]
    f2 = [267.800000, -697.899998, 489.200000, -0.000000, -0.000000, -97.106527]
    f3 = [267.800000, -886.682410, 541.603649, 45.000000, 0.000000, 180.000000]
    f4 = [267.800000, -900.824545, 555.745785, 45.000000, 0.000000, 180.000000]
    #expectedSimulationError = PathErrorFlags.Kinematic | PathErrorFlags.PathSingularity | PathErrorFlags.WristSingularity# Prior to RoboDK v5.1.2 (inclusive), RoboDK used to report this error although the path is feasible
    expectedSimulationError = PathErrorFlags.InnacurateDueToLargeAxisMove # Time step needs to be reduced to properly calculate error flags
    steps = [
        # Step: name, move_type, tcp, pose, blending, speed, accel, expected_error):
        Step("1", MoveType.Joint, 0, j1, 10, 0, 0, 0),
        Step("2", MoveType.Frame, 0, f2, 10, 0, 0, 0),
        Step("3", MoveType.Frame, 0, f3, 10, 0, 0, expectedSimulationError), 
        Step("4", MoveType.Frame, 0, f4, 0, 0, 0, 0),
    ]
    return Program("WristSingularity", steps)


def get_program_wrist_singularity2():
    """Test program to simulate a path which is near kinematic limits"""
    j1 = [ 58.871249, -78.599411,  143.944527, 173.481676, 65.485694,   -87.285718]
    f2 = [247.580323, -793.574636, 574.200001, 0.000000,   -0.000000,  -154.799784]
    expectedSimulationError = PathErrorFlags.Kinematic | PathErrorFlags.PathSingularity | PathErrorFlags.WristSingularity
    steps = [
        # Step: name, move_type, tcp, pose, blending, speed, accel, expected_error):
        Step("J1", MoveType.Joint, 0, j1, 0, 0, 0, 0),
        Step("F2", MoveType.Frame, 0, f2, 1, 0, 0, expectedSimulationError), 
    ]
    return Program("WristSingularity", steps)


def get_program_180degree_rotation_error():
    """180 degree rotation error. Test PathFlipAxis Error."""
    j1 = [ 62.800000, -58.000000, 114.300000, -31.700000, -60.300000, 107.000000]
    f2 = [   247.718647,  -776.118962,   544.157022,     0,     0,  -180 ] # Make sure the orientation flips 180 deg exact, otherwise, blending will adjust the path
    f3 = [   147.718647,  -776.118962,   544.157022,     0,    180, -180] # default RoboDK tolerance for flip axis is 0.5 deg rotation (so a 179.5 deg rotation is allowed at most)
    expectedSimulationError = PathErrorFlags.PathFlipAxis ## currently not implemented in RoboDK
    # As of RoboDK 5.1.0, FlipAxis may be also reported as kinematic error if we try a move close to 180 deg outside the 0.5 deg tolerance
    steps = [
        # Step: name, move_type, tcp, pose, blending, speed, accel, expected_error):
        Step("J1", MoveType.Joint, 0, j1, 0, 0, 0, 0),
        Step("F2", MoveType.Frame, 0, f2, 1, 0, 0, 0),
        Step("F3", MoveType.Frame, 0, f3, 1, 0, 0, expectedSimulationError)
    ]
    return Program("180 degree rotation error", steps)

def get_program_kinematic_pathlimit1():
    """To large movement in short time. Crossing ToleranceSmoothKinematic limit"""
    j1 = [ 86.567590, -60.878784, 114.472076, -92.763651, 87.963609, -126.357581]
    f2 = [   247.500000,  -869.864902,   574.200001,     0.000001,     0.000000,   -90.000000 ]
    f3 = [   247.500000,  -869.864902,   554.200001,     0.000001,     0.000000,   -90.000000 ]
    f4 = [   247.500000,  -874.864902,   554.200001,     0.000001,     0.000000,   -90.000000 ]
    f5 = [   247.500000,  -874.864902,   545.600001,     0.000001,     0.000000,   -90.000000 ]
    f6 = [   117.866636,  -874.864929,   545.599975,     0.000001,    -6.810226,   -55.597047 ]
    expectedSimulationError = PathErrorFlags.Kinematic  
    steps = [
        # Step: name, move_type, tcp, pose, blending, speed, accel, expected_error):
        Step("J1", MoveType.Joint, 0, j1, 0, 0, 0, 0),
        Step("F2", MoveType.Frame, 0, f2, 1, 0, 0, 0),
        Step("F3", MoveType.Frame, 0, f3, 1, 0, 0, 0),
        Step("F4", MoveType.Frame, 0, f4, 1, 0, 0, 0),
        Step("F5", MoveType.Frame, 0, f5, 1, 0, 0, 0),  
        Step("F6", MoveType.Frame, 0, f6, 1, 0, 0, expectedSimulationError), 
    ]
    return Program("Kinematic PathLimit: large movement in short time", steps)

def get_program_kinematic_pathlimit2():
    """To large movement in short time. Crossing ToleranceSmoothKinematic limit"""
    j1 = [ -121.731234, -105.839164, 118.925433, 44.376981, 49.562618, 133.063482]
    f2 = [  -305.479377,   506.206249,   561.080615,  -179.352790,   -74.861742,  -134.816977 ]
    f3 = [  -280.574677,   506.130142,   567.817833,  -179.352790,   -74.861742,  -134.816977 ]
    f4 = [  -277.584253,   506.915648,   544.586082,   179.947088,   -75.021714,   -45.217495 ]
    f5 = [  -302.700873,   506.909442,   537.866308,   179.947088,   -75.021714,   -45.217495 ]
    f6 = [  -300.434263,   506.661885,   567.779535,   179.947088,   -75.021714,   -45.217495 ]
    #expectedSimulationError = PathErrorFlags.Kinematic # Prior to RoboDK v5.1.2 (inclusive), RoboDK used to report this error although the path is feasible
    expectedSimulationError = PathErrorFlags.InnacurateDueToLargeAxisMove # Time step needs to be reduced to properly calculate error flags
    steps = [
        # Step: name, move_type, tcp, pose, blending, speed, accel, expected_error):
        Step("J1", MoveType.Joint, 0, j1, 0, 0, 0, 0),
        Step("F2", MoveType.Frame, 0, f2, 1, 0, 0, 0),
        Step("F3", MoveType.Frame, 0, f3, 1, 0, 0, 0),
        Step("F4", MoveType.Frame, 0, f4, 1, 0, 0, expectedSimulationError), 
        Step("F5", MoveType.Frame, 0, f5, 1, 0, 0, 0),  
        Step("F6", MoveType.Frame, 0, f6, 1, 0, 0, 0),
    ]
    return Program("Kinematic PathLimit: large movement in short time", steps)

def get_program_front_back_singularity_wrist_close_to_axis_1():
    """The robot is too close to the front/back singularity (wrist to close to axis 1)"""
    j1 = [ 106.000000, -52.000000, -79.000000, -81.000000, 58.000000, -47.000000]
    f2 = [   681.000000,  -417.900000,  1063.200000,    -0.000000,   -77.000000,   180.000000 ]
    expectedSimulationError = PathErrorFlags.PathSingularity | PathErrorFlags.PathNearSingularity | PathErrorFlags.ShoulderSingularity
    steps = [
        # Step: name, move_type, tcp, pose, blending, speed, accel, expected_error):
        Step("J1", MoveType.Joint, 0, j1, 0, 0, 0, 0),
        Step("F2", MoveType.Frame, 0, f2, 1, 0, 0, expectedSimulationError), 
    ]
    return Program("singularity (wrist to close to axis 1) error", steps)
    

def get_program_test_fast_long_move():
    """When we request a time based result, the error reporting can be innacurate if the time step is too large or the speed is too fast"""
    j1 = [86.567590, -60.878784, 114.472076, 87.236349, -87.963609, -306.357582]
    f2 = [   650,  -650,   550,     0.000001,     0.000000,   -90.000000 ]
    f3 = [   650,  +650,   550,     0.000001,     0.000000,   -90.000000 ]
    expectedSimulationError = PathErrorFlags.NoError
    steps = [
        # Step: name, move_type, tcp, pose, blending, speed, accel, expected_error):
        Step("J1", MoveType.Joint, 0, j1, 0, 8000, 8000, 0),
        Step("F2", MoveType.Frame, 0, f2, 1, 8000, 8000, 0),
        Step("F3", MoveType.Frame, 0, f3, 1, 8000, 8000, expectedSimulationError)
    ]
    return Program("Kinematic PathLimit: large movement in short time", steps)

def get_program_wrist_singularity_RDK_91():
    """Test program near wrist singularity"""
    j1 = [-124.420433, -100.220908, 123.962337, 23.242314, 63.944991, 137.508752]
    f2 = [  -278.518943,   436.007618,   547.030830,   179.789916,   -74.994562,   -47.567604 ]
    f3 = [  -303.439195,   435.983125,   540.350978,   179.789916,   -74.994562,   -47.567604 ]
    f4 = [  -301.172585,   435.735568,   570.264206,   179.789916,   -74.994562,   -47.567604 ]
    f5 = [  -231.253202,   513.686454,   655.467183,   179.789916,   -74.994562,  -118.578163 ]
    j6 = [-116.562035, -101.182577, 117.673968, 29.901480, 56.537640, 144.298732]
    j7 = [-69.323892, -117.000000, 116.917103, 3.454614, 34.862541, -15.159028]
    j8 = [69.928026, -109.590561, 148.647412, -21.437124, -0.098633, -8.370814]
    #expectedSimulationError = PathErrorFlags.PathSingularity | PathErrorFlags.PathNearSingularity | PathErrorFlags.WristSingularity # Prior to RoboDK v5.1.2 (inclusive), RoboDK used to report this error although the path is feasible
    expectedSimulationError = PathErrorFlags.InnacurateDueToLargeAxisMove # Time step needs to be reduced to properly calculate error flags
    steps = [
        # Step: name, move_type, tcp, pose, blending, speed, accel):
        Step("J1", MoveType.Joint, 0, j1, 10, 0, 0),
        Step("F2", MoveType.Frame, 0, f2, 1, 0, 0),
        Step("F3", MoveType.Frame, 0, f3, 0, 0, 0),
        Step("F4", MoveType.Frame, 0, f4, 1, 0, 0),
        Step("F5", MoveType.Frame, 0, f5, 1, 0, 0),
        Step("J6", MoveType.Joint, 0, j6, 10, 0, 0),
        Step("J7", MoveType.Joint, 0, j7, 10, 0, 0),
        Step("J8", MoveType.Joint, 0, j8, 10, 0, 0, expectedSimulationError),
    ]
    return Program("Wrist Singularity", steps)

def get_program_path_invalid_target_rdk_93():
    """Target StepId 65 can not be reached"""
    j1 = [-121.962375, -102.168116, 105.538444, 18.089514, 86.239362, 148.055458]
    f2 = [  -307.346432,   439.570058,   576.803381,  -179.352794,   -74.861742,   -99.294176 ]
    f3 = [  -282.441732,   439.493952,   583.540599,  -179.352794,   -74.861742,   -99.294176 ]
    f4 = [  -267.103305,   434.010573,   516.128581,   179.777317,   -74.944947,   -33.895889 ]
    f5 = [  -292.017764,   433.984527,   509.427158,   179.777317,   -74.944947,   -33.895889 ]
    f6 = [  -289.751154,   433.736971,   539.340385,   179.777317,   -74.944947,   -33.895889 ]
    f7 = [  -239.806166,   432.381194,   699.351823,   179.777317,   -74.944947,   -33.895889 ]
    j8 = [0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000]
    j9 = [79.238350, -54.625500, 102.860318, -115.621424, 68.885526, -126.911760]
    f10 = [   312.309807,  -910.024549,   574.500010,    -0.000000,     0.000000,  -111.978180 ]
    expectedSimulationError = PathErrorFlags.PathLimit  
    steps = [
        # Step: name, move_type, tcp, pose, blending, speed, accel):
        Step("StepId 61", MoveType.Joint, 0, j1, 10, 0, 0),
        Step("StepId 58", MoveType.Frame, 0, f2, 0, 0, 0),
        Step("StepId 62", MoveType.Frame, 0, f3, 10, 0, 0),
        Step("StepId 63", MoveType.Frame, 0, f4, 10, 0, 0),
        Step("StepId 60", MoveType.Frame, 0, f5, 0, 0, 0),
        Step("StepId 64", MoveType.Frame, 0, f6, 10, 0, 0),
        Step("StepId 65", MoveType.Frame, 0, f7, 10, 0, 0, expectedSimulationError), 
        Step("StepId 66", MoveType.Joint, 0, j8, 10, 0, 0, 0),
        Step("StepId 81", MoveType.Joint, 0, j9, 10, 0, 0, 0),
        Step("StepId 83", MoveType.Frame, 0, f10, 1, 0, 0, 0),
    ]
    return Program("target_StepId65_can_not_be_reached", steps)
    
    
     
def get_program_Arc_InValidMove():
    """Test program was previously crashing during path simulation."""
    j1 = [85.313866, -54.353057, 109.847412, 90.670697, -90.461034, 55.497054]
    f1 = [   252.127218,  -530.131963,   529.199999,   -84.500000,    -0.000001,    -0.000000 ]
    f2 = [   384.041242,  -453.856457,   529.200000,   -84.500000,    -0.000001,    -0.000000 ]
    # f3 = [   289.724650,  -298.049571,   529.200000,   -84.500000,    -0.000001,    -0.000000 ]

    expectedSimulationError = PathErrorFlags.InvalidArcMove
    steps = [
        # Step: name, move_type, tcp, pose, blending, speed, accel):
        Step("J1", MoveType.Joint, 0, j1, 0, 0, 0),
        Step("F1", MoveType.Frame, 0, f1, 0, 0, 0),
        Step("F2", MoveType.Arc, 0, f2, 0, 0, 0, expectedSimulationError, f1)
    ]
    return Program("Invalid_ArcMove", steps)

@parameterized_class(
    ("test_name", "sim_type", "sim_step_mm", "sim_step_deg", "sim_step_time"), [
        (f"TimeBasedX({test_RobotSimBase.step_time_RM:0.4f}ms)".replace(".", test_RobotSimBase.dot_repr),
         InstructionListJointsFlags.TimeBased, None, None, test_RobotSimBase.step_time_RM)
    ])
class TestRobotSimulationError6Axes(test_RobotSimBase.TestRobotSimBase):

    def load_robot_cell(self):
        self.robot, self.tools = load_file(r"Robot_2TCP.rdk")

    def test_wrist_wrist_singularity1(self):
        """Test program wrist singularity error"""
        self.program = get_program_wrist_singularity1()
        self._test_program(verbose=False)

    def test_wrist_wrist_singularity2(self):
        """Test program wrist singularity error"""
        self.program = get_program_wrist_singularity2()
        self._test_program(verbose=False)

    def test_program_wrist_singularity_RDK_91(self):
        """Test singularity error"""
        self.program = get_program_wrist_singularity_RDK_91()
        self._test_program(verbose=False)
       
    def test_180degree_rotation_error_rdk_94(self):
        """Test 180 degree roation error: AxisFLip"""
        self.program = get_program_180degree_rotation_error()
        self._test_program(verbose=False)

    def test_kinematic_pathlimit1(self):
        """Test smoothe kinematic error (axis movement to large in one step)"""
        self.program = get_program_kinematic_pathlimit1()
        self._test_program(verbose=False)

    def test_kinematic_pathlimit2(self):
        """Test smooth kinematic error (axis movement to large in one step)"""
        self.program = get_program_kinematic_pathlimit2()
        self._test_program(verbose=False)

    def test_program_path_invalid_target_rdk_93(self):
        """One or more targets are not reachable or missing."""
        self.program = get_program_path_invalid_target_rdk_93()
        self._test_program(verbose=False)

    def test_program_path_invalid_ArcMove(self):
        """One or more targets are not reachable or missing."""
        self.program = get_program_Arc_InValidMove()
        self._test_program(verbose=False)    

    def test_wrist_close_to_axis_1_error(self):
        """The robot is too close to the front/back singularity. Wrist close to axis 1"""
        self.program = get_program_front_back_singularity_wrist_close_to_axis_1()
        self._test_program(verbose=False)

    def test_fast_long_move_report(self):
        """The robot is too close to the front/back singularity. Wrist close to axis 1"""
        self.program = get_program_test_fast_long_move()
        self._test_program(verbose=False)


if __name__ == '__main__':
    unittest.main()
