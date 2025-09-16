from .assign_user_permissions import AssignUserPermissions
from .calculate_nav import CalculateNav
from .close_fund import CloseFund
from .create_commitment import CreateCommitment
from .create_fund import CreateFund
from .create_subscription import CreateSubscription
from .create_upload_document import CreateUploadDocument
from .create_user_account import CreateUserAccount
from .deactivate_reactivate_instrument import DeactivateReactivateInstrument
from .deactivate_user_account import DeactivateUserAccount
from .execute_trade import ExecuteTrade
from .flag_transaction_for_review import FlagTransactionForReview
from .fulfill_commitment import FulfillCommitment
from .generate_report import GenerateReport
from .get_commitments import GetCommitments
from .get_document_info import GetDocumentInfo
from .get_fund_info import GetFundInfo
from .get_instrument_details import GetInstrumentDetails
from .get_investor_profile import GetInvestorProfile
from .get_nav_history import GetNavHistory
from .get_portfolio_holdings import GetPortfolioHoldings
from .get_redemption_requests import GetRedemptionRequests
from .get_subscription_details import GetSubscriptionDetails
from .get_trade_history import GetTradeHistory
from .get_user_account import GetUserAccount
from .offboard_investor import OffboardInvestor
from .onboard_investor import OnboardInvestor
from .process_redemption import ProcessRedemption
from .switch_funds import SwitchFunds
from .update_fund import UpdateFund
from .update_instrument import UpdateInstrument
from .update_user_account import UpdateUserAccount

ALL_TOOLS_INTERFACE_1 = [
    AssignUserPermissions,
    CalculateNav,
    CloseFund,
    CreateCommitment,
    CreateFund,
    CreateSubscription,
    CreateUploadDocument,
    CreateUserAccount,
    DeactivateReactivateInstrument,
    DeactivateUserAccount,
    ExecuteTrade,
    FlagTransactionForReview,
    FulfillCommitment,
    GenerateReport,
    GetCommitments,
    GetDocumentInfo,
    GetFundInfo,
    GetInstrumentDetails,
    GetInvestorProfile,
    GetNavHistory,
    GetPortfolioHoldings,
    GetRedemptionRequests,
    GetSubscriptionDetails,
    GetTradeHistory,
    GetUserAccount,
    OffboardInvestor,
    OnboardInvestor,
    ProcessRedemption,
    SwitchFunds,
    UpdateFund,
    UpdateInstrument,
    UpdateUserAccount
]
