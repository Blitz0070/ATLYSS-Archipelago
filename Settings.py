from typing import Union

from settings import Bool, Group, OptionalUserFolderPath

# File is Auto-generated, see: [https://github.com/SWCreeperKing/ApWorldFactories/tree/master/ApWorldFactories/Games]

class AtlyssSettings(Group):
    class ExportLogic(Bool):
        """Write atlyss_logic_pN.json to the spoiler output folder after generation (debug / UT)."""

    class PoptrackerPackPath(OptionalUserFolderPath):
        """Unpacked ATLYSS-AP-PopTracker folder (manifest.json at root). Used by Universal Tracker map tab."""

    export_logic: Union[ExportLogic, bool] = False
    atlyss_poptracker_path: Union[PoptrackerPackPath, str] = PoptrackerPackPath()