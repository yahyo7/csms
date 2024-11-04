from loguru import logger


async def update_charge_point_status(charge_point_id: str, status: str) -> None:
    logger.info(f"Updating charge point status (charge_point_id={charge_point_id}, status={status})")