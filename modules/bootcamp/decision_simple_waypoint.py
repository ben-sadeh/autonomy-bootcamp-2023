"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint.
"""

from .. import commands
from .. import drone_report

# Disable for bootcamp use
# pylint: disable-next=unused-import
from .. import drone_status
from .. import location
from ..private.decision import base_decision

# Disable for bootcamp use
# No enable
# pylint: disable=duplicate-code,unused-argument


class DecisionSimpleWaypoint(base_decision.BaseDecision):
    """
    Travel to the designed waypoint.
    """

    def __init__(self, waypoint: location.Location, acceptance_radius: float) -> None:
        """
        Initialize all persistent variables here with self.
        """
        self.waypoint = waypoint
        print(f"Waypoint: {waypoint}")

        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Add your own

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def run(self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]") -> commands.Command:
        current_position = report.position
        current_status = report.status

        distance = self._distance_to_waypoint(current_position)

        if distance <= self.acceptance_radius:
            if current_status == drone_status.DroneStatus.HALTED:
                return commands.Command.create_land_command()
            else:
                return commands.Command.create_halt_command()

        if current_status == drone_status.DroneStatus.HALTED:
            dx, dy = self._get_relative_vector(current_position)
            return commands.Command.create_set_relative_destination_command(dx, dy)

        return commands.Command.create_null_command()


    def _distance_to_waypoint(self, position: location.Location) -> float:
        dx = self.waypoint.location_x - position.location_x
        dy = self.waypoint.location_y - position.location_y
        return (dx**2 + dy**2)**0.5

    def _get_relative_vector(self, position: location.Location) -> tuple[float, float]:
        dx = self.waypoint.location_x - position.location_x
        dy = self.waypoint.location_y - position.location_y
        distance = (dx**2 + dy**2)**0.5

        if distance == 0:
            return (0.0, 0.0)

        max_step = 10.0
        scale = min(max_step / distance, 1.0)
        return (dx * scale, dy * scale)
