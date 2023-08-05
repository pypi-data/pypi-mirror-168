# Copyright 2022 macanudo527
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Binance.com REST plugin links:
# REST API: https://binance-docs.github.io/apidocs/
# Authentication: https://binance-docs.github.io/apidocs/spot/en/#introduction
# Endpoint: https://api.binance.com

# CCXT documentation:
# https://docs.ccxt.com/en/latest/index.html

# pylint: disable=too-many-lines

import json
import logging
import re
from datetime import datetime, timezone
from time import sleep
from typing import Any, Dict, List, NamedTuple, Optional, Union

from ccxt import DDoSProtection, Exchange, InvalidNonce, binance
from rp2.logger import create_logger
from rp2.rp2_decimal import ZERO, RP2Decimal

from dali.abstract_input_plugin import AbstractInputPlugin
from dali.abstract_transaction import AbstractTransaction
from dali.configuration import Keyword
from dali.in_transaction import InTransaction
from dali.intra_transaction import IntraTransaction
from dali.out_transaction import OutTransaction

# Native format keywords
_ACCOUNT_PROFITS: str = "accountProfits"
_ALGO: str = "algo"
_ALGO_NAME: str = "algoName"
_AMOUNT: str = "amount"
_ASSET: str = "asset"
_BEGIN_TIME: str = "beginTime"
_BUY: str = "buy"  # CCXT only variable
_COIN: str = "coin"
_COIN_NAME: str = "coinName"
_COST: str = "cost"  # CCXT only variable
_CREATE_TIME: str = "createTime"
_CRYPTOCURRENCY: str = "cryptoCurrency"
_CURRENCY: str = "currency"  # CCXT only variable
_DAILY: str = "DAILY"
_DATA: str = "data"
_DATE_TIME: str = "datetime"  # CCXT only variable
_DELIVER_DATE: str = "deliverDate"
_DEPOSIT: str = "deposit"  # CCXT only variable
_DIV_TIME: str = "divTime"
_END_TIME: str = "endTime"
_EN_INFO: str = "enInfo"
_FEE: str = "fee"
_FIAT_CURRENCY: str = "fiatCurrency"
_ID: str = "id"  # CCXT only variable
_INDICATED_AMOUNT: str = "indicatedAmount"
_INFO: str = "info"
_INSERT_TIME: str = "insertTime"
_INTEREST_PARAMETER: str = "INTEREST"
_INTEREST_FIELD: str = "interest"
_IS_DUST: str = "isDust"
_IS_FIAT_PAYMENT: str = "isFiatPayment"
_LEGAL_MONEY: str = "legalMoney"
_LENDING_TYPE: str = "lendingType"
_LIMIT: str = "limit"
_LOCK_PERIOD: str = "lockPeriod"
_OBTAIN_AMOUNT: str = "obtainAmount"
_ORDER: str = "order"  # CCXT only variable
_ORDER_NO: str = "orderNo"
_PAGE_INDEX: str = "pageIndex"
_PAGE_SIZE: str = "pageSize"
_POSITION_ID: str = "positionId"
_PRICE: str = "price"
_PRODUCT: str = "product"
_PROFIT_AMOUNT: str = "profitAmount"
_REDEMPTION: str = "REDEMPTION"
_ROWS: str = "rows"
_SELL: str = "sell"  # CCXT only variable
_SIDE: str = "side"  # CCXT only variable
_SIZE: str = "size"
_STAKING: str = "STAKING"
_START_TIME: str = "startTime"
_STATUS: str = "status"
_SOURCE_AMOUNT: str = "sourceAmount"
_SUBSCRIPTION: str = "SUBSCRIPTION"
_SYMBOL: str = "symbol"
_TIME: str = "time"
_TIMESTAMP: str = "timestamp"  # CCXT only variable
_TRAN_ID: str = "tranId"
_TRANSACTION_TYPE: str = "transactionType"
_TOTAL: str = "total"
_TOTAL_FEE: str = "totalFee"
_TOTAL_NUM: str = "totalNum"
_TYPE: str = "type"
_TX_ID: str = "txid"  # CCXT doesn't capitalize I
_TXN_TYPE: str = "txnType"
_UPDATE_TIME: str = "updateTime"
_USERNAME: str = "userName"
_WITHDRAWAL: str = "withdrawal"  # CCXT only variable

# Time period constants
_NINETY_DAYS_IN_MS: int = 7776000000
_THIRTY_DAYS_IN_MS: int = 2592000000
_ONE_DAY_IN_MS: int = 86400000
_MS_IN_SECOND: int = 1000

# Record limits
_DEPOSIT_RECORD_LIMIT: int = 1000
_DIVIDEND_RECORD_LIMIT: int = 500
_DUST_TRADE_RECORD_LIMIT: int = 100
_INTEREST_SIZE_LIMIT: int = 100
_MINING_PAGE_LIMIT: int = 200
_TRADE_RECORD_LIMIT: int = 1000
_WITHDRAWAL_RECORD_LIMIT: int = 1000

# Types of Binance Dividends
_BNB_VAULT = "BNB Vault"
_ETH_STAKING = "ETH 2.0 Staking"
_FLEXIBLE_SAVINGS = "Flexible Savings"
_LAUNCH_POOL = "Launchpool"
_LOCKED_SAVINGS = "Locked Savings"
_LOCKED_STAKING = "Locked Staking"
_SOLO_AIRDROP = "SOLO airdrop"
_GENERAL_STAKING = "STAKING"

_AIRDROP_LIST = [_SOLO_AIRDROP]
_INTEREST_LIST = [_FLEXIBLE_SAVINGS, _LOCKED_SAVINGS]
_STAKING_LIST = [_ETH_STAKING, _LOCKED_STAKING, _BNB_VAULT, _LAUNCH_POOL, _GENERAL_STAKING]


class _ProcessAccountResult(NamedTuple):
    in_transactions: List[InTransaction]
    out_transactions: List[OutTransaction]
    intra_transactions: List[IntraTransaction]


class _Trade(NamedTuple):
    base_asset: str
    quote_asset: str
    base_info: str
    quote_info: str


