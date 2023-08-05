from dataclasses import dataclass

from ....constant import directory
from ....helper import operating_system
from ....model.viewport.device import DeviceViewportSize
from .page_load_strategy import PageLoadStrategy
from .timeout.settings import TimeoutSettings
from .type import BrowserType


@dataclass(kw_only=True, slots=True)
class BrowserSettings:
    """Class to configure the browser driver.

    headless: If enabled, note that some interactable methods, e.g. "select", aren't supported.

    screenshot_dir: Destination directory for screenshot files. If not set, default directory is from where the script is executed.

    viewport: Emulate a viewport size upon initiation by either a common device or a custom value in pixels "(width, height)". If no value, the browser's default is used."""

    type: BrowserType = BrowserType.EDGE if operating_system.is_windows() else BrowserType.CHROME
    headless: bool = False
    disable_images: bool = False
    page_load_strategy: PageLoadStrategy = PageLoadStrategy.NORMAL
    path_to_executable: str | None = None
    screenshot_dir: str = directory.CURRENT
    timeout: TimeoutSettings = TimeoutSettings()
    viewport: DeviceViewportSize | tuple[int, int] | None = None
