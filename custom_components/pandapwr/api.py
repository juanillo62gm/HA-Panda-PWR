import aiohttp
import async_timeout


class PandaPWRApi:
    def __init__(self, ip_address: str):
        """Initialize the API client."""
        self._base_url = f"http://{ip_address}"
        self._session = aiohttp.ClientSession()

    async def test_connection(self) -> bool:
        """Test if the connection to the device can be established."""
        try:
            async with async_timeout.timeout(10):
                async with self._session.get(
                    f"{self._base_url}/update_ele_data"
                ) as response:
                    return response.status == 200
        except Exception:
            return False

    async def get_data(self) -> dict:
        """Fetch data from the device."""
        async with async_timeout.timeout(10):
            async with self._session.get(
                f"{self._base_url}/update_ele_data"
            ) as response:
                return await response.json()

    async def set_power_state(self, state: int):
        """Set power state (0 for off, 1 for on) using RAW payload."""
        payload = f"power={state}"
        async with self._session.post(
            f"{self._base_url}/set", data=payload
        ) as response:
            return response.status == 200

    async def set_usb_state(self, state: int):
        """Set USB state (0 for off, 1 for on) using RAW payload."""
        payload = f"usb={state}"
        async with self._session.post(
            f"{self._base_url}/set", data=payload
        ) as response:
            return response.status == 200
