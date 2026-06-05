from typing import Union

from settings import Group, Bool

# File is Auto-generated, see: [https://github.com/SWCreeperKing/ApWorldFactories/tree/master/ApWorldFactories/Games]

class AtlyssSettings(Group):
    class ExportLogic(Bool):
        """Write atlyss_logic_pN.json to the spoiler output folder after generation (debug / UT)."""

    export_logic: Union[ExportLogic, bool] = False