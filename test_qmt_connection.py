import logging
import os
import sys
import time
from pathlib import Path

from xtquant import xtconstant
from xtquant.xttrader import XtQuantTrader
from xtquant.xttype import StockAccount


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def main() -> int:
    qmt_account_identifier = os.environ.get("QMT_ACCOUNT_ID")
    if not qmt_account_identifier:
        logging.error("QMT_ACCOUNT_ID is required")
        return 2

    qmt_userdata_directory = Path(
        os.environ.get("QMT_USERDATA_PATH", r"C:\gjzqqmt\userdata_mini")
    )
    logging.info(
        "QMT connection test starting: account=%s userdata=%s",
        qmt_account_identifier,
        qmt_userdata_directory,
    )

    if not qmt_userdata_directory.is_dir():
        logging.error(
            "QMT userdata directory does not exist: %s. Start and log in to QMT first.",
            qmt_userdata_directory,
        )
        return 3

    session_identifier = int(time.time() * 1000) % 2_147_483_647
    qmt_trader = XtQuantTrader(str(qmt_userdata_directory), session_identifier)

    try:
        qmt_trader.start()
        connection_result = qmt_trader.connect()
        logging.info("QMT connect result: %s", connection_result)
        if connection_result != 0:
            logging.error("QMT connection failed")
            return 4

        stock_account = StockAccount(
            qmt_account_identifier,
            xtconstant.SECURITY_ACCOUNT,
        )
        subscription_result = qmt_trader.subscribe(stock_account)
        logging.info("QMT account subscription result: %s", subscription_result)
        if subscription_result != 0:
            logging.error("QMT account subscription failed")
            return 5

        account_asset = qmt_trader.query_stock_asset(stock_account)
        if account_asset is None:
            logging.error("QMT returned no account asset data")
            return 6

        logging.info(
            "QMT account asset query succeeded: account=%s cash=%s frozen_cash=%s "
            "market_value=%s total_asset=%s",
            account_asset.account_id,
            account_asset.cash,
            account_asset.frozen_cash,
            account_asset.market_value,
            account_asset.total_asset,
        )
        return 0
    except Exception:
        logging.exception("QMT connection test raised an exception")
        return 1
    finally:
        qmt_trader.stop()


if __name__ == "__main__":
    sys.exit(main())
