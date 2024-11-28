import yaml
import logging
import logging.config
import traceback
import time


with open("logger.yaml") as f:
    loggerConfig = yaml.safe_load(f.read())
    logging.config.dictConfig(loggerConfig)

logger = logging.getLogger(__name__)


import src.gawin as gawin


def fighting() -> None:
    cooldown = 0
    fighting = False
    while True:
        startTime = time.time()
        if cooldown <= 0:
            inventory = gawin.getInventory()
            itemsMax = gawin.getCharacter()["inventory_max_items"]
            logger.debug(f"Inventory max items: {itemsMax}")
            itemsTotal = 0
            for item in inventory:
                itemsTotal += int(item["quantity"])
            inventoryPercentage = itemsTotal / itemsMax * 100
            if inventoryPercentage >= 98:
                logger.warning("Inventory almost full")
                logger.info(f"Inventory: {itemsTotal}/{itemsMax}")
                break
            logger.info(f"Inventory: {itemsTotal / itemsMax * 100:.1f}%")
            if fighting:
                cooldown = gawin.fight()
                fighting = False
            else:
                cooldown, needingHealth = gawin.heal()
                if needingHealth <= 0:
                    fighting = True

        else:
            cooldown -= time.time() - startTime

def farming():
    cooldown = 0
    arrived = True
    running = True
    while running:
        startTime = time.time()
        if cooldown <= 0:
            inventory = gawin.getInventory()
            itemsMax = gawin.getCharacter()["inventory_max_items"]
            logger.debug(f"Inventory max items: {itemsMax}")
            itemsTotal = 0
            for item in inventory:
                itemsTotal += int(item["quantity"])
            inventoryPercentage = itemsTotal / itemsMax * 100
            if inventoryPercentage >= 98:
                logger.warning("Inventory almost full")
                logger.info(f"Inventory: {itemsTotal}/{itemsMax}")
                break
            logger.info(f"Inventory: {itemsTotal / itemsMax * 100:.1f}%")
            if not arrived:
                cooldown, arrived = gawin.move((-1, 0))
            else:
                cooldown = gawin.harvest()
        else:
            cooldown -= time.time() - startTime

if __name__ == "__main__":
    try:
        farming()
        #fighting()

    except Exception:
        logger.critical(traceback.format_exc())
