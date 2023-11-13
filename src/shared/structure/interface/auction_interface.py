from abc import ABC, abstractmethod
from typing import Optional, Dict, List

from src.shared.structure.entities.bid import Bid
from src.shared.structure.entities.auction import Auction
from src.shared.structure.entities.payment import Payment


class AuctionInterface(ABC):
    @abstractmethod
    def create_auction(self, auction: Auction) -> Dict or None:
        """
        Create a new auction
        """
        pass

    @abstractmethod
    def get_payment_by_id(self, payment_id: str) -> Optional[Dict]:
        """
        Get a payment by id
        """
        pass

    @abstractmethod
    def create_bid(self, bid: Bid) -> Dict or None:
        """
        Create a new bid
        """
        pass

    @abstractmethod
    def create_payment(self, payment: Payment) -> Dict or None:
        """
        Create a new payment
        """
        pass

    @abstractmethod
    def get_auction_by_id(self, auction_id: str) -> Optional[Dict]:
        """
        Get a auction by id
        """
        pass

    @abstractmethod
    def get_all_bids_by_auction_id(self, auction_id: str) -> List[Dict]:
        pass

    @abstractmethod
    def get_all_auctions(self, exclusive_start_key: str, amount: int) -> Optional[Dict]:
        pass

    @abstractmethod
    def get_all_auctions_menu(self) -> Optional[List[Dict]]:
        """
        Get all auctions for menu
        """
        pass

    @abstractmethod
    def update_auction(self, auction: Auction = None, auction_dict: Dict = None) -> Optional[Dict]:
        """
        Update the basics information of the auction
        Don't update the bids, payments and created_by
        """
        pass

    @abstractmethod
    def update_auction_current_amount(self, auction_id: str = None, amount: float = None) -> Optional[Dict]:
        """
        Update the current amount of the auction
        """
        pass

    @abstractmethod
    def get_auction_between_dates(self, start_date: int, end_date: int) -> Optional[Dict]:
        pass

    @abstractmethod
    def get_last_auction_id(self) -> Optional[int]:
        pass

    @abstractmethod
    def get_last_bid_id(self, auction_id: str) -> Optional[int]:
        pass

    @abstractmethod
    def get_payment_by_auction(self, auction_id: str) -> Optional[Dict]:
        pass

    @abstractmethod
    def update_status_payment(self, auction_id: str = None, payment_id: str = None, status_payment: str = None) -> Optional[Dict]:
        pass