class InputPlugin(AbstractInputPlugin):

    __BINANCE_COM: str = "Binance.com"

    def __init__(
        self,
        account_holder: str,
        api_key: str,
        api_secret: str,
        native_fiat: str,
        username: Optional[str] = None,
    ) -> None:

        super().__init__(account_holder, native_fiat)
        self.__logger: logging.Logger = create_logger(f"{self.__BINANCE_COM}/{self.account_holder}")
        self.__cache_key: str = f"{self.__BINANCE_COM.lower()}-{account_holder}"
        self.__client: binance = binance(
            {
                "apiKey": api_key,
                "enableRateLimit": True,
                "secret": api_secret,
            }
        )
        self.__username = username

        # We have to know what markets and algos are on Binance so that we can pull orders using the market
        self.__markets: List[str] = []
        self.__algos: List[str] = []

        # We will have a default start time of July 13th, 2017 since Binance Exchange officially launched on July 14th Beijing Time.
        self.__start_time: datetime = datetime(2017, 7, 13, 0, 0, 0, 0)
        self.__start_time_ms: int = int(self.__start_time.timestamp()) * _MS_IN_SECOND

    def cache_key(self) -> Optional[str]:
        return self.__cache_key

    def client(self) -> Optional[Exchange]:
        return self.__client

    @staticmethod
    def _rp2_timestamp_from_ms_epoch(epoch_timestamp: str) -> str:
        rp2_time = datetime.fromtimestamp((int(epoch_timestamp) / _MS_IN_SECOND), timezone.utc)

        return rp2_time.strftime("%Y-%m-%d %H:%M:%S%z")

    @staticmethod
    def _to_trade(market_pair: str, base_amount: str, quote_amount: str) -> _Trade:
        assets = market_pair.split("/")
        return _Trade(
            base_asset=assets[0],
            quote_asset=assets[1],
            base_info=f"{base_amount} {assets[0]}",
            quote_info=f"{quote_amount} {assets[1]}",
        )

    def load(self) -> List[AbstractTransaction]:
        result: List[AbstractTransaction] = []
        in_transactions: List[InTransaction] = []
        out_transactions: List[OutTransaction] = []
        intra_transactions: List[IntraTransaction] = []

        ccxt_markets: Any = self.__client.fetch_markets()
        for market in ccxt_markets:
            self.__logger.debug("Market: %s", json.dumps(market))
            self.__markets.append(market[_ID])

        if self.__username:
            binance_algos = self.__client.sapiGetMiningPubAlgoList()
            for algo in binance_algos[_DATA]:
                self.__logger.debug("Algo: %s", json.dumps(algo))
                self.__algos.append(algo[_ALGO_NAME])

        self._process_deposits(in_transactions, out_transactions, intra_transactions)
        self._process_gains(in_transactions, out_transactions)
        self._process_trades(in_transactions, out_transactions)
        self._process_withdrawals(out_transactions, intra_transactions)

        result.extend(in_transactions)
        result.extend(out_transactions)
        result.extend(intra_transactions)

        return result

    ### Multiple Transaction Processing

    def _process_deposits(
        self,
        in_transactions: List[InTransaction],
        out_transactions: List[OutTransaction],
        intra_transactions: List[IntraTransaction],
    ) -> None:

        # We need milliseconds for Binance
        current_start = self.__start_time_ms
        now_time = int(datetime.now().timestamp()) * _MS_IN_SECOND

        # Crypto Deposits can only be pulled in 90 day windows
        current_end = current_start + _NINETY_DAYS_IN_MS
        crypto_deposits = []

        # Crypto Bought with fiat. Technically this is a deposit of fiat that is used for a market order that fills immediately.
        # No limit on the date range
        # fiat payments takes the 'beginTime' param in contrast to other functions that take 'startTime'
        fiat_payments = self.__client.sapiGetFiatPayments(params=({_TRANSACTION_TYPE: 0, _BEGIN_TIME: self.__start_time_ms, _END_TIME: now_time}))
        # {
        #   "code": "000000",
        #   "message": "success",
        #   "data": [
        #   {
        #      "orderNo": "353fca443f06466db0c4dc89f94f027a",
        #      "sourceAmount": "20.0",  // Fiat trade amount
        #      "fiatCurrency": "EUR",   // Fiat token
        #      "obtainAmount": "4.462", // Crypto trade amount
        #      "cryptoCurrency": "LUNA",  // Crypto token
        #      "totalFee": "0.2",    // Trade fee
        #      "price": "4.437472",
        #      "status": "Failed",  // Processing, Completed, Failed, Refunded
        #      "createTime": 1624529919000,
        #      "updateTime": 1624529919000
        #   }
        #   ],
        #   "total": 1,
        #   "success": true
        # }
        if _DATA in fiat_payments:
            for payment in fiat_payments[_DATA]:
                self.__logger.debug("Payments: %s", json.dumps(payment))
                if payment[_STATUS] == "Completed":
                    payment[_IS_FIAT_PAYMENT] = True
                    self._process_buy(payment, in_transactions, out_transactions)

        # Process crypto deposits (limited to 90 day windows), fetches 1000 transactions
        while current_start < now_time:
            # The CCXT function only retrieves fiat deposits if you provide a valid 'legalMoney' code as variable.
            crypto_deposits = self.__client.fetch_deposits(params=({_START_TIME: current_start, _END_TIME: current_end}))

            # CCXT returns a standardized response from fetch_deposits. 'info' is the exchange-specific information
            # in this case from Binance.com

            # {
            #   'info': {
            #       'amount': '0.00999800',
            #       'coin': 'PAXG',
            #       'network': 'ETH',
            #       'status': '1',
            #       'address': '0x788cabe9236ce061e5a892e1a59395a81fc8d62c',
            #       'addressTag': '',
            #       'txId': '0xaad4654a3234aa6118af9b4b335f5ae81c360b2394721c019b5d1e75328b09f3',
            #       'insertTime': '1599621997000',
            #       'transferType': '0',
            #       'confirmTimes': '12/12',
            #       'unlockConfirm': '12/12',
            #       'walletType': '0'
            #   },
            #   'id': None,
            #   'txid': '0xaad4654a3234aa6118af9b4b335f5ae81c360b2394721c019b5d1e75328b09f3',
            #   'timestamp': 1599621997000,
            #   'datetime': '2020-09-09T03:26:37.000Z',
            #   'network': 'ETH',
            #   'address': '0x788cabe9236ce061e5a892e1a59395a81fc8d62c',
            #   'addressTo': '0x788cabe9236ce061e5a892e1a59395a81fc8d62c',
            #   'addressFrom': None,
            #   'tag': None,
            #   'tagTo': None,
            #   'tagFrom': None,
            #   'type': 'deposit',
            #   'amount': 0.00999800,
            #   'currency': 'PAXG',
            #   'status': 'ok',
            #   'updated': None,
            #   'internal': False,
            #   'fee': None
            # }

            for deposit in crypto_deposits:
                self.__logger.debug("Transfer: %s", json.dumps(deposit))
                self._process_transfer(deposit, intra_transactions)

            # If user made more than 1000 transactions in a 90 day period we need to shrink the window.
            if len(crypto_deposits) < _DEPOSIT_RECORD_LIMIT:
                current_start = current_end + 1
                current_end = current_start + _NINETY_DAYS_IN_MS
            else:
                # Binance sends latest record first ([0])
                # CCXT sorts by timestamp, so latest record is last ([999])
                current_start = int(crypto_deposits[_DEPOSIT_RECORD_LIMIT - 1][_TIMESTAMP]) + 1  # times are inclusive
                current_end = current_start + _NINETY_DAYS_IN_MS

        # Process actual fiat deposits (no limit on the date range)
        # Fiat deposits can also be pulled via CCXT fetch_deposits by cycling through legal_money
        # Using the underlying api endpoint is faster for Binance.
        # Note that this is the same endpoint as withdrawls, but with _TRANSACTION_TYPE set to 0 (for deposits)
        fiat_deposits = self.__client.sapiGetFiatOrders(params=({_TRANSACTION_TYPE: 0, _START_TIME: self.__start_time_ms, _END_TIME: now_time}))
        #    {
        #      "code": "000000",
        #      "message": "success",
        #      "data": [
        #        {
        #          "orderNo": "25ced37075c1470ba8939d0df2316e23",
        #          "fiatCurrency": "EUR",
        #          "indicatedAmount": "15.00",
        #          "amount": "15.00",
        #          "totalFee": "0.00",
        #          "method": "card",
        #          "status": "Failed",
        #          "createTime": 1627501026000,
        #          "updateTime": 1627501027000
        #        }
        #      ],
        #      "total": 1,
        #      "success": True
        #    }
        if _DATA in fiat_deposits:
            for deposit in fiat_deposits[_DATA]:
                self.__logger.debug("Deposit: %s", json.dumps(deposit))
                if deposit[_STATUS] == "Completed":
                    self._process_deposit(deposit, in_transactions)

    def _process_gains(self, in_transactions: List[InTransaction], out_transactions: List[OutTransaction]) -> None:

        ### Regular Dividends from Staking (including Eth staking) and Savings (Lending) after around May 8th, 2021 01:00 UTC.

        # We need milliseconds for Binance
        current_start = self.__start_time_ms
        now_time = int(datetime.now().timestamp()) * _MS_IN_SECOND

        # The exact moment when Binance switched to unified dividends is unknown/unpublished.
        # This allows us an educated guess.
        earliest_record_epoch: int = 0

        # We will pull in 30 day periods. This allows for 16 assets with daily dividends.
        current_end = current_start + _THIRTY_DAYS_IN_MS

        while current_start < now_time:
            self.__logger.debug("Pulling dividends/subscriptions/redemptions from %s to %s", current_start, current_end)

            # CCXT doesn't have a standard way to pull income, we must use the underlying API endpoint
            dividends = self.__client.sapiGetAssetAssetDividend(params=({_START_TIME: current_start, _END_TIME: current_end, _LIMIT: _DIVIDEND_RECORD_LIMIT}))
            # {
            #     "rows":[
            #         {
            #             "id":1637366104,
            #             "amount":"10.00000000",
            #             "asset":"BHFT",
            #             "divTime":1563189166000,
            #             "enInfo":"BHFT distribution",
            #             "tranId":2968885920
            #         },
            #         {
            #             "id":1631750237,
            #             "amount":"10.00000000",
            #             "asset":"BHFT",
            #             "divTime":1563189165000,
            #             "enInfo":"BHFT distribution",
            #             "tranId":2968885920
            #         }
            #     ],
            #     "total":2
            # }
            for dividend in dividends[_ROWS]:
                self.__logger.debug("Dividend: %s", json.dumps(dividend))
                if dividend[_EN_INFO] in _STAKING_LIST or re.search("[dD]istribution", dividend[_EN_INFO]) or re.search("staking", dividend[_EN_INFO]):
                    self._process_gain(dividend, Keyword.STAKING, in_transactions)
                elif dividend[_EN_INFO] in _INTEREST_LIST:
                    self._process_gain(dividend, Keyword.INTEREST, in_transactions)
                elif dividend[_EN_INFO] in _AIRDROP_LIST or re.search("[aA]irdrop", dividend[_EN_INFO]):
                    self._process_gain(dividend, Keyword.AIRDROP, in_transactions)
                else:
                    self.__logger.error("WARNING: Unrecognized Dividend: %s. Please open an issue at %s", dividend[_EN_INFO], self.ISSUES_URL)

            # If user received more than 500 dividends in a 30 day period we need to shrink the window.
            if int(dividends[_TOTAL]) < _DIVIDEND_RECORD_LIMIT:
                current_start = current_end + 1
                current_end = current_start + _THIRTY_DAYS_IN_MS
            else:
                # Using implicit API so we need to follow Binance order, which sends latest record first ([0])
                # CCXT standard API sorts by timestamp, so latest record is last ([499])
                current_start = int(dividends[_ROWS][0][_DIV_TIME]) + 1  # times are inclusive
                current_end = current_start + _THIRTY_DAYS_IN_MS

            if not earliest_record_epoch and int(dividends[_TOTAL]) > 0:
                earliest_record_epoch = int(dividends[_ROWS][-1][_DIV_TIME]) - 1

            # We need to track subscription and redemption amounts since Binance will take a fee equal to the amount of interest
            # earned during the lock period if the user prematurely redems their funds.

        # Old system Locked Savings

        old_savings: bool = False

        # Reset window
        current_start = self.__start_time_ms
        current_end = current_start + _THIRTY_DAYS_IN_MS

        # The cummulative interest from a positionID
        total_current_interest: Dict[int, RP2Decimal] = {}

        # The cummulative interest payments made to each positionID
        total_current_payments: Dict[int, int] = {}

        # Subscriptions organized [asset][amount] = timestamp in milliseconds
        current_subscriptions: Dict[str, Dict[str, Dict[str, str]]] = {}

        # We will step backward in time from the switch over
        while current_start < now_time:

            self.__logger.debug("Pulling locked staking from older api system from %s to %s", current_start, current_end)

            locked_staking = self.__client.sapi_get_staking_stakingrecord(
                params=({_START_TIME: current_start, _END_TIME: current_end, _PRODUCT: _STAKING, _TXN_TYPE: _INTEREST_PARAMETER, _SIZE: _INTEREST_SIZE_LIMIT})
            )
            # [
            # 	{
            # 		'positionId': '7146912',
            # 		'time': '1624233772000',
            # 		'asset': 'BTC',
            # 		'amount': '0.017666',
            # 		'status': 'SUCCESS'
            # 	},
            # 	{
            # 		'positionId': '7147052',
            # 		'time': '1624147893000',
            # 		'asset': 'BTC',
            # 		'amount': '0.0176665',
            # 		'status': 'SUCCESS'
            # 	}
            # ]
            # NOTE: All values are str
            for stake_dividend in locked_staking:
                if int(stake_dividend[_TIME]) < earliest_record_epoch:
                    self.__logger.debug("Locked Staking (OLD): %s", json.dumps(stake_dividend))
                    stake_dividend[_EN_INFO] = "Locked Staking/Savings (OLD)"
                    stake_dividend[_ID] = Keyword.UNKNOWN.value
                    stake_dividend[_DIV_TIME] = stake_dividend[_TIME]
                    self._process_gain(stake_dividend, Keyword.STAKING, in_transactions)
                    old_savings = True

                # Early redemption penalty tracking. Needs to be recorded even for new system.
                position_id: int = stake_dividend[_POSITION_ID]
                total_current_interest[position_id] = total_current_interest.get(position_id, ZERO) + RP2Decimal(str(stake_dividend[_AMOUNT]))
                total_current_payments[position_id] = total_current_payments.get(position_id, 0) + 1

            locked_subscriptions = self.__client.sapi_get_staking_stakingrecord(
                params=({_START_TIME: current_start, _END_TIME: current_end, _PRODUCT: _STAKING, _TXN_TYPE: _SUBSCRIPTION, _SIZE: _INTEREST_SIZE_LIMIT})
            )
            # [
            #     {
            #         "time": "1624147893000",
            #         "asset": "BTC",
            #         "amount": "1",
            #         "lockPeriod": "10",
            #         "type": "NORMAL",
            #         "status": "SUCCESS",
            #     },
            #     {
            #         "time": "1624147893000",
            #         "asset": "BTC",
            #         "amount": "1",
            #         "lockPeriod": "10",
            #         "type": "NORMAL",
            #         "status": "SUCCESS",
            #     }
            # ]
            # NOTE: all values are str

            for subscription in locked_subscriptions:

                # If the dict already exists add another key, if not add new dict
                if current_subscriptions.get(subscription[_ASSET]):
                    current_subscriptions[subscription[_ASSET]][f"{RP2Decimal(subscription[_AMOUNT]):.13f}"] = subscription
                else:
                    current_subscriptions[subscription[_ASSET]] = {f"{RP2Decimal(subscription[_AMOUNT]):.13f}": subscription}

            locked_redemptions = self.__client.sapi_get_staking_stakingrecord(
                params=({_START_TIME: current_start, _END_TIME: current_end, _PRODUCT: _STAKING, _TXN_TYPE: _REDEMPTION, _SIZE: _INTEREST_SIZE_LIMIT})
            )
            # [
            #         {
            #             "positionId": "12345",
            #             "time": "1624147893000"
            #             "asset": "BTC",
            #             "amount": "1",
            #             "deliverDate": "1624147895000"
            #             "status": "PAID",
            #         },
            #         {
            #             "positionId": "12346",
            #             "time": "1624147993000"
            #             "asset": "BTC",
            #             "amount": "0.95",
            #             "deliverDate": "1624148093000"
            #             "status": "PAID",
            #         }
            # ]
            # NOTE: all values are str

            for redemption in locked_redemptions:

                redemption_amount: str = f"{RP2Decimal(redemption[_AMOUNT]):.13f}"

                # Check if there is a subscription with this asset and if the redemption amount is equal to the subscription amount
                if redemption[_ASSET] in current_subscriptions and redemption_amount not in current_subscriptions[redemption[_ASSET]]:

                    # If they do not equal we need to calculate what the amended principal should be based on total interest paid to that productId
                    total_interest_earned: RP2Decimal = total_current_interest[redemption[_POSITION_ID]]
                    original_principal: str = f"{(RP2Decimal(redemption[_AMOUNT]) + RP2Decimal(str(total_interest_earned))):.13f}"
                    earliest_redemption_timestamp: int = 0

                    if str(original_principal) in current_subscriptions[redemption[_ASSET]]:

                        subscription_time: int = int(current_subscriptions[redemption[_ASSET]][str(original_principal)][_TIME])
                        lockperiod_in_ms: int = int(current_subscriptions[redemption[_ASSET]][str(original_principal)][_LOCK_PERIOD]) * _ONE_DAY_IN_MS
                        earliest_redemption_timestamp = subscription_time + lockperiod_in_ms

                    else:
                        raise Exception(
                            f"Internal Error: Principal ({original_principal}) minus paid interest ({RP2Decimal(str(total_interest_earned))}) does not equal"
                            f" returned principal ({RP2Decimal(redemption[_AMOUNT])}) on locked savings position ID - {redemption[_POSITION_ID]}."
                        )

                    # There is some lag time between application for the subscription and when the subscription actually starts ~ 2 days
                    if (int(redemption[_TIME]) - int(earliest_redemption_timestamp)) < 2 * _ONE_DAY_IN_MS:
                        out_transactions.append(
                            OutTransaction(
                                plugin=self.__BINANCE_COM,
                                unique_id=Keyword.UNKNOWN.value,
                                raw_data=json.dumps(redemption),
                                timestamp=self._rp2_timestamp_from_ms_epoch(redemption[_DELIVER_DATE]),
                                asset=redemption[_ASSET],
                                exchange=self.__BINANCE_COM,
                                holder=self.account_holder,
                                transaction_type=Keyword.FEE.value,
                                spot_price=Keyword.UNKNOWN.value,
                                crypto_out_no_fee="0",
                                crypto_fee=str(total_interest_earned),
                                crypto_out_with_fee=str(total_interest_earned),
                                fiat_out_no_fee=None,
                                fiat_fee=None,
                                notes=(f"Penalty Fee for {redemption[_POSITION_ID]}"),
                            )
                        )

                    else:
                        raise Exception(
                            f"Internal Error: The redemption time ({self._rp2_timestamp_from_ms_epoch(redemption[_TIME])}) is not in the redemption window "
                            f"({self._rp2_timestamp_from_ms_epoch(str(earliest_redemption_timestamp))} + 2 days)."
                        )

                elif redemption[_ASSET] in current_subscriptions and redemption_amount in current_subscriptions[redemption[_ASSET]]:

                    self.__logger.debug("Locked Savings positionId %s redeemed successfully.", redemption[_POSITION_ID])

                else:
                    raise Exception(f"Internal Error: Orphaned Redemption. Please open an issue at {self.ISSUES_URL}.")

            # if we returned the limit, we need to roll the window forward to the last time
            if len(locked_redemptions) < _INTEREST_SIZE_LIMIT:
                current_start = current_end + 1
                current_end = current_start + _THIRTY_DAYS_IN_MS
            else:
                current_start = now_time - 1  # int(locked_redemptions[0][_TIME]) + 1
                current_end = now_time  # current_start + _THIRTY_DAYS_IN_MS

        # Old system Flexible Savings

        # Reset window
        current_start = self.__start_time_ms
        current_end = current_start + _THIRTY_DAYS_IN_MS

        # We will step backward in time from the switch over
        while current_start < earliest_record_epoch:

            self.__logger.debug("Pulling flexible saving from older api system from %s to %s", current_start, current_end)

            flexible_saving = self.__client.sapi_get_lending_union_interesthistory(
                params=({_START_TIME: current_start, _END_TIME: current_end, _LENDING_TYPE: _DAILY, _SIZE: _INTEREST_SIZE_LIMIT})
            )
            # [
            #     {
            #         "asset": "BUSD",
            #         "interest": "0.00006408",
            #         "lendingType": "DAILY",
            #         "productName": "BUSD",
            #         "time": 1577233578000
            #     },
            #     {
            #         "asset": "USDT",
            #         "interest": "0.00687654",
            #         "lendingType": "DAILY",
            #         "productName": "USDT",
            #         "time": 1577233562000
            #     }
            # ]
            for saving in flexible_saving:
                self.__logger.debug("Flexible Saving: %s", json.dumps(saving))
                saving[_EN_INFO] = "Flexible Savings (OLD)"
                saving[_ID] = Keyword.UNKNOWN.value
                saving[_DIV_TIME] = saving[_TIME]
                saving[_AMOUNT] = saving[_INTEREST_FIELD]
                self._process_gain(saving, Keyword.INTEREST, in_transactions)
                old_savings = True

            # if we returned the limit, we need to roll the window forward to the last time
            if len(flexible_saving) < _INTEREST_SIZE_LIMIT:
                current_start = current_end + 1
                current_end = current_start + _THIRTY_DAYS_IN_MS
            else:
                current_start = int(flexible_saving[0][_TIME]) + 1
                current_end = current_start + _THIRTY_DAYS_IN_MS

            current_end = min(current_end, earliest_record_epoch)

        if old_savings:
            # Since we are making a guess at the cut off, there might be errors.
            self.__logger.warning(
                "Pre-May 8th, 2021 savings detected. Please be aware that there may be duplicate or missing savings records around May 8th, 2021."
            )

        ### Mining Income

        # username is only required when pulling mining data
        for algo in self.__algos:
            # Binance uses pages for mining payments
            current_page = 1
            while True:
                results = self.__client.sapiGetMiningPaymentList(
                    params=({_ALGO: algo, _USERNAME: self.__username, _PAGE_INDEX: current_page, _PAGE_SIZE: _MINING_PAGE_LIMIT})
                )
                # {
                #   "code": 0,
                #   "msg": "",
                #   "data": {
                #     "accountProfits": [
                #       {
                #         "time": 1586188800000,            // Mining date
                #         "type": "31", // 0:Mining Wallet,5:Mining Address,7:Pool Savings,
                #           8:Transferred,31:Income Transfer ,32:Hashrate Resale-Mining Wallet 33:Hashrate Resale-Pool Savings
                #         "hashTransfer": null,            // Transferred Hashrate
                #         "transferAmount": null,          // Transferred Income
                #         "dayHashRate": 129129903378244,  // Daily Hashrate
                #         "profitAmount": 8.6083060304,   //Earnings Amount
                #         "coinName":"BTC",              // Coin Type
                #         "status": "2"    //Status：0:Unpaid， 1:Paying  2：Paid
                #       },
                #       {
                #         "time": 1607529600000,
                #         "coinName": "BTC",
                #         "type": "0", // String
                #         "dayHashRate": 9942053925926,
                #         "profitAmount": 0.85426469,
                #         "hashTransfer": 200000000000,
                #         "transferAmount": 0.02180958,
                #         "status": "2"
                #       },
                #       {
                #         "time": 1607443200000,
                #         "coinName": "BTC",
                #         "type": "31",
                #         "dayHashRate": 200000000000,
                #         "profitAmount": 0.02905916,
                #         "hashTransfer": null,
                #         "transferAmount": null,
                #         "status": "2"
                #       }
                #     ],
                #     "totalNum": 3,          // Total Rows
                #     "pageSize": 20          // Rows per page
                #   }
                # }

                if results[_DATA][_TOTAL_NUM] != "0":
                    profits: List[Dict[str, Union[int, str]]] = results[_DATA][_ACCOUNT_PROFITS]
                    for result in profits:
                        self.__logger.debug("Mining profit: %s", json.dumps(result))

                        # Currently the plugin only supports standard mining deposits
                        # Payment must also be made (status=2) in order to be counted
                        if result[_TYPE] == "0" and result[_STATUS] == "2":
                            self._process_gain(result, Keyword.MINING, in_transactions)
                        else:
                            self.__logger.error(
                                "WARNING: Unsupported Mining Transaction Type: %s.\nFull Details: %s\nPlease open an issue at %s.",
                                result[_TYPE],
                                json.dumps(result),
                                self.ISSUES_URL,
                            )

                    if len(profits) == _MINING_PAGE_LIMIT:
                        current_page += 1
                    else:
                        break
                else:
                    break

    def _process_trades(self, in_transactions: List[InTransaction], out_transactions: List[OutTransaction]) -> None:

        ### Regular Trades

        # Binance requires a symbol/market
        # max limit is 1000
        for market in self.__markets:
            since: int = self.__start_time_ms
            while True:
                try:
                    market_trades = self.__client.fetch_my_trades(symbol=market, since=since, limit=_TRADE_RECORD_LIMIT)
                    #   {
                    #       'info':         { ... },                    // the original decoded JSON as is
                    #       'id':           '12345-67890:09876/54321',  // string trade id
                    #       'timestamp':    1502962946216,              // Unix timestamp in milliseconds
                    #       'datetime':     '2017-08-17 12:42:48.000',  // ISO8601 datetime with milliseconds
                    #       'symbol':       'ETH/BTC',                  // symbol
                    #       'order':        '12345-67890:09876/54321',  // string order id or undefined/None/null
                    #       'type':         'limit',                    // order type, 'market', 'limit' or undefined/None/null
                    #       'side':         'buy',                      // direction of the trade, 'buy' or 'sell'
                    #       'takerOrMaker': 'taker',                    // string, 'taker' or 'maker'
                    #       'price':        0.06917684,                 // float price in quote currency
                    #       'amount':       1.5,                        // amount of base currency
                    #       'cost':         0.10376526,                 // total cost, `price * amount`,
                    #       'fee':          {                           // provided by exchange or calculated by ccxt
                    #           'cost':  0.0015,                        // float
                    #           'currency': 'ETH',                      // usually base currency for buys, quote currency for sells
                    #           'rate': 0.002,                          // the fee rate (if available)
                    #       },
                    #   }

                    # * The work on ``'fee'`` info is still in progress, fee info may be missing partially or entirely, depending on the exchange capabilities.
                    # * The ``fee`` currency may be different from both traded currencies (for example, an ETH/BTC order with fees in USD).
                    # * The ``cost`` of the trade means ``amount * price``. It is the total *quote* volume of the trade (whereas `amount` is the *base* volume).
                    # * The cost field itself is there mostly for convenience and can be deduced from other fields.
                    # * The ``cost`` of the trade is a *"gross"* value. That is the value pre-fee, and the fee has to be applied afterwards.
                    for trade in market_trades:
                        self.__logger.debug("Trade: %s", json.dumps(trade))
                        self._process_sell(trade, out_transactions)
                        self._process_buy(trade, in_transactions, out_transactions)
                    if len(market_trades) < _TRADE_RECORD_LIMIT:
                        break
                    # Times are inclusive
                    since = int(market_trades[_TRADE_RECORD_LIMIT - 1][_TIMESTAMP]) + 1
                except (DDoSProtection, InvalidNonce):
                    # DDosProtection - too many requests in time window
                    # InvalidNonce - server is taking too long to process a request
                    sleep(0.2)
                    self.__logger.debug("Too many requests or server overloaded. Waiting 0.2 seconds")

        ### Dust Trades

        # We need milliseconds for Binance
        current_start = self.__start_time_ms
        now_time = int(datetime.now().timestamp()) * _MS_IN_SECOND

        # We will pull in 30 day periods
        # If the user has more than 100 dust trades in a 30 day period this will break.
        # Maybe we can set a smaller window in the .ini file?
        current_end = current_start + _THIRTY_DAYS_IN_MS
        while current_start < now_time:
            dust_trades = self.__client.fetch_my_dust_trades(params=({_START_TIME: current_start, _END_TIME: current_end}))
            # CCXT returns the same json as .fetch_trades()

            # Binance only returns 100 dust trades per call. If we hit the limit we will have to crawl
            # over each 'dribblet'. Each dribblet can have multiple assets converted into BNB at the same time.
            # If the user converts more than 100 assets at one time, we can not retrieve accurate records.
            if len(dust_trades) == _DUST_TRADE_RECORD_LIMIT:
                current_dribblet: Any = []
                current_dribblet_time: int = int(dust_trades[0][_DIV_TIME])
                for dust in dust_trades:
                    self.__logger.debug("Dust: %s", json.dumps(dust))
                    dust[_ID] = dust[_ORDER]
                    if dust[_DIV_TIME] == current_dribblet_time:
                        current_dribblet.append(dust)
                    elif len(current_dribblet) < (_DUST_TRADE_RECORD_LIMIT + 1):
                        for dribblet_piece in current_dribblet:
                            self._process_sell(dribblet_piece, out_transactions)
                            self._process_buy(dribblet_piece, in_transactions, out_transactions)

                        # Shift the call window forward past this dribblet
                        current_start = current_dribblet_time + 1
                        current_end = current_start + _THIRTY_DAYS_IN_MS
                        break
                    else:
                        raise Exception(
                            f"Internal error: too many assets dusted at the same time: " f"{self._rp2_timestamp_from_ms_epoch(str(current_dribblet_time))}"
                        )
            else:

                for dust in dust_trades:
                    self.__logger.debug("Dust: %s", json.dumps(dust))
                    # dust trades have a null id, and if multiple assets are dusted at the same time, all are assigned same ID
                    dust_trade: _Trade = self._to_trade(dust[_SYMBOL], str(dust[_AMOUNT]), str(dust[_COST]))
                    dust[_ID] = f"{dust[_ORDER]}{dust_trade.base_asset}"
                    self._process_sell(dust, out_transactions)
                    self._process_buy(dust, in_transactions, out_transactions)

                current_start = current_end + 1
                current_end = current_start + _THIRTY_DAYS_IN_MS

    def _process_withdrawals(self, out_transactions: List[OutTransaction], intra_transactions: List[IntraTransaction]) -> None:

        # We need milliseconds for Binance
        current_start = self.__start_time_ms
        now_time = int(datetime.now().timestamp()) * _MS_IN_SECOND

        # Crypto Withdrawls can only be pulled in 90 day windows
        current_end = current_start + _NINETY_DAYS_IN_MS
        crypto_withdrawals: Any = []

        # Process crypto withdrawls (limited to 90 day windows), fetches 1000 transactions
        while current_start < now_time:
            # The CCXT function only retrieves fiat deposits if you provide a valid 'legalMoney' code as variable.
            crypto_withdrawals = self.__client.fetch_withdrawals(params=({_START_TIME: current_start, _END_TIME: current_end}))

            # CCXT returns a standardized response from fetch_withdrawls. 'info' is the exchange-specific information
            # in this case from Binance.com

            # {
            #   'info': {
            #       'amount': '0.00999800',
            #       'coin': 'PAXG',
            #       'network': 'ETH',
            #       'status': '1',
            #       'address': '0x788cabe9236ce061e5a892e1a59395a81fc8d62c',
            #       'addressTag': '',
            #       'txId': '0xaad4654a3234aa6118af9b4b335f5ae81c360b2394721c019b5d1e75328b09f3',
            #       'insertTime': '1599621997000',
            #       'transferType': '0',
            #       'confirmTimes': '12/12',
            #       'unlockConfirm': '12/12',
            #       'walletType': '0'
            #   },
            #   'id': None,
            #   'txid': '0xaad4654a3234aa6118af9b4b335f5ae81c360b2394721c019b5d1e75328b09f3',
            #   'timestamp': 1599621997000,
            #   'datetime': '2020-09-09T03:26:37.000Z',
            #   'network': 'ETH',
            #   'address': '0x788cabe9236ce061e5a892e1a59395a81fc8d62c',
            #   'addressTo': '0x788cabe9236ce061e5a892e1a59395a81fc8d62c',
            #   'addressFrom': None,
            #   'tag': None,
            #   'tagTo': None,
            #   'tagFrom': None,
            #   'type': 'withdrawal',
            #   'amount': 0.00999800,
            #   'currency': 'PAXG',
            #   'status': 'ok',
            #   'updated': None,
            #   'internal': False,
            #   'fee': None
            # }

            for withdrawal in crypto_withdrawals:
                self.__logger.debug("Transfer: %s", json.dumps(withdrawal))
                self._process_transfer(withdrawal, intra_transactions)

            # If user made more than 1000 transactions in a 90 day period we need to shrink the window.
            if len(crypto_withdrawals) < _WITHDRAWAL_RECORD_LIMIT:
                current_start = current_end + 1
                current_end = current_start + _NINETY_DAYS_IN_MS
            else:
                # Binance sends latest record first ([0])
                # CCXT sorts by timestamp, so latest record is last ([999])
                current_start = int(crypto_withdrawals[_WITHDRAWAL_RECORD_LIMIT - 1][_TIMESTAMP]) + 1  # times are inclusive
                current_end = current_start + _NINETY_DAYS_IN_MS

        # Process actual fiat withdrawls (no limit on the date range)
        # Fiat deposits can also be pulled via CCXT fetch_withdrawls by cycling through legal_money
        # Using the underlying api endpoint is faster for Binance.
        # Note that this is the same endpoint as deposits, but with _TRANSACTION_TYPE set to 1 (for withdrawls)
        fiat_withdrawals = self.__client.sapiGetFiatOrders(params=({_TRANSACTION_TYPE: 1, _START_TIME: self.__start_time_ms, _END_TIME: now_time}))
        #    {
        #      "code": "000000",
        #      "message": "success",
        #      "data": [
        #        {
        #          "orderNo": "25ced37075c1470ba8939d0df2316e23",
        #          "fiatCurrency": "EUR",
        #          "indicatedAmount": "15.00",
        #          "amount": "15.00",
        #          "totalFee": "0.00",
        #          "method": "card",
        #          "status": "Failed",
        #          "createTime": 1627501026000,
        #          "updateTime": 1627501027000
        #        }
        #      ],
        #      "total": 1,
        #      "success": True
        #    }
        if _DATA in fiat_withdrawals:
            for withdrawal in fiat_withdrawals[_DATA]:
                self.__logger.debug("Withdrawal: %s", json.dumps(withdrawal))
                if withdrawal[_STATUS] == "Completed":
                    self._process_withdrawal(withdrawal, out_transactions)

    ### Single Transaction Processing

    def _process_buy(
        self, transaction: Any, in_transaction_list: List[InTransaction], out_transaction_list: List[OutTransaction], notes: Optional[str] = None
    ) -> None:
        crypto_in: RP2Decimal
        crypto_fee: RP2Decimal

        if _IS_FIAT_PAYMENT in transaction:
            in_transaction_list.append(
                InTransaction(
                    plugin=self.__BINANCE_COM,
                    unique_id=transaction[_ORDER_NO],
                    raw_data=json.dumps(transaction),
                    timestamp=self._rp2_timestamp_from_ms_epoch(transaction[_CREATE_TIME]),
                    asset=transaction[_CRYPTOCURRENCY],
                    exchange=self.__BINANCE_COM,
                    holder=self.account_holder,
                    transaction_type=Keyword.BUY.value,
                    spot_price=str(RP2Decimal(transaction[_PRICE])),
                    crypto_in=transaction[_OBTAIN_AMOUNT],
                    crypto_fee=None,
                    fiat_in_no_fee=str(RP2Decimal(transaction[_SOURCE_AMOUNT]) - RP2Decimal(transaction[_TOTAL_FEE])),
                    fiat_in_with_fee=str(transaction[_SOURCE_AMOUNT]),
                    fiat_fee=str(RP2Decimal(transaction[_TOTAL_FEE])),
                    fiat_ticker=transaction[_FIAT_CURRENCY],
                    notes=(f"Buy transaction for fiat payment orderNo - " f"{transaction[_ORDER_NO]}"),
                )
            )

        else:
            trade: _Trade = self._to_trade(transaction[_SYMBOL], str(transaction[_AMOUNT]), str(transaction[_COST]))
            if transaction[_SIDE] == _BUY:
                out_asset = trade.quote_asset
                in_asset = trade.base_asset
                crypto_in = RP2Decimal(str(transaction[_AMOUNT]))
                conversion_info = f"{trade.quote_info} -> {trade.base_info}"
            elif transaction[_SIDE] == _SELL:
                out_asset = trade.base_asset
                in_asset = trade.quote_asset
                crypto_in = RP2Decimal(str(transaction[_COST]))
                conversion_info = f"{trade.base_info} -> {trade.quote_info}"
            else:
                raise Exception(f"Internal error: unrecognized transaction side: {transaction[_SIDE]}")

            if transaction[_FEE][_CURRENCY] == in_asset:
                crypto_fee = RP2Decimal(str(transaction[_FEE][_COST]))
            else:
                crypto_fee = ZERO

                transaction_fee = transaction[_FEE][_COST]

                # Users can use BNB to pay fees on Binance
                if transaction[_FEE][_CURRENCY] != out_asset and float(transaction_fee) > 0:
                    out_transaction_list.append(
                        OutTransaction(
                            plugin=self.__BINANCE_COM,
                            unique_id=transaction[_ID],
                            raw_data=json.dumps(transaction),
                            timestamp=self._rp2_timestamp_from_ms_epoch(transaction[_TIMESTAMP]),
                            asset=transaction[_FEE][_CURRENCY],
                            exchange=self.__BINANCE_COM,
                            holder=self.account_holder,
                            transaction_type=Keyword.FEE.value,
                            spot_price=Keyword.UNKNOWN.value,
                            crypto_out_no_fee="0",
                            crypto_fee=str(transaction_fee),
                            crypto_out_with_fee=str(transaction_fee),
                            fiat_out_no_fee=None,
                            fiat_fee=None,
                            notes=(f"{notes + '; ' if notes else ''} Fee for conversion from " f"{conversion_info}"),
                        )
                    )

            # Is this a plain buy or a conversion?
            if trade.quote_asset in self.__client.options[_LEGAL_MONEY]:  # Is this fiat? (options[_LEGAL_MONEY] is a list of all fiat traded on Binance.com)
                fiat_in_with_fee = RP2Decimal(str(transaction[_COST]))
                fiat_fee = RP2Decimal(crypto_fee)
                spot_price = RP2Decimal(str(transaction[_PRICE]))
                if transaction[_SIDE] == _BUY:
                    transaction_notes = f"Fiat buy of {trade.base_asset} with {trade.quote_asset}"
                    fiat_in_no_fee = fiat_in_with_fee - (fiat_fee * spot_price)
                elif transaction[_SIDE] == _SELL:
                    transaction_notes = f"Fiat sell of {trade.base_asset} into {trade.quote_asset}"
                    fiat_in_no_fee = fiat_in_with_fee - fiat_fee

                in_transaction_list.append(
                    InTransaction(
                        plugin=self.__BINANCE_COM,
                        unique_id=transaction[_ID],
                        raw_data=json.dumps(transaction),
                        timestamp=self._rp2_timestamp_from_ms_epoch(transaction[_TIMESTAMP]),
                        asset=in_asset,
                        exchange=self.__BINANCE_COM,
                        holder=self.account_holder,
                        transaction_type=Keyword.BUY.value,
                        spot_price=str(spot_price),
                        crypto_in=str(crypto_in),
                        crypto_fee=str(crypto_fee),
                        fiat_in_no_fee=str(fiat_in_no_fee),
                        fiat_in_with_fee=str(fiat_in_with_fee),
                        fiat_fee=None,
                        fiat_ticker=trade.quote_asset,
                        notes=(f"{notes + '; ' if notes else ''} {transaction_notes}"),
                    )
                )

            else:
                transaction_notes = f"Buy side of conversion from " f"{conversion_info}" f"({out_asset} out-transaction unique id: {transaction[_ID]}"

                in_transaction_list.append(
                    InTransaction(
                        plugin=self.__BINANCE_COM,
                        unique_id=transaction[_ID],
                        raw_data=json.dumps(transaction),
                        timestamp=self._rp2_timestamp_from_ms_epoch(transaction[_TIMESTAMP]),
                        asset=in_asset,
                        exchange=self.__BINANCE_COM,
                        holder=self.account_holder,
                        transaction_type=Keyword.BUY.value,
                        spot_price=Keyword.UNKNOWN.value,
                        crypto_in=str(crypto_in),
                        crypto_fee=str(crypto_fee),
                        fiat_in_no_fee=None,
                        fiat_in_with_fee=None,
                        fiat_fee=None,
                        notes=(f"{notes + '; ' if notes else ''} {transaction_notes}"),
                    )
                )

    def _process_deposit(self, transaction: Any, in_transaction_list: List[InTransaction], notes: Optional[str] = None) -> None:

        amount: RP2Decimal = RP2Decimal(transaction[_INDICATED_AMOUNT])
        fee: RP2Decimal = RP2Decimal(transaction[_TOTAL_FEE])
        notes = f"{notes + '; ' if notes else ''}{'Fiat Deposit of '}; {transaction[_FIAT_CURRENCY]}"
        in_transaction_list.append(
            InTransaction(
                plugin=self.__BINANCE_COM,
                unique_id=transaction[_ORDER_NO],
                raw_data=json.dumps(transaction),
                timestamp=self._rp2_timestamp_from_ms_epoch(transaction[_CREATE_TIME]),
                asset=transaction[_FIAT_CURRENCY],
                exchange=self.__BINANCE_COM,
                holder=self.account_holder,
                transaction_type=Keyword.BUY.value,
                spot_price="1",
                crypto_in=str(amount),
                crypto_fee=str(fee),
                fiat_in_no_fee=None,
                fiat_in_with_fee=None,
                fiat_fee=None,
                fiat_ticker=transaction[_FIAT_CURRENCY],
                notes=notes,
            )
        )

    def _process_gain(self, transaction: Any, transaction_type: Keyword, in_transaction_list: List[InTransaction], notes: Optional[str] = None) -> None:

        if transaction_type == Keyword.MINING:
            amount: RP2Decimal = RP2Decimal(str(transaction[_PROFIT_AMOUNT]))
            notes = f"{notes + '; ' if notes else ''}'Mining profit'"
            in_transaction_list.append(
                InTransaction(
                    plugin=self.__BINANCE_COM,
                    unique_id=Keyword.UNKNOWN.value,
                    raw_data=json.dumps(transaction),
                    timestamp=self._rp2_timestamp_from_ms_epoch(transaction[_TIME]),
                    asset=transaction[_COIN_NAME],
                    exchange=self.__BINANCE_COM,
                    holder=self.account_holder,
                    transaction_type=transaction_type.value,
                    spot_price=Keyword.UNKNOWN.value,
                    crypto_in=str(amount),
                    crypto_fee=None,
                    fiat_in_no_fee=None,
                    fiat_in_with_fee=None,
                    fiat_fee=None,
                    notes=notes,
                )
            )
        else:
            amount = RP2Decimal(transaction[_AMOUNT])
            notes = f"{notes + '; ' if notes else ''}{transaction[_EN_INFO]}"

            in_transaction_list.append(
                InTransaction(
                    plugin=self.__BINANCE_COM,
                    unique_id=str(transaction[_ID]),  # Binance sometimes has two ids for one tranid
                    raw_data=json.dumps(transaction),
                    timestamp=self._rp2_timestamp_from_ms_epoch(transaction[_DIV_TIME]),
                    asset=transaction[_ASSET],
                    exchange=self.__BINANCE_COM,
                    holder=self.account_holder,
                    transaction_type=transaction_type.value,
                    spot_price=Keyword.UNKNOWN.value,
                    crypto_in=str(amount),
                    crypto_fee=None,
                    fiat_in_no_fee=None,
                    fiat_in_with_fee=None,
                    fiat_fee=None,
                    notes=notes,
                )
            )

    def _process_sell(self, transaction: Any, out_transaction_list: List[OutTransaction], notes: Optional[str] = None) -> None:
        trade: _Trade = self._to_trade(transaction[_SYMBOL], str(transaction[_AMOUNT]), str(transaction[_COST]))

        # For some reason CCXT outputs amounts in float
        if transaction[_SIDE] == _BUY:
            out_asset = trade.quote_asset
            in_asset = trade.base_asset
            crypto_out_no_fee: RP2Decimal = RP2Decimal(str(transaction[_COST]))
            conversion_info = f"{trade.quote_info} -> {trade.base_info}"
        elif transaction[_SIDE] == _SELL:
            out_asset = trade.base_asset
            in_asset = trade.quote_asset
            crypto_out_no_fee = RP2Decimal(str(transaction[_AMOUNT]))
            conversion_info = f"{trade.base_info} -> {trade.quote_info}"
        else:
            raise Exception(f"Internal error: unrecognized transaction side: {transaction[_SIDE]}")

        if transaction[_FEE][_CURRENCY] == out_asset:
            crypto_fee: RP2Decimal = RP2Decimal(str(transaction[_FEE][_COST]))
        else:
            crypto_fee = ZERO
        crypto_out_with_fee: RP2Decimal = crypto_out_no_fee + crypto_fee

        # Is this a plain buy or a conversion?
        if trade.quote_asset in self.__client.options[_LEGAL_MONEY]:  # Is this fiat? (options[_LEGAL_MONEY] is a list of all fiat ever traded on Binance.com)
            fiat_out_no_fee: RP2Decimal = RP2Decimal(str(transaction[_COST]))
            fiat_fee: RP2Decimal = RP2Decimal(crypto_fee)
            spot_price: RP2Decimal = RP2Decimal(str(transaction[_PRICE]))

            out_transaction_list.append(
                OutTransaction(
                    plugin=self.__BINANCE_COM,
                    unique_id=transaction[_ID],
                    raw_data=json.dumps(transaction),
                    timestamp=self._rp2_timestamp_from_ms_epoch(transaction[_TIMESTAMP]),
                    asset=out_asset,
                    exchange=self.__BINANCE_COM,
                    holder=self.account_holder,
                    transaction_type=Keyword.SELL.value,
                    spot_price=str(spot_price),
                    crypto_out_no_fee=str(crypto_out_no_fee),
                    crypto_fee=str(crypto_fee),
                    crypto_out_with_fee=str(crypto_out_with_fee),
                    fiat_out_no_fee=str(fiat_out_no_fee),
                    fiat_fee=str(fiat_fee),
                    fiat_ticker=trade.quote_asset,
                    notes=(f"{notes + ';' if notes else ''} Fiat sell of {trade.base_asset} with {trade.quote_asset}."),
                )
            )

        else:
            # Binance does not report the value of transaction in fiat
            out_transaction_list.append(
                OutTransaction(
                    plugin=self.__BINANCE_COM,
                    unique_id=transaction[_ID],
                    raw_data=json.dumps(transaction),
                    timestamp=self._rp2_timestamp_from_ms_epoch(transaction[_TIMESTAMP]),
                    asset=out_asset,
                    exchange=self.__BINANCE_COM,
                    holder=self.account_holder,
                    transaction_type=Keyword.SELL.value,
                    spot_price=Keyword.UNKNOWN.value,
                    crypto_out_no_fee=str(crypto_out_no_fee),
                    crypto_fee=str(crypto_fee),
                    crypto_out_with_fee=str(crypto_out_with_fee),
                    fiat_out_no_fee=None,
                    fiat_fee=None,
                    notes=(
                        f"{notes + '; ' if notes else ''} Sell side of conversion from "
                        f"{conversion_info}"
                        f"({in_asset} in-transaction unique id: {transaction[_ID]}"
                    ),
                )
            )

    def _process_transfer(self, transaction: Any, intra_transaction_list: List[IntraTransaction]) -> None:
        if transaction[_STATUS] == "failed":
            self.__logger.info("Skipping failed transfer %s", json.dumps(transaction))
        else:
            # This is a CCXT list must convert to string from float
            amount: RP2Decimal = RP2Decimal(str(transaction[_AMOUNT]))

            if transaction[_TYPE] == _DEPOSIT:
                intra_transaction_list.append(
                    IntraTransaction(
                        plugin=self.__BINANCE_COM,
                        unique_id=transaction[_TX_ID],
                        raw_data=json.dumps(transaction),
                        timestamp=transaction[_DATE_TIME],
                        asset=transaction[_CURRENCY],
                        from_exchange=Keyword.UNKNOWN.value,
                        from_holder=Keyword.UNKNOWN.value,
                        to_exchange=self.__BINANCE_COM,
                        to_holder=self.account_holder,
                        spot_price=Keyword.UNKNOWN.value,
                        crypto_sent=Keyword.UNKNOWN.value,
                        crypto_received=str(amount),
                    )
                )
            elif transaction[_TYPE] == _WITHDRAWAL:
                intra_transaction_list.append(
                    IntraTransaction(
                        plugin=self.__BINANCE_COM,
                        unique_id=transaction[_TX_ID],
                        raw_data=json.dumps(transaction),
                        timestamp=transaction[_DATE_TIME],
                        asset=transaction[_CURRENCY],
                        from_exchange=self.__BINANCE_COM,
                        from_holder=self.account_holder,
                        to_exchange=Keyword.UNKNOWN.value,
                        to_holder=Keyword.UNKNOWN.value,
                        spot_price=Keyword.UNKNOWN.value,
                        crypto_sent=str(amount),
                        crypto_received=Keyword.UNKNOWN.value,
                    )
                )
            else:
                self.__logger.error("Unrecognized Crypto transfer: %s", json.dumps(transaction))

    def _process_withdrawal(self, transaction: Any, out_transaction_list: List[OutTransaction], notes: Optional[str] = None) -> None:

        amount: RP2Decimal = RP2Decimal(transaction[_INDICATED_AMOUNT])
        fee: RP2Decimal = RP2Decimal(transaction[_TOTAL_FEE])
        notes = f"{notes + '; ' if notes else ''}{'Fiat Withdrawal of '}; {transaction[_FIAT_CURRENCY]}"
        out_transaction_list.append(
            OutTransaction(
                plugin=self.__BINANCE_COM,
                unique_id=transaction[_ORDER_NO],
                raw_data=json.dumps(transaction),
                timestamp=self._rp2_timestamp_from_ms_epoch(transaction[_CREATE_TIME]),
                asset=transaction[_FIAT_CURRENCY],
                exchange=self.__BINANCE_COM,
                holder=self.account_holder,
                transaction_type=Keyword.SELL.value,
                spot_price="1",
                crypto_out_no_fee=str(amount),
                crypto_fee=str(fee),
                fiat_out_no_fee=None,
                fiat_fee=None,
                fiat_ticker=transaction[_FIAT_CURRENCY],
                notes=notes,
            )
        )
