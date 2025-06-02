"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint and then land at a nearby landing pad.
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


class DecisionWaypointLandingPads(base_decision.BaseDecision):
    """
    Travel to the designed waypoint and then land at the nearest landing pad.
    """

    def __init__(self, waypoint: location.Location, acceptance_radius: float) -> None:
        """
        Initialize all persistent variables here with self.
        """
        self.waypoint = waypoint
        print(f"Waypoint: {waypoint}")

        self.acceptance_radius = acceptance_radius
        self.reached_waypoint = False
        self.target_pad = None

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Add your own

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def run(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> commands.Command:
        """
        Make the drone fly to the waypoint and then land at the nearest landing pad.

        You are allowed to create as many helper methods as you want,
        as long as you do not change the __init__() and run() signatures.

        This method will be called in an infinite loop, something like this:

        ```py
        while True:
            report, landing_pad_locations = get_input()
            command = Decision.run(report, landing_pad_locations)
            put_output(command)
        ```
        """
        # Default command
        # command = commands.Command.create_null_command()

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Do something based on the report and the state of this class...
        current_position = report.position
        current_status = report.status

        # Phase 1: go to waypoint
        if not self.reached_waypoint:
            if self._distance(current_position, self.waypoint) <= self.acceptance_radius:
                self.reached_waypoint = True
                self.target_pad = self._find_closest_pad(current_position, landing_pad_locations)
                print(f"Reached waypoint. Closest pad: {self.target_pad}")
                return commands.Command.create_halt_command()

            if current_status == drone_status.DroneStatus.HALTED:
                dx, dy = self._get_relative_vector(current_position, self.waypoint)
                return commands.Command.create_set_relative_destination_command(dx, dy)

            return commands.Command.create_null_command()

        # Phase 2: go to landing pad
        if self._distance(current_position, self.target_pad) <= self.acceptance_radius:
            if current_status == drone_status.DroneStatus.HALTED:
                return commands.Command.create_land_command()
            else:
                return commands.Command.create_halt_command()

        if current_status == drone_status.DroneStatus.HALTED:
            dx, dy = self._get_relative_vector(current_position, self.target_pad)
            return commands.Command.create_set_relative_destination_command(dx, dy)

        return commands.Command.create_null_command()


        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def _distance(self, a: location.Location, b: location.Location) -> float:
        dx = a.location_x - b.location_x
        dy = a.location_y - b.location_y
        return (dx**2 + dy**2)**0.5

    def _get_relative_vector(self, from_pos: location.Location, to_pos: location.Location) -> tuple[float, float]:
        dx = to_pos.location_x - from_pos.location_x
        dy = to_pos.location_y - from_pos.location_y
        distance = (dx**2 + dy**2)**0.5
        if distance == 0:
            return (0.0, 0.0)
        max_step = 10.0
        scale = min(max_step / distance, 1.0)
        return (dx * scale, dy * scale)

    def _find_closest_pad(self, position: location.Location, pads: "list[location.Location]") -> location.Location:
        closest_pad = None
        min_dist_sq = float("inf")
        for pad in pads:
            dx = pad.location_x - position.location_x
            dy = pad.location_y - position.location_y
            dist_sq = dx * dx + dy * dy  # Avoid sqrt for performance
            if dist_sq < min_dist_sq:
                min_dist_sq = dist_sq
                closest_pad = pad
        return closest_pad
